#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=src.tasks.celery_app:celery worker -l INFO; fi
if [[ "${1}" == "celery_beat" ]]; then
    celery --app=src.tasks.celery_app:celery worker -l INFO -B;
elif [[ "${1}" == "flower" ]]; then
    celery --app=src.tasks.celery_app:celery flower; fi