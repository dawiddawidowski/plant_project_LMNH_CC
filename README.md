# LNHM Plant Sensor Project
This stores the group project work for the plant project in W12.

## Entity Relationship Diagram (ERD)

The relational database used for short-term storage is in 3rd Normal Form, as the data extracted from the API is structured and there is a clear but complex relationship between the entities.

The database must be updated with a large number of frequent real-time transactional operations every minute, thus a database model favouring online transactional processing was chosen. This will provide a good balance between data integrity and flexibility.

![Alt text](erd_diagram.png)

## Architecture Diagram

![Architecture Diagram](architecture_diagram.png)

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
