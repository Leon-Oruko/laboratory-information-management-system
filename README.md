﻿# laboratory-information-management-system
LABORATORY INFORMATION MANAGEMENT SYSTEM
This is a web app that manages how personnel deal with information about samples in the laboratory.
Samples are registered by the admin and analyzed by the analyst. The analysis is viewed and recommendations and interpretations provided by the 
Agronomist. The recommendations and interpretations are issued out to the client and the client pays some fee on the service.
The web app is supposed to manage the interaction of sample information 

ROLES
Admin – Registration desk
Analyst – Analyses samples and provides analysis in the app
Agronomist – Reads through analyses and writes recommendations and interpretations
-	Oversees the roles below him
Lab Manager -Oversees the roles 
-	Processes the invoices

MODELS
Model	Fields
USERS	Username
First name 
Last name
email
password
Date joined
SAMPLES	Sample ID
Sample Name
Sample Type
Industry Type
SAMPLE REGISTERATION	Sample ID
Date of registration
Registered by
ANALYST TASKS	Sample ID
Status (Complete/Picked also incomplete)
Analysis (only for complete)
Analysis Date
Analyzed by (only for complete)
AGRONOMIST TASKS	Sample ID
Interpretation
Recommendation
LAB MANAGER TASKS	Sample ID
Status(picked/invoiced)
Invoice (only for invoiced) -pdf
Invoice date (only for invoiced)


Possible apps
Registration (Admin)
Analysis (Analyst)
Recommendations (Agronomist)
Management (Lab Manager)
Login

Features
The app can monitor real time sample registration, analysis and recommendation.
The app has permission restrictions for views only authorized access is permitted.
The lab manager can easily track sample stages and know which samples are delayed. The delayed samples are indicated using different colors.
Sample details analysis is stored until the manager wants them deleted.
Changes or records or modifications added to a sample can be traced to certain person (if a sample is registered and someone deletes it the record can be traced to the person, or if the person edited)
The app easily assigns id to the samples based on the sample type and the date and the record number as follows:
	For water sample we have  
	PS which stands for water then the date like 24 meaning 2024 and then the record positions like 01 for the first position so we have
	PS01/24
	Effluent
	EF01/24
	etc.

App tools and requirements
Framework: Django 4.2.1
Front end styling: Tailwind CSS 
Web sockets: Channels and daphne
Databases: PostgreSQL
Authentication: Django Authentication System
Deployment: PythonAnywhere
Version Control: Git
Development Environment: Python 3.11 or higher
Cache: Redis





