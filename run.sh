#! /usr/bin/env bash

python manage.py migrate

sleep 10;
python manage.py loaddata fixtures/load_users.json

sleep 10;
python manage.py loaddata fixtures/load_images.json

sleep 10;
python manage.py loaddata fixtures/load_mailing.json

sleep 10;
python manage.py test app.test.test_models

sleep 10;
python manage.py test app.test.test_endpoints

sleep 10;
python manage.py runserver