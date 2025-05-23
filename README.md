## Web Application Deployment on AWS
This project demonstrates a complete web application deployment using AWS services, including EC2 for compute, RDS for database management, and S3 for static content hosting.
Project Overview
This application provides a user interface to interact with a dataset from Kaggle, allowing users to view, add, and delete data through a web interface. The architecture employs a three-tier design:

Frontend: Static HTML/CSS/JS files hosted on Amazon S3
Backend: Application server running on Amazon EC2
Database: PostgreSQL database on Amazon RDS

## AWS Resources

S3 Bucket: s3://noila1t - Hosts static website content
EC2 Instance: webapp_noila - Runs the application server
RDS Database: db-noila.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com - PostgreSQL database instance

## How to Run the Application
1. Access the Web Application
The application can be accessed at: http://noila1t.s3-website.ap-northeast-2.amazonaws.com
2. Using the Application

## Browse Data: The homepage displays data from the Kaggle dataset
Add Data: Click the "Add" button to insert new records into the database
Delete Data: Click the "Delete" button to remove records from the database

3. Backend API Endpoints

GET /api/data: Retrieves all records from the database
POST /api/data: Adds a new record to the database
DELETE /api/data/{id}: Deletes a record from the database

## Project Setup
Database Setup (Amazon RDS)

Created a PostgreSQL database instance on Amazon RDS
Database name: db_noila
Table name: tbl_noila_supermarket_sales
Imported dataset from Kaggle into the RDS database

## Static Website (Amazon S3)

Created S3 bucket configured for static website hosting
Uploaded HTML/CSS/JS files to the bucket
Main HTML file: index_noila.html
Set bucket policy for public access

## Application Server (Amazon EC2)

Launched Ubuntu EC2 instance
Installed necessary dependencies (Python/Flask)
Deployed backend application connecting to RDS database
Project folder: webapp_noila

## Technologies Used

Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
Database: PostgreSQL
AWS Services: EC2, RDS, S3

## Project Structure
webapp_noila/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── static/                # Static files (copied to S3)
│   ├── css/
│   ├── js/
│   └── index_noila.html
├── templates/             # Flask templates
└── scripts/               # Database import scripts
Development and Deployment Notes

## Database connection string is configured in the application
Application automatically connects to RDS on startup
Static files are served directly from S3
EC2 instance hosts only the API endpoints
