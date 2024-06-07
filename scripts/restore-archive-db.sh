cp -a /data/database-basebackup/. /postgres/${POSTGRES_DATA_FOLDER}/
chown -R 999:999 /postgres/${POSTGRES_DATA_FOLDER}/
chmod -R 700 /postgres/${POSTGRES_DATA_FOLDER}/