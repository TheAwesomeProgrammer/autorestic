mv /postgres/pgdata/pg_wal /tmp/orig-pg_wal
rm -rf /postgres/pgdata/*
cp -a /data/database-basebackup/. /postgres/pgdata/
chown -R 999:999 /postgres/pgdata/
chmod -R 700 /postgres/pgdata/
rm -rf /postgres/pgdata/pg_wal
cp -a /tmp/orig-pg_wal/. /postgres/pgdata/pg_wal/
touch /postgres/pgdata/recovery.signal