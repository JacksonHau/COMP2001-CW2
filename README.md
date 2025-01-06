# COMP2001-CW2 Trail Management Microservice

Overview
This project is a microservice for managing trails as part of a larger well-being trail application. The microservice provides CRUD operations on trail data and supports secure interactions using JWT-based authentication. Users can create, read, update, and delete trail information and view trail data through a RESTful API.

Features:
Manage trails (create, read, update, delete).
JWT-based authentication for secure access.
Integration with Microsoft SQL Server for data storage.
RESTful API with endpoints documented in Swagger.
Ensures data integrity and security using appropriate constraints and validations.

Requirements
This project uses the following dependencies:

Flask==3.1.0
Flask-JWT-Extended==4.7.1
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.36
pyodbc==5.0.1
flask-swagger-ui==4.11.1
For a full list of dependencies, refer to the requirements.txt.
