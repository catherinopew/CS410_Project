#!/bin/bash

gunicorn -w 2 -b 0.0.0.0:8080 run_ws:app --daemon
sudo service analyzer start
