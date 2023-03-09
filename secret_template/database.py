import os
from sh import pg_dump

host = '127.0.0.1'

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')

if DATABASE_NAME is None or DATABASE_USERNAME is None or DATABASE_PASSWORD is None:
    raise SystemExit(0)

if DATABASE_HOST is not None:
    host = DATABASE_HOST

os.makedirs('/data/database-dump/', exist_ok=True)
pg_dump('-h', '127.0.0.1', '-U', DATABASE_USERNAME, DATABASE_NAME, _out='/data/database-dump/dump.sql', _env={"PGPASSWORD": DATABASE_PASSWORD})