#!/bin/bash

echo '
DATABASE_ENGINE=postgresql
DATABASE_NAME=rhixescans
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=Rhixe&company@1
DATABASE_HOST=
DATABASE_PORT=5432
HOST=smtp.mailtrap.io
HOST_USER=
HOST_PASSWORD=
PORT=2525
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY= 
' > .env

sudo apt update && sudo apt install python3-pip git ufw micro python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl nodejs npm  -y 
sudo ufw allow 'Nginx Full' && sudo ufw allow 'OpenSSH' && sudo ufw enable

sudo gpasswd -a www-data bot && echo 'www-data user Profile Created !'

sudo chmod g+x /home/bot  && sudo chmod g+x /home/bot/rhixescans && sudo chmod g+x /home/bot/rhixescans/static && sudo chmod g+x /home/bot/rhixescans/media && sudo chmod g+x /home/bot/rhixescans/frontend/build && echo 'www-data user Permission set Successfully !!' ;
sudo mv rhixescans.service /etc/systemd/system && sudo mv rhixescans.socket /etc/systemd/system  && sudo mv rhixescans.conf /etc/nginx/sites-available/ && sudo systemctl enable rhixescans.socket rhixescans.service nginx && sudo systemctl start rhixescans.socket rhixescans.service nginx && sudo systemctl status rhixescans.socket rhixescans.service nginx && echo 'Server Configure Successfully' ;

