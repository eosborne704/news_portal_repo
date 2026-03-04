# news_portal_repo
For creating a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

For docker:
docker build -t news_portal .
docker run -p 8000:8000 news_portal
