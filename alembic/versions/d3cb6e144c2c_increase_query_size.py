"""
 ** Copyright 2021 Bloomberg Finance L.P.
 **
 ** Licensed under the Apache License, Version 2.0 (the "License");
 ** you may not use this file except in compliance with the License.
 ** You may obtain a copy of the License at
 **
 **     http://www.apache.org/licenses/LICENSE-2.0
 **
 ** Unless required by applicable law or agreed to in writing, software
 ** distributed under the License is distributed on an "AS IS" BASIS,
 ** WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 ** See the License for the specific language governing permissions and
 ** limitations under the License.


increase query size

Revision ID: d3cb6e144c2c
Revises: 1c7e48e82bed
Create Date: 2022-08-23 10:00:40.375381

"""
from sqlalchemy import String, Text

from alembic import op

# revision identifiers, used by Alembic.
revision = "d3cb6e144c2c"
down_revision = "1c7e48e82bed"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "query_metrics", "query", existing_type=String(10_000), existing_nullable=True, type_=Text, schema="raw_metrics"
    )


def downgrade():
    op.alter_column(
        "query_metrics", "query", existing_type=Text, existing_nullable=True, type_=String(10_000), schema="raw_metrics"
    )
