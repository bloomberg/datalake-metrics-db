# #!/bin/bash

# # Create the DB & run the initial schema
mysql -u root -e "CREATE DATABASE datalake_analytics;"
mysql -u root -e "CREATE SCHEMA raw_metrics;" datalake_analytics
