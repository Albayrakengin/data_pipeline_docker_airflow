# data_pipeline_docker_airflow


# The way it works

1. `api_to_postgres.py` fetchs products data from the api and, it writes it to a postgres table.

2. Two new tables, which are product_details and ratings_table, are created

3. Transforms the data and insert it into newly created tables

# Installation

```bash
 docker-compose up
```
After it downloads all neccesary images, check if all containers are running. Then go to 'http://localhost:8080' and see if airflow-webserver is working as intented.

Then, we are going to create a connection to be able to connect postgres databases and run the PostgresOperators.

```bash
docker ps
```

Copy the id of airflow-webserver and use it on following command.

```bash
docker exec -it <airflow-webserver-container-id> bash
```

Now, we are inside of the webserver container.

```bash
airflow connections add postgres_default \
    --conn-type postgres \
    --conn-host postgres \
    --conn-login airflow \
    --conn-password airflow \
    --conn-port 5432
```

Everything is set up