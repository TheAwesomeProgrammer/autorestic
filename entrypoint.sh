#!/bin/sh
python3 /template.py
if [ -n "$CRON_CONFIG_DIR" ]
then
    autorestic check -c $CRON_CONFIG_DIR
    autorestic $AUTORESTIC_INITIAL_ARGS
    echo "CRON_CONFIG_DIR is set, cron enabled"
    crond -f -L /var/log/cron.log
else
    autorestic check -c $CONFIG_DIR
    autorestic $AUTORESTIC_INITIAL_ARGS
    exit 0
fi