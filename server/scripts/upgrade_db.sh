cd server/src

# core db
export FLASK_APP=main.py

flask db upgrade
