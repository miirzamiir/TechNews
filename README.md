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

- These steps were needed in order to initiate the project. From this point, as outlined in the project document, the project will have a new branch called `challenge1` and all changes related to the first challenge will be done there.
   
### Updates in Branch `challenge1`
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
Unit tests have been created for the `models`, `serializers`, and `views` within the `news` app. These tests are located in the `tests` directory. To run the tests, use the following command:
   ```bash
   python3 manage.py test
   ```
   And also to generate a coverage report for these tests, run:
   ```bash
   coverage run manage.py test && coverage html
   ```
   The coverage report will be available at `project_root/htmlcov/index.html` .

*  Also **search functionality** and **pagination** were implemented in both the `News` and `Tag` views.

- Since **Challenge 1** has been done properly, at this point branch `challenge1` will be merged into branch `master` .

## Challenge 2: Collecting News Data

The second challenge focuses on gathering news data, requiring the development of a crawler to extract information from [Zoomit](https://zoomit.ir). For this task, a new branch named `challenge2` was created.

### Updates in Branch `challenge2`

To create the crawler, it was necessary to design an appropriate architecture. **The first challenge** was deciding where to place the crawler within the project, and **the second challenge** was determining the best implementation approach.  
Given that the webpage is dynamic, I used **Selenium** for the crawling process. The crawler is located at `news/utils/zoomit_crawler.py`.

To simplify the execution of the crawler, a command was created for running the crawler. This command is implemented in `news/management/commands/crawl.py` using Django's `BaseCommand`. You can now easily run the crawler with the following command:

```bash
python3 manage.py crawl <from_page> <to_page>
```
This command will crawl the archive of [Zoomit](https://zoomit.ir). The first argument( `from_page` ) specifies the starting page, and the second argument( `to_page` ) defines the ending page.

## Pre-Challenge Modifications

To enhance the efficiency of Challenge 3, I implemented several modifications to the `News` model and the `ZoomitCrawler`. Specifically, I added a `date` field to the `News` model, which necessitated updates across various components, including:

- **NewsSerializer**: Adjusted to accommodate the new `date` field.
- **NewsModelViewSet**: Updated to ensure proper handling of the `date` attribute in API responses.
- **NewsModelTest**: Revised to include tests for the new `date` functionality, ensuring data integrity.
- **ZoomitCrawler**: Modified to utilize the `date` field when crawling news articles.

Following these changes, I introduced the `crawl_unseen_news` method within the `ZoomitCrawler`. This method iterates over the Zoomit archive, crawling news articles until it encounters one that is already stored in the database. It includes a `stop` parameter, which specifies the page number at which the crawler will cease collecting news links if no new articles are detected. This method can be executed using the following command:

```bash
python3 manage.py crawl
```

## Challenge 3: Crawler Automation and Dockerizing the Project

The third challenge centers on automating the news crawler with **Celery** and **Celery Beat**, monitoring the automated process using **Celery Flower**, and Dockerizing the entire project.

### Automation with Celery

To automate the crawler, a **Message Broker** was required. I opted for **Redis** due to its simplicity and robust performance. The steps taken include:

- **Defining Celery Tasks**: I created tasks that encapsulate the crawling logic, allowing for asynchronous execution.
- **Scheduling with Celery Beat**: I configured Celery Beat to schedule the crawling tasks at specified intervals, ensuring continuous operation.
- **Monitoring with Celery Flower**: I integrated Celery Flower to provide a real-time dashboard for monitoring task execution and performance metrics.

### Dockerizing the Project

To facilitate deployment and ensure consistency across environments, I Dockerized the project. The following steps were undertaken:

- **Creating the Dockerfile**: I wrote a `Dockerfile` to define the application environment, including dependencies and configurations.
- **Setting Up docker-compose.yaml**: This file was created to manage multi-container Docker applications, allowing for easy orchestration of services.
- **Handling Database Preparation**: To address potential latency issues during database preparation, I utilized **wait-for-it**. This script ensures that the application waits for the database to be ready before proceeding.
- **Custom Database Image**: Since the project requires a backup of the data, I created a custom `Dockerfile` for the database service rather than using the standard `postgres` image.
- **Creating docker-entrypoint.sh**: This script was developed to automate the migration process before launching the Django application, ensuring that the database schema is up-to-date.

---

Thank you for taking the time to read this document. Your feedback and insights are always welcome!
