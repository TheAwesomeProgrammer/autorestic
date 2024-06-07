rm -r /postgres/*
cp -a /data/database-basebackup/. /postgres/${POSTGRES_DATA_FOLDER}/
chown -R ${DATABASE_OWNER_ID} /postgres/${POSTGRES_DATA_FOLDER}/
chmod -R 700 /postgres/${POSTGRES_DATA_FOLDER}/