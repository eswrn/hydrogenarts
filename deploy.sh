#!/bin/bash
# HydrogenArts Django Deployment Script
# Usage: sudo bash deploy.sh

set -ex


PROJECT_DIR="/home/eswaran/Documents/ImageCreator"
USER="eswaran"
DOMAIN_OR_IP="192.168.0.255"  # <-- Change to your domain or server IP
GUNICORN_SOCK="$PROJECT_DIR/gunicorn.sock"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_BIN="$VENV_DIR/bin/python"
GUNICORN_BIN="$VENV_DIR/bin/gunicorn"


# 1. Install system dependencies
apt update
apt install -y python3-pip python3-venv nginx mysql-server

# 2. Set up Python virtual environment and install dependencies
cd "$PROJECT_DIR"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    pip install django mysqlclient django-widget-tweaks gunicorn
fi

# 3. Collect static files
$PYTHON_BIN manage.py collectstatic --noinput

# 4. Apply migrations
$PYTHON_BIN manage.py migrate

# 5. Create Gunicorn systemd service
cat <<EOF > /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon for HydrogenArts
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=/home/eswaran/Documents/ImageCreator/venv/bin/gunicorn --workers 3 --bind unix:/home/eswaran/Documents/ImageCreator/gunicorn.sock image_creator.wsgi:application
UMask=0007

[Install]
WantedBy=multi-user.target
EOF

# 6. Start and enable Gunicorn
systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn

# 7. Create Nginx config
cat <<EOF > /etc/nginx/sites-available/hydrogen_arts
server {
    listen 80;
    server_name $DOMAIN_OR_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias $PROJECT_DIR/static/;
    }
    location /media/ {
        alias $PROJECT_DIR/media/;
    }

    location / {
        proxy_pass http://unix:$GUNICORN_SOCK;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/hydrogen_arts /etc/nginx/sites-enabled/hydrogen_arts
nginx -t
systemctl restart nginx

# 8. (Optional) Enable HTTPS with certbot
# apt install -y certbot python3-certbot-nginx
# certbot --nginx

echo "\nDeployment complete! Visit http://$DOMAIN_OR_IP to view your site."
echo "\nRemember to set DEBUG=False and configure ALLOWED_HOSTS in settings.py for production."
echo "\nFor HTTPS, uncomment the certbot lines in this script."
