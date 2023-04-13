# A ComicBook Scraper Using React, Scrapy And Django

A Live Deployment is available at https://www.rhixescans.tk

## To Get Started Download the source code install all required modules and run the command to download comics locally

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py downloads
cd frontend ; npm i && npm run build ; cd .. ;
python3 manage.py collectstatic
# webapp
