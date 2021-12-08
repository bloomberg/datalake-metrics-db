# Copyright 2021 Bloomberg Finance L.P.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash

# Create the DB & run the initial schema
psql -c "CREATE user datalake_analytics_admin with login password 'foobar';"
psql -c "CREATE user raw_metrics_rw with login password 'foobar';"
psql -c "GRANT raw_metrics_rw to datalake_analytics_admin;"
psql -c "CREATE DATABASE datalake_analytics with owner datalake_analytics_admin;"
psql -U datalake_analytics_admin -c "Create schema raw_metrics authorization raw_metrics_rw;" datalake_analytics
