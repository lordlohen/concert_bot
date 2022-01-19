#!/usr/bin/env bash

docker run \
  --name redis \
  --rm \
  -v ${PWD}/redis_data:/data \
  -p 6379:6379 \
  redis:6.2-alpine \
    redis-server --save 60 1 --loglevel warning
