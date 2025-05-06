Full Web Application Deployment on AWS – Final Project
By: [Your Name]
Overview
This project demonstrates the deployment of a full-stack web application using Amazon Web Services (AWS). The application connects a static frontend hosted on Amazon S3 with a backend server running on Amazon EC2 that interacts with a PostgreSQL database hosted on Amazon RDS.

The application supports:

Displaying static HTML content

Performing Add and Delete operations

Real-time interaction with the PostgreSQL database

Tech Stack
Frontend: HTML, CSS, JavaScript (hosted on Amazon S3)

Backend: Python (Flask)

Database: PostgreSQL (Amazon RDS)

Hosting/Compute: Amazon EC2 (Ubuntu)

Project Components
Amazon RDS - PostgreSQL

Database name: db_<your_first_name>

Table name: tbl_<your_first_name>_<dataset_name>

Dataset imported from Kaggle and uploaded using DBeaver or psql

Amazon S3 - Static Website

S3 bucket hosts index_<your_first_name>.html

Public access configured via S3 bucket policy

UI includes "Add" and "Delete" buttons linked to backend

Amazon EC2 - Backend App

Hosted Flask application (app.py)

Connected to RDS using psycopg2

Handles /add and /delete requests

How to Run the Application
Frontend (Static Website)
Open the link below in a browser:
S3 Static Website Link

Backend (Flask API)
Access the backend hosted on EC2:
EC2 Public IP or Domain

Database (Amazon RDS)
PostgreSQL running on RDS is not publicly browsable but is accessible by the EC2 instance.

Add/Delete Functionality
Add Button: Sends data to EC2 backend → Inserts into RDS table

Delete Button: Sends request to EC2 backend → Deletes from RDS table

All changes are reflected live in the database.

Links
GitHub Repo: GitHub Repository Link

S3 Static Hosting: Static Website URL

EC2 Backend App: EC2 Public IP

Deployment Folder Name
Project folder is named:
webapp_<your_first_name>
