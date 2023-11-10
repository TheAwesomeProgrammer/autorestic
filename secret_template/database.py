import os
from sh import pg_dump
import subprocess

host = '127.0.0.1'

POSTGRES_TYPE = 'postgres'
MARIA_DB_TYPE = 'mariadb'

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_TYPE = os.getenv('DATABASE_TYPE')

if DATABASE_NAME is None or DATABASE_USERNAME is None or DATABASE_PASSWORD is None:
    raise SystemExit(0)

if DATABASE_HOST is not None:
    host = DATABASE_HOST
if DATABASE_TYPE is None:
    DATABASE_TYPE = POSTGRES_TYPE

os.makedirs('/data/database-dump/', exist_ok=True)

if DATABASE_TYPE == POSTGRES_TYPE:
    pg_dump('-h', host, '-U', DATABASE_USERNAME, DATABASE_NAME, _out='/data/database-dump/dump.sql', _env={"PGPASSWORD": DATABASE_PASSWORD})
elif DATABASE_TYPE == MARIA_DB_TYPE:
     subprocess.Popen(['mysqldump', '-u',DATABASE_USERNAME,'-p%s'%DATABASE_PASSWORD,DATABASE_NAME],shell=True)
