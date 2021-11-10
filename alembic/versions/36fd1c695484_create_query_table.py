"""create table query_metrics

Revision ID: 36fd1c695484
Revises:
Create Date: 2021-09-14 13:28:48.080864

"""
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.sql.schema import Column, ForeignKey

from alembic import op

# revision identifiers, used by Alembic.
revision = "36fd1c695484"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "query_metrics",
        Column("queryId", String(100), primary_key=True),
        Column("transactionId", String(100)),
        Column("query", String(10000)),
        Column("remoteClientAddress", String(100)),
        Column("user", String(100)),
        Column("userAgent", String(100)),
        Column("source", String(100)),
        Column("serverAddress", String(100)),
        Column("serverVersion", String(100)),
        Column("environment", String(10)),
        Column("queryType", String(50)),
        Column("cpuTime", Float),
        Column("wallTime", Float),
        Column("queuedTime", Float),
        Column("scheduledTime", Float),
        Column("analysisTime", Float),
        Column("planningTime", Float),
        Column("executionTime", Float),
        Column("peakUserMemoryBytes", Integer),
        Column("peakTotalNonRevocableMemoryBytes", Integer),
        Column("peakTaskUserMemory", Integer),
        Column("peakTaskTotalMemory", Integer),
        Column("physicalInputBytes", Integer),
        Column("physicalInputRows", Integer),
        Column("internalNetworkBytes", Integer),
        Column("internalNetworkRows", Integer),
        Column("totalBytes", Integer),
        Column("totalRows", Integer),
        Column("outputBytes", Integer),
        Column("outputRows", Integer),
        Column("writtenBytes", Integer),
        Column("writtenRows", Integer),
        Column("cumulativeMemory", Float),
        Column("completedSplits", Integer),
        Column("resourceWaitingTime", Float),
        Column("createTime", DateTime),
        Column("executionStartTime", DateTime),
        Column("endTime", DateTime),
        schema="raw_metrics",
    )

    op.create_table(
        "column_metrics",
        Column("queryId", String(100), ForeignKey("raw_metrics.query_metrics.queryId"), primary_key=True),
        Column("catalogName", String(100), primary_key=True),
        Column("schemaName", String(100), primary_key=True),
        Column("tableName", String(100), primary_key=True),
        Column("columnName", String(100), primary_key=True),
        Column("physicalInputBytes", Integer),
        Column("physicalInputRows", Integer),
        schema="raw_metrics",
    )


def downgrade():
    op.drop_table("column_metrics", schema="raw_metrics")

    op.drop_table("query_metrics", schema="raw_metrics")
