# Reddit API Pipeline
![Python](https://img.shields.io/badge/python-35c4cb?style=for-the-badge&logo=python&logoColor=black&logoSize=auto)
![SQL](https://img.shields.io/badge/sql-orange?style=for-the-badge&logo=postgresql&logoColor=black&logoSize=auto)
![Airflow](https://img.shields.io/badge/airflow-cb3557?style=for-the-badge&logo=apacheairflow&logoColor=black&logoSize=auto)
![AWS](https://img.shields.io/badge/AWS-purple?style=for-the-badge&logo=amazonwebservices&logoColor=black&logoSize=auto)
![Docker](https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker&logoColor=black&logoSize=auto)
![Terraform](https://img.shields.io/badge/Terraform-623CE4?style=for-the-badge&logo=terraform&logoColor=black&logoSize=auto)
![Looker](https://img.shields.io/badge/Looker-white?style=for-the-badge&logo=looker&logoSize=auto)

This is my study project focused on learning data engineering stack. The project creates an efficient pipeline to extract data from any subreddits on Reddit for downstream consumption.

## Project overview
![Project diagram](/img/diagram.png) 
This project automates the extraction and storage of data from Reddit API using a Python application orchestrated by Apache Airflow and deployed within Docker containers.
1. **Docker** manages the isolated environment for Apache Airflow and the data pipeline.
2. **Apache Airflow** schedules and manages the data extraction pipeline, triggering the Python application to fetch data from the Reddit API at regular intervals.
3. **The Python application** retrieves data from Reddit by utilizing [PRAW](https://praw.readthedocs.io/en/stable/) and processes it into a structured format.
4. The processed data is then uploaded to a **PostgreSQL** database using a AWS RDS service for storage, managed by Terraform for infrastructure provisioning.

## Prerequisites and Setup
### Prerequisites
- A Reddit account to access the API
Visit this [page](https://www.reddit.com/prefs/apps) to create an app and get your API key
- An AWS account with needed permissions
- Terraform + Docker already installed on your machine
### Setup
1. Fork Clone this repository
2. Create `/terraform/variable.tf` to store your Terraform variables
```
variable "aws_access_key" {
    default = "your access key" 
}
variable "aws_secret_key" {
    default = "your secret key"
}
variable "aws_region" {
    default = "your region"
}
variable "rds_username" {
    default = "your username"
}
variable "rds_password" {
    default = "your password"
}
```
3. Initialize AWS RDS service using Terraform
```
cd terraform
terraform init
terraform apply 
```
4. Create a `.env` to store environment variables for Airflow container.
Below is the list of the variables that you need to configure in `.env`, these can be found on the Reddit developer page and in the Terraform state file:
```
AIRFLOW_UID=50000
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
RDS_PORT=
RDS_HOST=
RDS_USERNAME=
RDS_PASSWORD=
RDS_DATABASE=
```
5. Initialize Airflow. The detailed instruction on how to run Airflow using Docker-compose can be found on [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
```
mkdir -p ./logs ./plugins
docker compose up airflow-init
```
6. Finally, you can start the pipeline and let Airfow handles the orchestration:
```
docker-compose up
```

## Configuration
### API configuration
A subreddit is a specialized community within the website Reddit. Each subredit is dedicated to a specific topic, interest, or theme where users can post content and engage in discussions. In this project, I am going to collect data about popular MMORPG games on the market as an example.
You can set the subreddits that you want to extract in `/dags/extract.py`
```
subreddits = ['ffxiv', 'Guildwars2', 'blackdesertonline']
```
The engine collects recent posts and filters out the unnecessary data based on date. The `limit` variable in `/dags/extract.py` controls how many posts the engine searchs. If this is set to 100, 100 most recent posts will be collected.
Depending on the popularity of the subreddits, you might want to adjust this value accordingly. Setting `limit` too high can impact the performance, while setting it too low may result in potential data lost. For subreddits with an average of more than 100 posts per day, consider setting limit to 200.
```
limit = 200
```
### Terraform
This project uses AWS RDS because of the [AWS free tier](https://aws.amazon.com/free/). If you want to have a better performance, you can change this to a different AWS database resource in `/terraform/main.tf`:
```
resource "aws_db_instance" "rds_postgres" {
    engine = "postgres"
    engine_version = "14.13"
    instance_class = "db.t3.micro"
}
```
### Docker
Docker is used to manage Airflow in this project. Since this is a small-scale setup, the project uses `LocalExecutor` instead of the default `CeleryExecutor`:
```
AIRFLOW__CORE__EXECUTOR: LocalExecutor
```
As a result, all Celery dependencies have been removed from the `docker-compose.yaml` to speed up the installation process.
If you need to use `CeleryExecutor`, you can create your own docker-compose based on the offical [docker-compose.yaml from Apache Airflow](https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml).
### Airflow
To customize the schedule of your DAG, edit the `schedule_interval` parameter in /dags/dag.py. By default, the DAG is set to run at 9:00 AM every day:
```
schedule_interval = '0 9 * * *'
```
Refer to the [Apache Airflow scheduling documentation](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/cron.html) for more examples and details on `schedule_interval`.

## Sample data
![Looker image](/img/data.png)
This section illustrates the potential final data format. Data is visualized using Google Looker Studio, providing insights into Reddit activity across multiple gaming subreddits.
You can explore the full interactive report with additional data filters [here](https://lookerstudio.google.com/s/v_t8-oGcJaM).
