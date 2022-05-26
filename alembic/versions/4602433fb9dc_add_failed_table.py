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


add failed table

Revision ID: 4602433fb9dc
Revises: d58a144ae68f
Create Date: 2022-05-25 12:38:56.355558

"""
from sqlalchemy import BigInteger, DateTime, UnicodeText, func
from sqlalchemy.sql.schema import Column

from alembic import op

# revision identifiers, used by Alembic.
revision = "4602433fb9dc"
down_revision = "d58a144ae68f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "failed_events",
        Column("id", BigInteger, primary_key=True, autoincrement=True),
        Column("event", UnicodeText, nullable=False),
        Column("createTime", DateTime, nullable=False, server_default=func.now()),
        schema="raw_metrics",
    )


def downgrade():
    op.drop_table("failed_events", schema="raw_metrics")
