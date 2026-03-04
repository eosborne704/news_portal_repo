# news_portal_repo
For creating a virtual environment:
1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver

For docker:
1. docker build -t news_portal .
2. docker run -p 8000:8000 news_portal
