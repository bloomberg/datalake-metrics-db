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


379 add more tables

Revision ID: d58a144ae68f
Revises: 5951554f7954
Create Date: 2022-05-05 10:21:10.881234

"""
from sqlalchemy import JSON, BigInteger, Float, String, UnicodeText
from sqlalchemy.sql.schema import Column, ForeignKey

from alembic import op

# revision identifiers, used by Alembic.
revision = "d58a144ae68f"
down_revision = "1670737c6856"
branch_labels = None
depends_on = None


def upgrade():

    for column in [
        # Statistics columns
        Column("failedCpuTime", Float, nullable=True),
        Column("failedScheduledTime", Float, nullable=True),
        Column("inputBlockedTime", Float, nullable=True),
        Column("failedInputBlockedTime", Float, nullable=True),
        Column("outputBlockedTime", Float, nullable=True),
        Column("failedOutputBlockedTime", Float, nullable=True),
        Column("processedInputBytes", BigInteger, nullable=True),
        Column("processedInputRows", BigInteger, nullable=True),
        Column("planNodeStatsAndCosts", JSON(none_as_null=True), nullable=True),
        # Metadata
        Column("uri", String(255), nullable=True),
        Column("plan", UnicodeText, nullable=True),
        Column("paylod", JSON(none_as_null=True), nullable=True),
        # Context
        Column("sessionProperties", JSON(none_as_null=True), nullable=True),
    ]:
        op.add_column("query_metrics", column, schema="raw_metrics")

    op.create_table(
        "client_tags",
        Column(
            "queryId",
            String(100),
            ForeignKey("raw_metrics.query_metrics.queryId"),
            primary_key=True,
        ),
        Column("clientTag", String(255), primary_key=True),
        schema="raw_metrics",
    )

    op.create_table(
        "resource_groups",
        Column(
            "queryId",
            String(100),
            ForeignKey("raw_metrics.query_metrics.queryId"),
            primary_key=True,
        ),
        Column("resourceGroup", String(255), primary_key=True),
        schema="raw_metrics",
    )

    op.create_table(
        "operator_summaries",
        Column("id", BigInteger, autoincrement=True, primary_key=True),
        Column(
            "queryId",
            String(100),
            ForeignKey("raw_metrics.query_metrics.queryId"),
            primary_key=True,
        ),
        Column("operatorSummary", JSON(none_as_null=True), nullable=False),
        schema="raw_metrics",
    )


def downgrade():

    for column in [
        "failedCpuTime",
        "failedScheduledTime",
        "inputBlockedTime",
        "failedInputBlockedTime",
        "outputBlockedTime",
        "failedOutputBlockedTime",
        "processedInputBytes",
        "processedInputRows",
        "uri",
        "plan",
        "payload",
        "planNodeStatsAndCosts",
        "sessionProperties",
    ]:
        op.drop_column("query_metrics", column, schema="raw_metrics")

    op.drop_table("client_tags", schema="raw_metrics")

    op.drop_table("resource_groups", schema="raw_metrics")

    op.drop_table("operator_summaries", schema="raw_metrics")
