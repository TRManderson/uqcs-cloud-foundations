sudo apt-get install -y postgresql nginx python3
sudo -u postgres psql -c "CREATE ROLE demo PASSWORD 'password'"
sudo -u postgres psql -c "CREATE DATABASE demo"
sudo cp nginx.conf /etc/nginx/sites-available/demo.conf
sudo ln -s /etc/nginx/sites-available/demo.conf /etc/nginx/sites-enabled/demo.conf
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip3 install -r requirements.txt supervisor
sudo bash -c "echo_supervisord_conf > /etc/supervisord/supervisord.conf"
sudo bash -c "echo files = /srv/*.conf" >> /etc/supervisord/supervisord.conf
sudo mkdir /srv
sudo cp application.py /srv/application.py
sudo cp	supervisor.conf /srv/application.conf
sudo cp supervisor.service /usr/lib/systemd/system/supervisord.service
sudo systemctl daemon-reload
sudo systemctl start supervisord
