# megadados-dpa-2021.1

Projeto FAST API - megadados

## Create db and set configs to SQLAlchemy

First execute:
create_db.sql to create the database

Then, you'll need to set some env vars to your system:
MEGADADOS_APS_USER -> Stores the MySQL User
MEGADADOS_APS_USER_PASSWORD -> Stores the MySQL Users's password
MEGADADOS_APS_SERVER -> Stores the Server (generally localhost)
MEGADADOS_APS_DB -> Stores the Database name (Need to create it with the script provided at /create_db.sql)

## Run application command

At megadados-dpa-2021.1 run:
uvicorn sql_app.main:app --reload
