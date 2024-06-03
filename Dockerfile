FROM golang:1.19-alpine as builder


WORKDIR /app
COPY go.* .
RUN go mod download
COPY . .
RUN go build

FROM restic/restic:0.15.1
RUN apk add --no-cache rclone bash curl
RUN mkdir -p /scripts
COPY --from=builder /app/autorestic /usr/bin/autorestic
COPY entrypoint.sh /entrypoint.sh
COPY secret_template /
COPY scripts/ /scripts
COPY crond.sh /crond.sh
RUN chmod +x /entrypoint.sh /crond.sh /template.py /database.py /scripts/backup-vault.sh /scripts/restore-vault.sh
RUN apk add --no-cache python3 py3-pip postgresql-client-16 mariadb-client
RUN pip3 install sh Jinja2
# show autorestic cron logs in docker
RUN ln -sf /proc/1/fd/1 /var/log/autorestic-cron.log
# run autorestic-cron every minute
RUN echo -e "*/1 * * * * bash /crond.sh" >> /etc/crontabs/root

ENTRYPOINT []
CMD /entrypoint.sh
