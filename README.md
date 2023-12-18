# plant_project_LMNH_CC
This stores the group project work for the plant project in W12.

## Architecture Diagram

![Architecture Diagram][architecture_diagram.png]

## Assumptions Log

Extract:
- Valid plant ids in range 0-51 (higher plant id's consistently return 'plant not found' error.)
- Origin_location, image info, name and scientific names are assumed to be static.

Databases:
- Short term databases - contains only the changing data
- Long term database - contains all information, and it seeded with the static data.
  - The data from the short term database will be inserted into the long-term database every 24 hours.
