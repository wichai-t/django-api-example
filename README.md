# API School & Students example

Hi! this is my example School & Students API using **Django Rest Framework (DRF)**.
It focuses on simplicity and practically implementation.

# Try it!

[https://school-demo.wichai.site](https://school-demo.wichai.site/)

# Test
All test cases are inside `school_manager/tests` directory.  
Run all tests using `python manage.py test`

# Deployment

You can deploy the app on system environment or a docker environment.  
**NOTE:** The Postgis is required on your system.

## Docker

To build a docker image and run the container, follows these steps:  
1. Clone or download this repo.  
`$ git clone git@github.com:wichai-t/django-api-example.git`
2. Set secrets and other configs in the `.env` file.
3. Build the image.  
`$ docker build -t school_man:latest -f Dockerfile .`
4. Run a container.  
`$ docker run  --name myschoolman -p 8080:8000 school_man`  

Then check the result on the web site: [127.0.0.1:8080](http://127.0.0.1:8080/)


## Working log

Here is the working log as I am writing this project:

|  Date  |    Task       |    Detail             |
|-----------|----------------------|-------------------|
|Sat, 15 Jan 22|  Setting up the project   | <ol><li>Create a Django app, with:<ul><li>Postgres as a database</li> <li>Pipenv as a Python dependency manager.</li> <li>Environment file (for sensitive information, etc.)</li> </li></ul><li>Add models to create the following structure: <ul><li> Students have a first name, a last name, and a student identification string (20 characters max for each)</li> <li>Schools have a name (20 char max) and a maximum number of student (any positive integer)</li> <li>Each student object must belong to a school object</li> </li></ul></li><ol>    |
|      | Implementing **Django Rest Framework (DRF)** support  |Make sure the API is following these:<br><ul><li>Endpoint `/students/` will return all students (GET) and allow student creation (POST)</li> <li>Endpoint `/schools/` will return all schools (GET) and allow school creation (POST) </li> <li> Endpoint `/schools/:id` and `/students/:id` will return the object by :id (GET) and allow editing (PUT/PATCH) or deleting (DELETE) </li> <li>Student creation will generate a unique identification string </li> <li>If maximum number of student in a school reached, it will return a DRF error message</li></ul>      |
|Sun, 16 Jan 22          | Implementing the **Django Nested Routers** support            | Install the `Django Nested Routers` and Make sure the API is following these:<br><ul><li>Endpoint `/schools/:id/students` will return students who belong to school :id (GET)</li> <li>Endpoint `/schools/:id/students` will allow student creation in the `school :id` (POST)</li> <li> Config the endpoint to allow GET/PUT/PATCH/DELETE methods on `/schools/:id/students/:id`</li> <li>Config the endpoint to respect the same two last rules of the above detail</li></ul>           |
|          |Improve readability | <ul><li>Make the code tidier</li> <li> Writing docstring</li> <li>and this README.md</li></ul>|
|          | Add all test cases |  Inside the `school_manager/tests` directory.|
|          | Modify some features | <ul><li>Add some fields to the models: education stage to Student and location (Postgis lat, lon) to Schools</li> <li>Add search and ordering filters to the endpoints such as `/students/?search=jeremy&ordering=first_name`</li> <li>Make admin's url configurable via the env file</li> <li>Config Limit-Offset style pagination</li></ul> |
|Mon, 17 Jan 22    | Implement the JWT authentication API support     | Install the `djangorestframework-jwt` and config its routes  |
|   | Dockerize the application  | Add Dockerfile to project |
|   | Deploy  | Deploy the project on [https://school-demo.wichai.site](https://school-demo.wichai.site/) |
|   | Generate example data  | <ul><li> Create a demo data generator fn inside the tests dir </li> <li>Generate example data on the site</li></ul> |
|   | Add home page  | Simple json response, which shows our API urls |