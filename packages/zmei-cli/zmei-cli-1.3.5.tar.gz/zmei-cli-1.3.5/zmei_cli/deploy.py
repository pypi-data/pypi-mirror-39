import os
from textwrap import dedent


def generate_dockerignore(target_path):
    tpl = dedent("""
        .zmei-cache
        *.sqlite*
    """)

    target_file = os.path.join(target_path, '.dockerignore')
    if not os.path.exists(target_file):
        with open(target_file, 'w') as f:
            f.write(tpl)


def generate_dockerfile(target_path):
    tpl = dedent("""
        FROM zmeigen/app

        COPY *requirements*.txt /var/www/app/
        
        WORKDIR /var/www/app
        
        RUN /var/www/env/bin/pip install -r requirements.prod.txt
        
        COPY . /var/www/app
        RUN /var/www/env/bin/python manage.py collectstatic --noinput -l

    """)

    target_file = os.path.join(target_path, 'Dockerfile')
    if not os.path.exists(target_file):
        with open(target_file, 'w') as f:
            f.write(tpl)

def generate_setting(target_path):
    tpl = dedent("""
        from .settings import *
        
        ALLOWED_HOSTS += ['*']
        
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'app',
                'USER': 'root',
                'PASSWORD': '123123',
                # 'HOST': 'localhost',
                # 'PORT': '',
            }
        }
        
        CACHES = {
            'default': {
                'BACKEND': 'redis_cache.RedisCache',
                'LOCATION': [
                    '127.0.0.1:6379',
                ],
                'OPTIONS': {
                    'DB': 1,
                    # 'PASSWORD': 'yadayada',
                    'PARSER_CLASS': 'redis.connection.HiredisParser',
                    'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                    'CONNECTION_POOL_CLASS_KWARGS': {
                        'max_connections': 50,
                        'timeout': 20,
                    },
                    'MAX_CONNECTIONS': 1000,
                    'PICKLE_VERSION': -1,
                },
            },
        }
        
        STATIC_ROOT = '/var/www/var/static/'
        
        MEDIA_ROOT = '/var/www/var/media/'

    """)

    target_file = os.path.join(target_path, 'app/settings_prod.py')
    if not os.path.exists(target_file):
        with open(target_file, 'w') as f:
            f.write(tpl)


def generate_req_prod(target_path):
    req_file = os.environ.get('ZMEI_REQUIREMNETS_FILE', 'requirements.txt')
    tpl = dedent(f"""
        -r {req_file}
        
        mysqlclient
        django-redis-cache
    """)

    target_file = os.path.join(target_path, 'requirements.prod.txt')
    if not os.path.exists(target_file):
        with open(target_file, 'w') as f:
            f.write(tpl)