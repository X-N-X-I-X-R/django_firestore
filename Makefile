.PHONY: runserver makemigrations migrate createsuperuser freeze install requirements virtualenv env python-decouple dec.env source env/bin/activate runenv deactivate killenv gitremove rm-rf gitdelete djangomongo djangofirebase django-mongodb-engine

runserver:
	python manage.py runserver  

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser

freeze:
	pip freeze > requirements.txt

install:  # Combined functionality of freeze and install for clarity
	pip install -r requirements.txt

virtualenv env:
	virtualenv env

python-decouple:
	pip install python-decouple

dec.env:  # Removed unnecessary space before `=`
	pip install python-decouple

source env/bin/activate:
	source env/bin/activate

deactivate:
	deactivate

gitremove:
	git rm --cached .env

rm-rf:  # Removed unnecessary line break
	rm -rf .git

djangomongo:
	# Consider alternatives due to `django-mongodb-engine`'s limitations
	echo "WARNING: django-mongodb-engine is not actively maintained and has limitations. Consider using Djongo or MongoEngine for a more robust solution."
	pip install django-mongodb-engine  # Install if still desired

djangoengie:
	pip install django-mongodb-engine

djangofirebase:
	pip install django-firebase-orm
