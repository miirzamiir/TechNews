FROM postgres:13

RUN apt-get update && apt-get install -y cron gettext

COPY postgres.env .

# Save backups every night at 00:00
RUN export $(grep -v '^#' /app/.env | xargs) && \
    echo "0 0 * * * postgres pg_dump -U $DB_USER \
    -d $DB_NAME -t news_news -t news_tag -t news_news_tags > \
    /var/lib/postgresql/data/backup.sql && echo Backup created \
    at \$(date) >> /var/lib/postgresql/data/backup.log 2>&1" >> /etc/crontab

# Start cron and PostgreSQL
CMD cron && docker-entrypoint.sh postgres

EXPOSE 5432
