# Readme file to be updated

#meHungry
---

meHungry is a the software project started by IIT students to implement private bidding process for bars and restaurants. 

#####You can find bitbucket repo [here](https://bitbucket.org/agyu/project-x).


##Initialization

The project setting up is influenced by a online video: 

Setting up a Django Project Part 1 (setup) : [Video](https://www.youtube.com/watch?v=D0MoGRZRtcA)  [Live App](http://realdjango.herokuapp.com)


##What you need for a basic dev environment:
 1. Python 2.7.x
 2. Git 1.7/1.8/1.9
 3. virtualenv
 4. Django
 5. Mysql Database (If you need to run on your local machine.)
 
You do not need to go through the entire setting up process. All file can be pulled from bitbucket repo at [here](https://bitbucket.org/agyu/project-x).

###virtualenv(Not required, but recommended)
It is common (I heard) to use virtualenv (virtual environment) for Python projects , which will create a self-contained developing envoriments (known as 'sandbox').

Install virtualenv with the following command(OSX/Linux):
	
	$ : pip install virtualenv

If it shows a **permission denied** error, try with:
	
	$ : sudo pip install virtualenv
	
Set up development structure:
	
	$ : cd project-x
	$ : virtualenv --no-site-packages virtual_env

###Database
We will use MySQL as database.

First, install MySQL from [here](http://dev.mysql.com/doc/refman/5.7/en/installing.html).

Next, start the server and create a new database for a user:

	$ : mysql.server start
	$ : mysql -u root -p
	Enter password:(Default password is empty, just click enter)
	
	mysql> CREATE DATABASE proj_db;
	mysql> SHOW databases;
	+--------------------+
	| Database           |
	+--------------------+
	| proj_db            |
	+--------------------+
	mysql> quit
	Bye
	$ :
	
Install python supporting for MySQL:
	
	$ : pip install MySQL-python

FOR WINDOWS: if you run into errors like the following:
	error: Microsoft Visual C++ 9.0 is required (Unable to find vcvarsall.bat). Get
	it from http://aka.ms/vcpython27
	error: 'PATH/cl.exe' failed with exit status 2

Use this link to install with an executable
http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python

###Django

#####Install (Required)
This step will get Django installed to the working directory , for Project X, which is :
	
	$ (virtualenv) : cd project-x
	$ (virtualenv)project-x : pip install django
	
#####Set up Django
Go to the root directory the project:
	
	$ (virtualenv)cd project-x
	$ (virtualenv)project-x : django-admin.py startproject proj_site

This will create a directory called *proj_site* under the root directory.



##How to run the code
Now, the project basic structure is:
	
	project-x
		|-----proj_site
		|		|-----manage.py
		|		|-----proj_site
		|				|-----__init__.py
		|				|-----settings.py
		|				|-----urls.py
		|				|-----wsgi.py
		|-----virtual_env
		|		|-----(virtual_env files)
		|-----requirements.txt
		|-----READMD.MD
Start MySQL service by entering:

	$ : mysql.server start

Make sure virtualenv has been activated:
	
	$ project-x : source virtual_env/bin/activate

If this is the first time to start this project, the following step is required:

	$ project-x : pip install -r requirements.txt

Then enter the following code to launch the development server:
	
	$ project-x/proj_site : python manage.py runserver



##Team

---

#####Alex Yu:

* Bitbucket username: [agyu](https://bitbucket.org/agyu) 
* Email:<alexgxiyu@gmail.com>

#####Bharat Lavania:
* Email:<blavania@iit.edu>

#####Jay Zheng:  
* Bitbucket username: [JaySurplus](https://bitbucket.org/JaySurplus) 
* Email:<znznbest2004@gmail.com>

#####Pranay Kumar: 
* Bitbucket username: [pkumar6](https://bitbucket.org/pkumar6)
* Email:<pranay112@gmail.com>
* Phone # - 312-613-5680
#####Siddharth Ravikumar: 
* Email:<ravikumar.siddharth@gmail.com>


version 0.1.5
