import os
from sh import pg_dump

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

if DATABASE_NAME is None or DATABASE_USERNAME is None or DATABASE_PASSWORD is None:
    raise SystemExit(0)

pg_dump('-h', '127.0.0.1', '-U', DATABASE_USERNAME, DATABASE_NAME, '>', '/data/database-dump/dump.sql', _env={"PGPASSWORD": DATABASE_PASSWORD})