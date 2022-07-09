#!/bin/bash

source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
# it asks if you wish to overrite static files, which is fine.
echo "yes" | python manage.py collectstatic
$HOME/codecourt/venv/bin/gunicorn --workers 3 --bind unix:$HOME/codecourt/codecourt.sock codecourt.wsgi
# wait for gunicorn to complete, to prevent supervisor from restarting
wait $!
