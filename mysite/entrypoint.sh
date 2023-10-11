#!/bin/sh

# Wait for postgres then run migrations
if [ "$DATABASE" = "postgres" ]  
then
  echo "Waiting for postgres..."
  
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do   
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

export PORT=${PORT:-5432}
# Run migrations
echo "Running migrations..."
python manage.py makemigrations --settings=mysite.settings.dev
python manage.py migrate --settings=mysite.settings.dev
# Start server
echo "Starting server..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000

exec "$@"
