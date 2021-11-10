#!/bin/bash

# Create the DB & run the initial schema
psql -c "CREATE user datalake_analytics_admin with login password 'foobar';"
psql -c "CREATE user raw_metrics_rw with login password 'foobar';"
psql -c "GRANT raw_metrics_rw to datalake_analytics_admin;"
psql -c "CREATE DATABASE datalake_analytics with owner datalake_analytics_admin;"
psql -U datalake_analytics_admin -c "Create schema raw_metrics authorization raw_metrics_rw;" datalake_analytics
