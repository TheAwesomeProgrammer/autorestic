#!/bin/bash
echo "autorestic cron process has started"
python3 /template.py
autorestic -c $CRON_CONFIG_DIR --ci cron > /var/log/autorestic-cron.log 2>&1
echo "autorestic cron process has finished"