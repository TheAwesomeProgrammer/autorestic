from string import Template

def generate_backend(backend_config, encryption_key, backup_path):
  type = backend_config['type']
  
  if type == 's3':
    return create_s3_backend(backend_config, encryption_key, backup_path)
  elif type == 'rest':
    return create_rest_backend(backend_config, encryption_key, backup_path)
  elif type == 'sftp':
    return create_sftp_backend(backend_config, encryption_key, backup_path)
  

def create_rest_backend(backend_config ,encryption_key, backup_path):
    backend_template = Template("""$server_name:
    type: rest
    path: '${server_path}/${backup_path}'
    key: '${encryption_key}'
    rest:
      user: ${username}
      password:  ${password}""")
        
    return backend_template.substitute(server_name=backend_config['server_name'], server_path=backend_config['server_path'],
                                       backup_path=backup_path, username=backend_config['username'], password=backend_config['password'], encryption_key=encryption_key)
    
def create_s3_backend(backend_config ,encryption_key, backup_path):
    backend_template = Template("""$server_name:
    type: s3
    path: '${server_path}/backup'
    key: '${encryption_key}'
    env:
      AWS_ACCESS_KEY_ID: ${s3_key_id}
      AWS_SECRET_ACCESS_KEY: ${s3_secret_key}""")
        
    return backend_template.substitute(server_name=backend_config['server_name'], server_path=backend_config['server_path'],
                                       backup_path=backup_path, s3_key_id=backend_config['s3_key_id'], s3_secret_key=backend_config['s3_secret_key'], encryption_key=encryption_key)
    
    
def create_sftp_backend(backend_config ,encryption_key, backup_path):
    backend_template = Template("""$server_name:
    type: sftp
    path: '${server_path}:/backup/${backup_path}'
    key: '${encryption_key}'""")
        
    return backend_template.substitute(server_name=backend_config['server_name'], server_path=backend_config['server_path'],
                                       backup_path=backup_path, encryption_key=encryption_key)