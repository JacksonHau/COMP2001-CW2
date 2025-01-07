# COMP2001-CW2 Trail Management Microservice

## Overview
This project is a microservice for managing trails as part of a larger well-being trail application. The microservice provides CRUD operations on trail data and supports secure interactions using JWT-based authentication. Users can create, read, update, and delete trail information and view trail data through a RESTful API.

## Features:

- Manage trails (create, read, update, delete).
- JWT-based authentication for secure access.
- Integration with Microsoft SQL Server for data storage.
- RESTful API with endpoints documented in Swagger.
- Ensures data integrity and security using appropriate constraints and validations.

## Requirements
This project uses the following dependencies:

    Flask==3.1.0
    Flask-JWT-Extended==4.7.1
    Flask-SQLAlchemy==3.1.1
    greenlet==3.1.1
    itsdangerous==2.2.0
    Jinja2==3.1.5
    MarkupSafe==3.0.2
    pyodbc==5.0.1
    SQLAlchemy==2.0.36
    Werkzeug==3.1.3
    flask-swagger-ui==4.11.1
    marshmallow==3.19.0
    marshmallow-sqlalchemy==0.28.0
    
For a full list of dependencies, refer to the requirements.txt.

Access the Swagger documentation: 
Open your browser and navigate to http://127.0.0.1:5000/swagger.

# API Documentation:
The API is documented using Swagger. Key endpoints include:

- GET /trails: Fetch all trails.
- POST /trails: Add a new trail.
- GET /trails/read: Retrieve trails using filters.
- DELETE /trails/delete: Delete a trail.

Refer to the swagger.json file for detailed documentation of all endpoints.

## Deployment

- Use Docker for containerised deployment (refer to the Dockerfile for configuration).
