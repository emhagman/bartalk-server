#!/bin/sh

uwsgi --socket :9000 --wsgi-file bartalk/wsgi.py --enable-threads 20
