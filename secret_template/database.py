import os
from sh import pg_dump
import subprocess

host = '127.0.0.1'

POSTGRES_TYPE = 'postgres'
MARIA_DB_TYPE = 'mariadb'

DUMP_BACKUP_TYPE = 'dump'
ARCHIVE_BACKUP_TYPE = 'archive'

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_TYPE = os.getenv('DATABASE_TYPE')
DATABASE_BACKUP_TYPE = os.getenv('DATABASE_BACKUP_TYPE')

if DATABASE_NAME is None or DATABASE_USERNAME is None or DATABASE_PASSWORD is None:
    raise SystemExit(0)

if DATABASE_BACKUP_TYPE is None:
    DATABASE_BACKUP_TYPE = DUMP_BACKUP_TYPE

if DATABASE_HOST is not None:
    host = DATABASE_HOST
if DATABASE_TYPE is None:
    DATABASE_TYPE = POSTGRES_TYPE


os.makedirs('/data/database-dump/', exist_ok=True)
os.makedirs('/data/database-basebackup', exist_ok=True)

if DATABASE_TYPE == POSTGRES_TYPE:
    if DATABASE_BACKUP_TYPE == DUMP_BACKUP_TYPE:
        pg_dump('-h', host, '-U', DATABASE_USERNAME, DATABASE_NAME, _out='/data/database-dump/dump.sql', _env={"PGPASSWORD": DATABASE_PASSWORD})
    elif DATABASE_BACKUP_TYPE == ARCHIVE_BACKUP_TYPE:
        subprocess.Popen(['pg_basebackup', '-D', '/data/database-basebackup' '-d', f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{host}'], shell=True)
elif DATABASE_TYPE == MARIA_DB_TYPE:
     subprocess.Popen(['mysqldump', '-u',DATABASE_USERNAME,'-p%s'%DATABASE_PASSWORD,DATABASE_NAME],shell=True)
