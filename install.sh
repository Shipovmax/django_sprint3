#!/bin/bash
GREEN="\e[32m"
ENDCOLOR="\e[0m"

#git clone git@github.com:yapduser/django_sprint3.git
#cd django_sprint3

python3.9 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 blogicum/manage.py migrate
python3 blogicum/manage.py loaddata db.json
python3 blogicum/manage.py createsuperuser

echo -e "
${GREEN}****************************\nProject setup is complete.\n****************************${ENDCOLOR}
\nYou can start the server now or later by running ${GREEN}python3 manage.py runserver${ENDCOLOR}
in the project directory ${GREEN}./django_sprint3/blogicum/${ENDCOLOR}"

answer="N"
while true; do
  read -p "Start the server now [Y/N]: " answer
  case "$answer" in
  n | N | y | Y) break ;;
  esac
done

if [[ "$answer" = [yY] ]]; then
  python3 blogicum/manage.py runserver
fi
