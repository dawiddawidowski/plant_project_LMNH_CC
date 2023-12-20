# LNHM Plant Sensor Project
This stores the group project work for the plant project in W12.

## Architecture Diagram

The main ETL pipeline Python script extracts data from the plant API, cleans the data, and loads the data into the database. The script is Dockerised and ran as a continuous service on AWS ECS. The aim here is to monitor the plant health as close to every minute as possible. If one iteration of passing data through the pipeline takes longer than one minute (largely due to response times in communicating with the API), then the next iteration begins immediately. Otherwise, if the current iteration takes less than one minute to complete, the next iteration begins after one minute has passed from the start of the current iteration.

Our chosen long-term storage solution is AWS S3, as it is an easy, scalable and cost-effective way to store the plant health data long-term. The data is stored in CSV-format with the CSV file containing all the data collated in the previous 24 hours, which comes from short-term RDS storage. AWS EventBridge provides an easy way to trigger this every 24 hours, whilst a Lambda function is chosen to implement this transfer, as it is lightweight and relatively infrequent.

In addition to the pipeline, the Python script running a Streamlit dashboard is configured as a continuous service on ECS. The script connects to the database and utilises the data contained in the database to create visualisations which provide insights into the health of each plant in the museum at any given moment.

![Architecture Diagram](architecture_diagram.png)

## Entity Relationship Diagram (ERD)

The relational database used for short-term storage is in 3rd Normal Form, as the data extracted from the API is structured and there is a clear but complex relationship between the entities.

The database must be updated with a large number of frequent real-time transactional operations every minute, thus a database model favouring online transactional processing was chosen. This will provide a good balance between data integrity and flexibility.

The static data from the API is seeded into the database tables upon their creation using a CSV containing a complete dataset of the static information. The tables seeded are the origin, botanist, license, image and plant tables.

This approach increases the speed of pipeline by allowing it to only process the dynamic data to insert into the reading table.

![Alt text](erd_diagram.png)

## Assumptions Log

Extract:
- Valid plant ids in range 0-51 (higher plant id's consistently return 'plant not found' error.)
- Origin_location, image info, name and scientific names are assumed to be static.

- The database is hard-coded with static values, which applies to the following databases:
  - Botanist
  - Plant
  - License
  - Origin
  - Image

- Transient values are added to the database, for each plant, every minute
- Only data extracted within the last 24 hours is held in the database and used for the dashboard.
- After 24 hours, the data is stored in an S3 bucket and the database is wiped.

Transform:
- Soil moisture and temperature have a precision of 2 decimal places.
- Any rows which contain an error regardless of the type of error is removed from data

- All valid data will be stored in long-term S3 bucket and not omitted, due to potential change of requirements in the future.
