export DATABASE=postgres
export FLASK_APP=main.py
cd server/src
flask db upgrade
gunicorn main:app -b 0.0.0.0:8000 -w 4
