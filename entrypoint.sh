# This file is changed from CRLF to LF, to avoid the /r issue for new line https://stackoverflow.com/questions/64083660/how-do-i-replace-r-line-endings-when-running-docker-script-on-windows#_=_

# Collect static files
echo "Collect static files"
python bookstore_api/manage.py collectstatic --noinput

echo "Apply database migrations"
python bookstore_api/manage.py migrate

# Create Superuser
echo "Creating superuser"
python bookstore_api/manage.py createsuperuser --noinput

# Generate groups
echo "Generate groups"
python bookstore_api/manage.py populate_groups

# Start server
echo "Starting server"
python bookstore_api/manage.py runserver 0.0.0.0:8000