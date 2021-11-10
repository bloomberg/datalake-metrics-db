"""bigger numbers

Revision ID: 5951554f7954
Revises: 36fd1c695484
Create Date: 2021-09-23 10:12:56.351656

"""
from sqlalchemy import BigInteger
from sqlalchemy.sql.sqltypes import Integer

from alembic import op

# revision identifiers, used by Alembic.
revision = "5951554f7954"
down_revision = "36fd1c695484"
branch_labels = None
depends_on = None


query_upgrade_columns = [
    "peakUserMemoryBytes",
    "peakTotalNonRevocableMemoryBytes",
    "peakTaskUserMemory",
    "peakTaskTotalMemory",
    "physicalInputBytes",
    "physicalInputRows",
    "internalNetworkBytes",
    "internalNetworkRows",
    "totalBytes",
    "totalRows",
    "outputBytes",
    "outputRows",
    "writtenBytes",
    "writtenRows",
    "cumulativeMemory",
    "completedSplits",
]

column_upgrade_columns = ["physicalInputBytes", "physicalInputRows"]


def upgrade():
    for col in query_upgrade_columns:
        op.alter_column("query_metrics", col, schema="raw_metrics", type_=BigInteger)

    for col in column_upgrade_columns:
        op.alter_column("column_metrics", col, schema="raw_metrics", type_=BigInteger)


def downgrade():
    for col in query_upgrade_columns:
        op.alter_column("query_metrics", col, schema="raw_metrics", type_=Integer)

    for col in column_upgrade_columns:
        op.alter_column("column_metrics", col, schema="raw_metrics", type_=Integer)
