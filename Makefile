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
	deactivate

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