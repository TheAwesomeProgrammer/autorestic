import os
import json 
from string import Template
from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = os.getenv('CRON_CONFIG_DIR')
BACKEND_CONFIGS_PATH = os.getenv('BACKEND_CONFIGS_PATH')
BACKUP_SCRIPT_NAME = os.getenv('BACKUP_SCRIPT_NAME')
BEFORE_BACKUP_SCRIPT_NAME = os.getenv('BEFORE_BACKUP_SCRIPT_NAME')
BACKUP_PATH = os.getenv('BACKUP_PATH')
CRON_SCHEDULE = os.getenv('CRON_SCHEDULE')

DefaultScript = "echo 'nothing'"

def create_backend(backend_config ,encryption_key, backup_path):
  print(backend_config)
  type = backend_config['type']
  
  if type == 's3':
    return create_s3_backend(backend_config, encryption_key, backup_path)
  elif type == 'rest':
    return create_rest_backend(backend_config, encryption_key, backup_path)
  

def create_rest_backend(backend_config ,encryption_key, backup_path):
    backend_template = Template("""
  $server_name:
    type: rest
    path: '${server_path}/${backup_path}'
    key: '${encryption_key}'
    rest:
      user: ${username}
      password:  ${password}""")
        
    return backend_template.substitute(server_name=backend_config['server_name'], server_path=backend_config['server_path'],
                                       backup_path=backup_path, username=backend_config['username'], password=backend_config['password'], encryption_key=encryption_key)
    
def create_s3_backend(backend_config ,encryption_key, backup_path):
    backend_template = Template("""
  $server_name:
    type: s3
    path: '${server_path}/backup'
    key: '${encryption_key}'
    env:
      AWS_ACCESS_KEY_ID: ${s3_key_id}
      AWS_SECRET_ACCESS_KEY: ${s3_secret_key}""")
        
    return backend_template.substitute(server_name=backend_config['server_name'], server_path=backend_config['server_path'],
                                       backup_path=backup_path, s3_key_id=backend_config['s3_key_id'], s3_secret_key=backend_config['s3_secret_key'], encryption_key=encryption_key)
    
def create_hooks(backup_script_name, before_backup_script_name):
    hooks_template = Template("""
    hooks:
      backup:
        before:
          - python3 /database.py
          - ${before_backup_script_name}
        success:
          - ${backup_script_name} 0
        failure:
          - ${backup_script_name} -1""")
        
    return hooks_template.substitute(backup_script_name=backup_script_name, before_backup_script_name=before_backup_script_name)


path_to_config_file = CONFIG_DIR
with open(BACKEND_CONFIGS_PATH, 'r') as f:
  backend_configs = json.load(f)

config_content = """version: 3

locations:
  home:
    forget: prune # Or only "yes" if you don't want to prune
    options:
      forget:
        keep-last: 5 # always keep at least 5 snapshots
        keep-daily: 7 # keep74 last daily snapshots
        keep-weekly: 4 # keep 1 last weekly snapshots
        keep-monthly: 12 # keep 12 last monthly snapshots
        keep-yearly: 10 # keep 5 last yearly snapshots
        keep-within: '14d' # keep snapshots from the last 14 days
    from: /data
    to: """

for backend_config in backend_configs["configs"]:
   config_content += "\n    - " + backend_config['server_name']
   
config_content += create_hooks(BACKUP_SCRIPT_NAME or DefaultScript, BEFORE_BACKUP_SCRIPT_NAME or DefaultScript)

config_content += "\n    cron: '" + CRON_SCHEDULE + "'"
  
config_content += "\n\nbackends:"

for backend_config in backend_configs["configs"]:
  config_content += create_backend(backend_config, backend_configs["encryptionKey"], BACKUP_PATH)


os.makedirs(os.path.dirname(path_to_config_file), exist_ok=True)
config_file = open(path_to_config_file, "w")
config_file.write(config_content)
config_file.close()





