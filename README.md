# TechNews

**TechNews** is a RESTful API developed for the backend of a technology news website. This project was undertaken as part of a backend internship at **Roshan** and is organized into three main challenges.

## Challenge 1: News Retrieval API

The first challenge involves creating a RESTful API to retrieve news articles. Each `news` record includes essential attributes such as `title`, `text`, `tags`, and `resource`. To successfully complete this challenge, the following tasks were carried out:

1. **Database Model Design & Implementation:**  
   Designing and implementing the database structure to efficiently store news articles.

2. **API Implementation:**  
   Developing the API endpoints to create, read, update, and delete news records.

3. **Filter by Tag Feature:**  
   Adding functionality to filter news articles based on specific tags.

4. **Unit Testing:**  
   Writing unit tests to ensure the reliability and correctness of the API.

### Project Setup and Initialization

To initiate the project, the following steps were taken:

1. **Repository Creation:**  
   A new Git repository was created, and initial files like `.gitignore` and `README.md` were added.

2. **Starting the Project:**  
   The Django project was initialized using the command:  
   ```bash
   django-admin startproject TechNews .

3. **Adding Dependencies:**\
   A `requirements.txt` file was created to list all necessary packages for the project.

4. **Database Configuration and App Creation:**\
   After configuring the database in `settings.py`, the `news` app was created using the command:
   ```bash
   python3 manage.py startapp news

- These steps were needed in order to initiate the project. From this point, as it was asked in the project document, the project will have a new branch called `ch1` and all changes related to the first challenge will be done there.
   
