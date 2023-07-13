#!/bin/bash
pkill -9 celery
celery worker -A trustid_project & celery -A trustid_project beat & celery flower -A trustid_project --conf=./trustid_project/flowerconfig.py
sleep 5
