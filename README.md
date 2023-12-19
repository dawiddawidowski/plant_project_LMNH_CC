# LNHM Plant Sensor Project
This stores the group project work for the plant project in W12.

## Entity Relationship Diagram (ERD)

The relational database used for short-term storage is in 3rd Normal Form, as the data extracted from the API is structured and there is a clear but complex relationship between the entities.

The database must be updated with a large number of frequent real-time transactional operations every minute, thus a database model favouring online transactional processing was chosen. This will provide a good balance between data integrity and flexibility.

![Alt text](image.png)

## Architecture Diagram

![Architecture Diagram](architecture_diagram.png)

The code to run python scripts which involve processing plant data and updating the dashboard, are hosted on Dockerised containers on an ECS as a service. This ensures the dashboard/extracting data is always running, regardless if the Task definition fails at any stage. 

Long-term storage solution is AWS S3, as it is an easy, scalable and cost-effective way to store the long term data. The data is stored in CSV-format with the CSV file containing all the data collated in previous 24 hours, which comes from short-term RDS storage. AWS Eventbridge provides an easy way to trigger this every 24 hours, whilst a Lambda function is chosen to implement this transfer, as it is lightweight and relatively infrequent.


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
- Soil moisture and temperature were rounded to 2dp and 1dp respectively.
- Any rows which contain an error regardless of the type of error is removed from data

- All valid data will be stored in long-term S3 bucket and not omitted, due to potential change of requirements in the future. 