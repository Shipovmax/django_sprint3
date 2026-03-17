# Blogicum

## Description
Blogicum is a social platform for publishing personal diaries.
Users can create their own pages and publish messages there as posts.

## Features
- Every post belongs to a category, such as travel, cooking, or Python
  development, and can optionally reference a location.

- Users can open any category page and view all related posts.

- Users can visit other profiles, read posts, and comment on them.

- Authors can define a name and a unique address for their page.

- The platform supports moderation and blocking users who distribute spam.


## Installation and Startup

**Python version: 3.9**

Clone the repository:
```
git clone <https or SSH URL>
```

Change to the project directory:
```
cd django_sprint3
```

### Choose one of the following setup options
***
### 1. Automatic setup
Run the script and follow the prompts:
```
bash install.sh
```

***
### 2. Step-by-step setup
Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Upgrade `pip`:
```
python3 -m pip install --upgrade pip
```

Install the dependencies:
```
pip install -r requirements.txt
```

Apply migrations:
```
python3 blogicum/manage.py migrate
```

Load the database fixtures:
```
python3 blogicum/manage.py loaddata db.json
```

Create a superuser:
```
python3 blogicum/manage.py createsuperuser
```

Start the Django server:
```
python3 blogicum/manage.py runserver
```
