if [ -z "$1" ]
then
  echo "Revision summary required"
  exit 1
fi

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/../src"

export FLASK_APP=main.py

flask db migrate -m "$1"
