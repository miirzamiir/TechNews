# TechNews

**TechNews** is a RESTful API designed for the backend of a technology news website. This project was developed as part of a backend internship at **Roshan** and is divided into three main challenges.

## Challenge 1: News Retrieval API

The first challenge focuses on creating a RESTful API for retrieving news articles. Each `news` record includes attributes such as `title`, `text`, `tags`, and `resource`. The following tasks were undertaken to complete this challenge:

1. **Database Model Design & Implementation:**  
   Designed and implemented the database structure to efficiently store and manage news articles.

2. **API Implementation:**  
   Developed API endpoints to create, read, update, and delete news records.

3. **Filter by Tag Feature:**  
   Added functionality to filter news articles based on specific tags.

4. **Unit Testing:**  
   Wrote unit tests to ensure the API's reliability and correctness.

### Project Setup and Initialization

The project was initiated with the following steps:

1. **Repository Creation:**  
   A new Git repository was created, and initial files such as `.gitignore` and `README.md` were added.

2. **Starting the Project:**  
   The Django project was initialized with the following command:  
   ```bash
   django-admin startproject TechNews .

3. **Adding Dependencies:**\
   A `requirements.txt` file was created to list all necessary packages for the project.

4. **Database Configuration and App Creation:**\
   After configuring the database in `settings.py`, the `news` app was created using the command:
   ```bash
   python3 manage.py startapp news

- These steps were needed in order to initiate the project. From this point, as outlined in the project document, the project will have a new branch called `ch1` and all changes related to the first challenge will be done there.
   
### Changes in Branch `ch1`
1. **Design and Implementation of models**:\
The `News` and `Tag` models were created to represent the news articles and their associated tags. The `Tag` model contains a single attribute, `tag_label`, representing the name of the `tag`. The `News` model includes the following attributes:
   - `title`: The `title` of the `news`.
   - `text`: The content of the `news`.
   - `resource`: A URL field storing the original source of the `news`.
   - `tags`: A `ManyToManyField` linking `news` to multiple `Tag` instances.

2. **Implementation of `News` and `Tags` APIs**:\
To implement these endpoints, serializers were created for each model. The `NewsSerializer` and `TagSerializer` were developed based on the defined models. These serializers were then utilized in the corresponding `viewsets`, `NewsViewSet` and `TagViewSet`, which extend `ReadOnlyModelViewSet`. This allows for efficient retrieval of news articles and tags through the API.

3. **Filtering by `tag`** :
The `NewsViewSet` now supports filtering by `tag`, implemented using the `DjangoFilterBackend` from the `django-filter` package.

4. **Writing unit tests**:
