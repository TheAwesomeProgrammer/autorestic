cd ${VAULT_SECRETS_DIR_PATH};
curl -L https://github.com/jonasvinther/medusa/releases/download/v0.3.5/medusa_0.3.5_linux_amd64.tar.gz | tar -xz;
 ./medusa import secret ${VAULT_SECRETS_DIR_PATH}/${VAULT_SECRET_FILENAME} --address="${VAULT_URL}"  --token="${VAULT_TOKEN}" --insecure;