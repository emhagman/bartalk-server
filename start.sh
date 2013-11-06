#!/bin/sh

uwsgi --socket :9003 --wsgi-file bartalk/wsgi.py --enable-threads --py-auto-reload=1
