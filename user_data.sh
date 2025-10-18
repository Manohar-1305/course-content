#!/bin/bash
# Log everything to current working directory
exec > >(tee ./flask_userdata.log) 2>&1
set -xe

echo "Starting user-data script"

apt-get update -y
echo "Updated apt packages"

apt-get install -y git python3-pip python3.12-venv
echo "Installed git, pip, python3-venv"

mkdir -p /home/ubuntu/app
cd /home/ubuntu/app
echo "Created app directory"

# Clone repo first
git clone https://github.com/Manohar-1305/course-content.git
cd course-content
echo "Cloned repo"

# Create virtual environment
python3 -m venv ../venv
echo "Created virtual environment"

# Install requirements
../venv/bin/pip install --upgrade pip
echo "Upgraded pip"
../venv/bin/pip install -r requirements.txt
echo "Installed python requirements"

# Create systemd service
sudo bash -c 'cat <<EOF > /etc/systemd/system/flaskapp.service
[Unit]
Description=Flask App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/app/course-content
Environment="PATH=/home/ubuntu/app/venv/bin"
ExecStart=/home/ubuntu/app/venv/bin/python3 /home/ubuntu/app/course-content/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF'
echo "Created systemd service"

sudo chown -R ubuntu:ubuntu /home/ubuntu/app
sudo chmod -R 755 /home/ubuntu/app
echo "Set permissions"

sudo systemctl daemon-reload
sudo systemctl enable flaskapp.service
sudo systemctl start flaskapp.service
echo "Started flask service"

systemctl status flaskapp.service
echo "User-data script finished"
