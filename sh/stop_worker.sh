#!/usr/bin/env bash

celery multi stop w1 -A app -l info
celery multi stopwait w1 -A app -l info