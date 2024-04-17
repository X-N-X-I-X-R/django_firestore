

# color codes menu  - https://misc.flogisoft.com/bash/tip_colors_and_formatting
# \033[0;30m - Black
# \033[0;31m - Red
# \033[0;32m - Green
# \033[0;33m - Yellow
# \033[0;34m - Blue
# \033[0;35m - Magenta
# \033[0;36m - Cyan
# \033[0;37m - White




# phonty targets are not files but commands that are not associated with files in the file system 
.PHONY: runserver makemigrations migrate createsuperuser freeze install requirements virtualenv env python-decouple dec.env source env/bin/activate runenv deactivate killenv gitremove rm-rf gitdelete djangomongo djangofirebase django-mongodb-engine



rund:
	# Run the Django development server
	python manage.py runserver &
	clear

mig:
	# Create new migrations based on the changes detected to the models
	python manage.py makemigrations

migrate:
	# Apply the migrations to the database
	python manage.py migrate

super:
	# Create a superuser
	python manage.py createsuperuser

freeze:
	# Freeze the current environment's dependencies to a requirements.txt file
	pip freeze > requirements.txt

install-r:  
	# Install the requirements from the requirements.txt file
	pip install -r requirements.txt

envi:
	# Create a virtual environment
	virtualenv env

decouple:
	# Install the python-decouple package
	pip install python-decouple

envr:
		# Activate the virtual environment	
	source env/bin/activate

envk:
    # Deactivate the virtual environment
	@echo "To deactivate the virtual environment, run 'deactivate' in your shell."

gitremove:
	# Remove the .git folder and all its contents from the current directory and all subdirectories recursively 
	git rm --cached .env

remove.git: 
	# Remove the .git folder and all its contents from the current directory and all subdirectories recursively 
	rm -rf .git


	
dmongo:
	pip install django-mongodb-engine

djangofirebase:
	pip install django-firebase-orm



#	@printf "\033[0;32m%s\033[0m\n" "YES MY KING !" "running the Django development server"
# Run the Django development server






Django:

Django==5.0.3
django-cors-headers==4.3.1
django-firebase-orm==0.6.1
django-mongodb-engine==0.6.0
django-rest-swagger==2.2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
djangotoolbox==1.8.0
Flask:

Flask==3.0.1
Web Scraping:

beautifulsoup4==4.12.3
requests==2.31.0
urllib3==1.26.18
API Clients:

google-api-python-client==2.124.0
polygon-api-client==1.13.4
Authentication:

PyJWT==2.8.0
firebase-admin==6.5.0
Database:

pymongo==4.6.3
SQLAlchemy==2.0.29
Development Tools:

click==8.1.7
Werkzeug==3.0.1
Others:

Jinja2==3.1.3 (templating engine)
Pillow==10.2.0 (image processing)
cachetools==5.3.3 (caching)