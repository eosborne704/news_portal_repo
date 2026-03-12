# news_portal_repo
For creating a virtual environment:
1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver

## Using Docker Compose

1. Ensure Docker and Docker Compose are installed.
2. Configure your database connection in settings.py to use the DATABASE_URL environment variable:
	- Example: `postgres://newsuser:newspassword@db:5432/news_portal`
3. Start all services:
	- `docker-compose up --build`
4. Apply database migrations:
	- `docker-compose exec web python manage.py migrate`
5. The web app will be available at http://localhost:8000 and the database will be accessible via the `db` service name.

## Final check
- Confirm both containers stay running and http://localhost:8000 loads your app.

## Troubleshooting
- If you encounter database connection issues, ensure your Django settings use `db` as the host, not `localhost`.
- Docker Compose handles networking between containers automatically.
