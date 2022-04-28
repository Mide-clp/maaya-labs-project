# maaya-labs-project

## Objective 

The objective of this project was to build an efficient and reuseable data pipeline, that helps maaya labs load data into their ad hoc database so the visualization software can automatically pull data from the database into the dashboard.
## ETL data pipeline 

### The process 

`Extract` - Get data from csv files 

`Transform`- Select the necessary columns, rename columns, and change data type 

`Load`- Insert the data into a relational data base

### Tools used 
`Pandas`: for transformation and cleaning 

`Postgres`: relational database

`Apache superset`: data visualization dashboard 

### Schema

**Database** - `company_x `

There are `two tables` in the database:

`General_dashboard`: This contains all user transactions, ranging from the source of traffic to quantity of product bought and total amount spent daily. 

**Schemas**: <br>
`Table name: general_dashboard` 

*columns* <br>
`id SERIAL: PRIMARY KEY` <br>
`date: TIMESTAMP WITHOUT TIME ZONE `<br>
`source: TEXT`  <br>
`sessions: BIGINT` <br>
`organic_searches: BIGINT` <br>
`users: BIGINT` <br>
`transactions: BIGINT` <br>
`transaction_revenue: FLOAT(53)` <br>
`item_quantity: BIGINT` <br>
`transactions_per_user: FLOAT(53)`

<br>

`Publisher`: this contains data about the platform used for running ads, and how much was spent on each platform daily 

**Schemas** <br>

`Table name: publisher` 

*columns* <br>
`date: TIMESTAMP WITHOUT TIME ZONE` <br>
`publisher_platform: TEXT` <br>
`spend: FLOAT(53)`


### Setup

**From your *terminal/bash/cli*** 
- run `mkdir maaya_labs_data`
- To build docker image **run** `docker build -t maaya-labs .`
- Run `docker-compose -f docker-compose.yaml` to start the postgres database and run scripts

### Visualization

Install **[Apache superset](https://superset.apache.org/docs/installation/installing-superset-using-docker-compose)** using docker

sample visualization

**Channel breakdown of spend per ad platform**
<img src="doc/channel_breakdown_spend.png">
<br>

**Channel level breakdown of website orders**
<img src="doc/channel_breakdown_website_orders.png">
<br>

**Channel level breakdown of revenue**
<img src="doc/Channel_level_breakdown_revenue.png">
