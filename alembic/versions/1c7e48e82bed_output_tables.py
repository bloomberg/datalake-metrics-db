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


output tables

Revision ID: 1c7e48e82bed
Revises: 4602433fb9dc
Create Date: 2022-05-26 14:05:27.155668

"""
from sqlalchemy import BigInteger, ForeignKeyConstraint, String
from sqlalchemy.sql.schema import Column

from alembic import op

# revision identifiers, used by Alembic.
revision = "1c7e48e82bed"
down_revision = "4602433fb9dc"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "output_columns",
        Column("queryId", String(100), primary_key=True),
        Column("catalogName", String(100), primary_key=True),
        Column("schemaName", String(100), primary_key=True),
        Column("tableName", String(100), primary_key=True),
        Column("columnName", String(100), primary_key=True),
        # Foreign Keys
        ForeignKeyConstraint(["queryId"], ["raw_metrics.query_metrics.queryId"]),
        schema="raw_metrics",
    )

    # Creating a PrimaryKey with all the columns creates a index that is too big
    # for MySQL (and possibly other databases)
    # id fields is introduced to reduce to reduce primary key size
    op.create_table(
        "output_column_sources",
        # Output column identifiers
        Column("id", BigInteger, autoincrement=True, primary_key=True),
        Column("queryId", String(100), primary_key=True),
        Column("catalogName", String(100), primary_key=True),
        Column("schemaName", String(100), primary_key=True),
        Column("tableName", String(100), primary_key=True),
        Column("columnName", String(100), primary_key=True),
        # Source column identifiers
        Column("sourceCatalogName", String(100)),
        Column("sourceSchemaName", String(100)),
        Column("sourceTableName", String(100)),
        Column("sourceColumnName", String(100)),
        # Foreign Keys
        ForeignKeyConstraint(
            ["queryId", "catalogName", "schemaName", "tableName", "columnName"],
            [
                "raw_metrics.output_columns.queryId",
                "raw_metrics.output_columns.catalogName",
                "raw_metrics.output_columns.schemaName",
                "raw_metrics.output_columns.tableName",
                "raw_metrics.output_columns.columnName",
            ],
        ),
        schema="raw_metrics",
    )


def downgrade():
    op.drop_table("output_column_sources", schema="raw_metrics")

    op.drop_table("output_columns", schema="raw_metrics")
