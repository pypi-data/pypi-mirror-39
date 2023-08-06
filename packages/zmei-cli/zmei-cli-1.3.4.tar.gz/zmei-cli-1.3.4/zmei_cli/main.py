import atexit
import os
import signal
import sys

import click
import requests.exceptions
from termcolor import colored
from terminaltables import AsciiTable
from time import sleep

from zmei_cli.client import ZmeiApiClient, ApiError
from zmei_cli.config import Config
from zmei_cli.deploy import generate_setting, generate_req_prod
from zmei_cli.utils import collect_files, extract_files, collect_app_names, migrate_db, install_deps, remove_db, \
    wait_for_file_changes, run_django, run_webpack, npm_install, get_watch_paths, run_celery, run_livereload
import json

zmei = ZmeiApiClient(
    api_url=os.environ.get('ZMEI_URL', 'http://ng.genius-project.io:9000/api/'),
    # api_url=os.environ.get('ZMEI_URL', 'http://127.0.0.1:9000/api/'),
    apps_url=os.environ.get('ZMEI_APPS_URL', 'https://zmei-framework.com/')
    # apps_url=os.environ.get('ZMEI_APPS_URL', 'http://127.0.0.1:8000/')
)

def ensure_logged_in(msg='Login required to continue. You can create account at https://zmei-framework.com/auth/registration/\n'):
    if not zmei.is_logged_in():
        if msg:
            print(msg)

        email = click.prompt('Email address')
        password = click.prompt('Password', hide_input=True)

        success = zmei.login(email, password)
        if not success:
            print('Can not login with provided credentials.')
        return success
    else:
        return True



@click.group()
def main(**args):
    pass

def prepare_app():
    ensure_logged_in()

    c = Config(os.getcwd())
    c.load(interactive=False)

    key_path = c.config['ssh_public_key']
    app_name = c.config['app_name']

    c.save()

    generated = c.generate_new_ssh_key(key_path)
    if not generated:
        print('Can not continue without ssh key.')

    key_info = zmei.ssh_key_get(name=app_name)
    if not key_info:
        with open(key_path) as f:
            key_info = zmei.ssh_key_create(app_name, f.read())

    app = zmei.app_get(ref=app_name)
    if not app:
        app = zmei.app_create(ref=app_name, key=key_info['id'])

    if not app['ssh_port']:
        print('Waiting application to open ssh port')

    i = 0
    while not app['ssh_port']:
        print('.', end='', flush=True)
        sleep(2)
        app = zmei.app_get(ref=app_name)
        i += 1
        if i > 50:
            print('Seems to be application is still offline. Is it a bug? contact support...')
            sys.exit()
    sleep(3)
    # print('S')

    return app

def run_command(cmd, show=False):
    print(cmd)
    if not show:
        os.system(cmd)

@main.command(help='Ssh into deployed application')
@click.option('--show', help='Only print connect command', is_flag=True, default=False)
@click.pass_context
def ssh(context, show, **args):
    app = prepare_app()
    if not app:
        return

    if not app['ssh_port']:
        print('Applications is not ready. Waiting')
        while not app['ssh_port']:
            sleep(1)
            print('.')
            app = zmei.app_get(ref=app['ref'])

    run_command(f"ssh root@genius-apps.com -p {app['ssh_port']}", show=show)

@main.command(help='Deploy')
@click.pass_context
def deploy(context, **args):
    app = prepare_app()
    if not app:
        return

    generate_setting('.', app)
    generate_req_prod('.', app)

    run_command(
        f"rsync --exclude *.pyc --exclude .env --exclude __pycache__ --exclude *.sqlite* --exclude .idea --exclude .git .e  -e 'ssh -p {app['ssh_port']}' -rv ./ root@genius-apps.com:/var/www/app/")
    run_command(f"ssh -p {app['ssh_port']} root@genius-apps.com bash /var/www/deploy.sh")

    print(f"Your application is up at http://{app['ref']}.genius-apps.com/")

@main.group(help='Application management')
@click.pass_context
def app(context, **args):
    ensure_logged_in()

@app.command(help='Create application', name='create')
@click.option('--ref', help='Reference name of the new application')
@click.option('--key', help='Key id to use')
def app_create(ref, key, **args):
    if not key:
        print("Key is required")
        return

    new_app = zmei.app_create(ref, key)
    print(f"Created new app with id {new_app['id']}")

@app.command(help='Delete application and it\'s container and create from scratch', name='rebuild')
@click.option('--ref', help='Reference name of the new application')
def app_rebuild(ref, **args):
    app = zmei.app_get(ref=ref)
    print('Deleting application')
    zmei.app_delete(ref=app['ref'])
    print('Waiting ...')
    sleep(2)
    new_app = zmei.app_create(ref=app['ref'], key=app['key']['id'])
    print(f"Created new app with id {new_app['id']}")

@app.command(help='Delete application', name='delete')
@click.option('--ref', help='Reference name of the application to delete')
@click.option('--id', help='Id of the application to delete')
def app_delete(ref, id, **args):
    if ref:
        result = zmei.app_delete(ref=ref)
    elif id:
        result = zmei.app_delete(app_id=id)
    else:
        print('Specify --ref or --id of the application you wish to delete')
        return
    if result:
        print(f"App deleted.")
    else:
        print("App you requested, do not exist")

@app.command(help='List applications', name='list')
def app_list(**args):
    apps = zmei.app_list()

    if not len(apps):
        print("You have no applications.")
        return

    table = [
        ['Id', 'Reference name (ref)', 'Server created?', 'Public', 'Ssh port', 'Ssh key']
    ]

    for app in apps:
        if app['created']:
            table.append([
                app['id'],
                app['ref'],
                '+' if app['created'] else '',
                f"http://{app['ref']}.genius-apps.com/",
                app['ssh_port'],
                app['key']['name'] if app['key'] else '',
            ])
        else:
            table.append([
                app['id'],
                app['ref'],
                '',
                '',
                '',
                app['key']['name'] if app['key'] else '',
            ])
    print(AsciiTable(table).table)

@main.group(help='Ssh key management')
@click.pass_context
def key(context, **args):
    ensure_logged_in()

@key.command(help='Create ssh key', name='create')
@click.option('--name', help='Name of the new ssh key', default='default')
@click.option('--key', help='Key path', default='~/.ssh/id_rsa.pub')
def key_create(name, key, **args):
    with open(os.path.expanduser(key)) as f:
        key_source = f.read()
    new_key = zmei.ssh_key_create(name, key_source)
    print(f"Created new key with id {new_key['id']}")

@key.command(help='Delete ssh key', name='delete')
@click.option('--name', help='Name of the ssh key to delete')
@click.option('--id', help='Id of the ssh key to delete')
def key_delete(name, id, **args):
    if name:
        result = zmei.ssh_key_delete(name=name)
    elif id:
        result = zmei.ssh_key_delete(ssh_key_id=id)
    else:
        print('Specify --name or --id of the ssh key you wish to delete')
        return
    if result:
        print(f"Key deleted.")
    else:
        print("Key you requested, do not exist")

@key.command(help='List ssh keys', name='list')
def key_list(**args):
    keys = zmei.ssh_key_list()

    if not len(keys):
        print("You have no ssh keys.")
        return

    table = [
        ['Id', 'Name', 'Key']
    ]

    for key in keys:
        table.append([
            key['id'],
            key['name'],
            f"{key['key'][:20]}...{key['key'][-50:]}"
        ])
    print(AsciiTable(table).table)

@main.command(help='Deploy to hyper.sh')
def login(*args, **kwargs):
    if zmei.is_logged_in():
        if not click.confirm('Already logged in. Logout and login again?'):
            return
        zmei.logout()

    ensure_logged_in(msg='')

@main.command(help='Deploy to hyper.sh')
def logout(*args, **kwargs):
    zmei.logout()

@main.group()
@click.option('--src', default='.', help='Sources path')
@click.option('--dst', default='.', help='Target path')
def gen(**args):
    ensure_logged_in()

@gen.command(help='Generate and start app')
@click.option('--port', default='8000', help='Django host:port to run on')
@click.option('--host', default=None, help='Django host:port to run on')
@click.option('--live', default=False, is_flag=True, help='Reload browser on changes')
def up(**args):
    gen(up=True, **args)

@gen.command(help='Run application')
@click.option('--nodejs', is_flag=True, help='Initialize nodejs dependencies')
@click.option('--celery', is_flag=True, help='Run celery worker & beat')
@click.option('--watch', is_flag=True, help='Watch for changes')
@click.option('--webpack', is_flag=True, help='Run webpack with reload when generation ends')
@click.option('--port', default='8000', help='Django host:port to run on')
@click.option('--host', default=None, help='Django host:port to run on')
def app_run(**kwargs):
    gen(run=True, **kwargs)

@gen.command(help='Just generate the code')
@click.argument('app', nargs=-1)
def generate(app=None, **args):
    gen(app=app or [])

@gen.command(help='Install project dependencies')
def install():
    gen(install=True)

@gen.group(help='Database related commands')
def db(**args):
    pass

@db.command(help='Creates database migrations and apply them')
@click.argument('app', nargs=-1)
def migrate(app, **args):
    gen(auto=True, app=app)

@db.command(help='db remove + db migrate')
@click.argument('app', nargs=-1)
def rebuild(app, **args):
    gen(rebuild=True, app=app)

@db.command(help='Rollback all the migrations')
@click.argument('app', nargs=-1)
def remove(app, **args):
    gen(remove=True, app=app)

def gen(auto=False,
        src='.',
        dst='.',
        install=False,
        rebuild=False,
        remove=False,
        app=None,
        run=False,
        live=False,
        webpack=False,
        nodejs=False,
        celery=False,
        host=None,
        port=8000,
        watch=False,
        up=False
        ):

    if rebuild:
        auto = True
        remove = True

    if not host:
        host = '127.0.0.1:{}'.format(port)

    if up:
        install = True
        auto = True
        watch = True
        run = True

    if not app or len(app) == 0:
        app = collect_app_names()

    src = os.path.realpath(src)
    dst = os.path.realpath(dst)

    livereload_process = None
    django_process = None
    webpack_process = None
    celery_process = None

    def emergency_stop():
        if livereload_process:
            os.killpg(os.getpgid(livereload_process.pid), signal.SIGTERM)
        if django_process:
            os.killpg(os.getpgid(django_process.pid), signal.SIGTERM)
        if webpack_process:
            os.killpg(os.getpgid(webpack_process.pid), signal.SIGTERM)
        if celery_process:
            os.killpg(os.getpgid(celery_process.pid), signal.SIGTERM)

        sleep(1)
        print('\n')

    atexit.register(emergency_stop)

    for i in wait_for_file_changes(get_watch_paths(), watch=watch):
        print('--------------------------------------------')
        print('Generating ...')
        print('--------------------------------------------')

        files = collect_files(src)

        try:
            files = zmei.generate(files, collections=app)
            if up and os.path.exists('app/celery.py'):
                celery = True

            changed = extract_files(dst, files)

            if up and os.path.exists('react'):
                webpack = True
                nodejs = True

            if nodejs and os.path.exists('react'):
                npm_install()

            if remove:
                remove_db(apps=app)

            if install or rebuild:
                django_process = install_deps(django_process)

            if auto and (changed.models or not django_process):
                migrate_db(apps=app)

            if run and live and not livereload_process:
                livereload_process = run_livereload()

            if run and not django_process:
                django_process = run_django(run_host=host)

            if webpack and not webpack_process:
                webpack_process = run_webpack()

            if celery:
                # restart celery process on changes
                if celery_process:
                    os.killpg(os.getpgid(celery_process.pid), signal.SIGTERM)

                celery_process = run_celery()

            if watch:
                print(colored('> ', 'white', 'on_blue'), 'Watching for changes...')

        except ApiError as e:
            content = e.response.content.decode()
            try:
                content = json.loads(content)

                if 400 <= e.response.status_code < 500 and 'detail' in content:
                    print(content['detail'])
                    continue

            except ValueError:
                pass

            print(f'Error when accessing server. Status: {e.response.status_code}')
            print(e.response.content.decode())

        except requests.exceptions.ConnectionError as e:
            print('Can not connect to server.')
            print()
            return


def run():
    try:
        main()

    except ApiError as e:
        print(e)
