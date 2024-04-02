import os
import json 
from generate_backend import generate_backend
from jinja2 import Environment, FileSystemLoader, select_autoescape

from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = os.getenv('CRON_CONFIG_DIR')
if os.getenv('CONFIG_DIR'):
  CONFIG_DIR = os.getenv('CONFIG_DIR')
BACKEND_CONFIGS_PATH = os.getenv('BACKEND_CONFIGS_PATH')
BACKUP_SCRIPT_NAME = os.getenv('BACKUP_SCRIPT_NAME')
BEFORE_BACKUP_SCRIPT_NAME = os.getenv('BEFORE_BACKUP_SCRIPT_NAME')
BACKUP_PATH = os.getenv('BACKUP_PATH')
CRON_SCHEDULE = os.getenv('CRON_SCHEDULE')
HEALTH_CHECKS_URL = os.getenv('HEALTH_CHECKS_URL')

path_to_config_file = CONFIG_DIR
with open(BACKEND_CONFIGS_PATH, 'r') as f:
  backend_configs = json.load(f)

generated_backend_configs = []
backend_names = []

for backend_config in backend_configs["configs"]:
  backend_names.append(backend_config['server_name'])
  generated_backend_configs.append(generate_backend(backend_config, backend_configs["encryptionKey"], BACKUP_PATH))

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
print(template_dir)
env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True,lstrip_blocks=True)
autorestic_template = env.get_template("autorestic.yaml")
rendered_autorestic_template = autorestic_template.render(
  CONFIG_DIR=CONFIG_DIR,
  BACKEND_CONFIGS_PATH=BACKEND_CONFIGS_PATH,
  BACKUP_SCRIPT_NAME=BACKUP_SCRIPT_NAME,
  BEFORE_BACKUP_SCRIPT_NAME=BEFORE_BACKUP_SCRIPT_NAME,
  BACKUP_PATH=BACKUP_PATH,
  CRON_SCHEDULE=CRON_SCHEDULE,
  HEALTH_CHECKS_URL=HEALTH_CHECKS_URL,
  backend_names=backend_names,
  backend_configs=generated_backend_configs,
)


os.makedirs(os.path.dirname(path_to_config_file), exist_ok=True)
config_file = open(path_to_config_file, "w")
config_file.write(rendered_autorestic_template)
config_file.close()