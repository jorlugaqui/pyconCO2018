#!/bin/sh

celery -A celery.celeryconf worker -Q default -l info
