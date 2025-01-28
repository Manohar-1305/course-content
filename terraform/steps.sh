apt-get update -y
sudo apt update -y && sudo apt install git -y
sudo apt update -y
sudo apt install python3-pip -y
mkdir /home/ubuntu/app
cd /home/ubuntu/app
sudo DEBIAN_FRONTEND=noninteractive apt install -y python3.10-venv
python3 -m venv venv
source venv/bin/activate
git clone https://github.com/Manohar-1305/course-content.git
cd course-content
pip install -r /home/ubuntu/app/course-content/requirements.txt

vi /etc/systemd/system/flaskapp.service

[Unit]
Description=flask app
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/app/course-content
Environment="PATH=/home/ubuntu/app/venv/bin"
ExecStart=/home/ubuntu/app/venv/bin/python3 /home/ubuntu/app/course-content/app.py

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable flaskapp.service
sudo systemctl start flaskapp.service
systemctl status flaskapp.service
