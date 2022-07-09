# CodeCourt

Code submission and evaluation plaform using docker for execution and security. It's a court for code, constituting judges of different languages, conducting sessions in their own container.

Currently supports c11, c++14, c++17, c++20, python 2 and python 3, with more to come.

## Deploying to production
Use [this](https://rahmonov.me/posts/run-a-django-app-with-nginx-and-gunicorn/) or follow below

1. Install necessary software
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install python3-pip python3.8-venv nginx supervisor
    ```

2. Install docker from [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository), or follow steps below
    ```bash
    sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    sudo reboot

    sudo groupadd docker
    sudo gpasswd -a $USER docker
    ```

4. Setup postgres 12
    ```bash
    sudo apt-get install libpq-dev python-dev
    sudo apt-get install postgresql postgresql-contrib
    
    sudo su - postgres
    createdb ccdb
    createuser -P ccuser
    ```
    Create password for ccuser, and keep in mind, will come handy.

    Now, withing the postgres su
    ```bash
    psql
    GRANT ALL PRIVILEGES ON DATABASE ccdb TO ccuser;
    ```

    Add/replace below in `codecourt/settings.py` appropriately
    ```py
    import psycopg2.extensions
    # ...
    HOST = os.environ.get('HOST')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_NAME = os.environ.get('CCDB_NAME')
    DB_USERNAME = os.environ.get('CCDB_USERNAME')
    DB_USERPASS = os.environ.get('CCDB_USERPASS')
    # ...
    DEBUG = False
    # ...
    ALLOWED_HOSTS = [HOST]
    # ...
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USERNAME,
            'PASSWORD': DB_USERPASS,
            'HOST': 'localhost',
            'PORT': '',
        },
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    }
    ```

4. Add ENV to /etc/supervisor/conf.d/codecourt.d in last line
    ```
    environment=HOST='',SECRET_KEY ='',CCDB_NAME='',CCDB_USERNAME='',CCDB_USERPASS='',BASE_URL=''
    ```

3. Setup venv.
    ```bash
    python3 -m venv venv
    ```

4. create /etc/nginx/sites-available/codecourt and write
    ```
    server {
        listen 8000;
        server_name 0.0.0.0;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static/ {
                root /home/ubuntu/codecourt;
        }

        location / {
                include proxy_params;
                proxy_pass http://unix:/home/ubuntu/codecourt/codecourt.sock;
        }
    }
    ```

5. Link and test the above file, then restart nginx
    ```bash
    sudo ln -s /etc/nginx/sites-available/codecourt /etc/nginx/sites-enabled
    sudo nginx -t
    sudo service nginx restart
    ```

6. create /etc/supervisor/conf.d/codecourt.conf and write
    ```
    [program:codecourt]
    command=/bin/sh start.sh
    directory=/home/ubuntu/codecourt
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/codecourt.err.log
    stdout_logfile=/var/log/codecourt.out.log
    environment=HOST='',SECRET_KEY ='',CCDB_NAME='',CCDB_USERNAME='',CCDB_USERPASS='',BASE_URL=''
    ```

6. restart, update and get status of project using supervisor
    ```bash
    sudo service supervisor restart
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl status myproject
    ```
