#!/bin/bash
# Copyright (c) Magnon Compute Corporation. All rights reserved.
ray start --head --port=6379
python3 server.py
python3 client.py
ray stop --force