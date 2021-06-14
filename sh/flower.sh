#!/usr/bin/env bash


celery flower -A app --address=127.0.0.1 --port=5555 redis://:123456@127.0.0.1:6379 --basic_auth=root:123
