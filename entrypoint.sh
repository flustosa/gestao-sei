#!/usr/bin/env bash
cd /gestao-sei/app_sei/ && flask db init
cd /gestao-sei/app_sei/ && flask db migrate 
cd /gestao-sei/app_sei/ && flask db upgrade
cd /gestao-sei/ && python3 main.py

