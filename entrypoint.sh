#!/bin/sh
python3 /template.py
autorestic check -c $CRON_CONFIG_DIR
autorestic $AUTORESTIC_INITIAL_ARGS
if [ -n "$CRON_CONFIG_DIR" ]
then
    echo "CRON_CONFIG_DIR is set, cron enabled"
    crond -f -L /var/log/cron.log
else
    exit 0
fi