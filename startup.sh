#!/bin/sh
gunicorn  -c gunicorn_conf.py app:app