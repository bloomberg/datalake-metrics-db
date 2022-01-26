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


make peakTotalNonRevocableMemoryBytes nullable

Revision ID: 1670737c6856
Revises: 5951554f7954
Create Date: 2022-01-26 12:06:22.967428

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1670737c6856"
down_revision = "5951554f7954"
branch_labels = None
depends_on = None


COLUMN_NAME = "peakTotalNonRevocableMemoryBytes"


def upgrade():
    op.alter_column(
        "query_metrics",
        COLUMN_NAME,
        schema="raw_metrics",
        existing_type=sa.BigInteger,
        existing_nullable=False,
        nullable=True,
    )


def downgrade():
    op.alter_column(
        "query_metrics",
        COLUMN_NAME,
        schema="raw_metrics",
        existing_type=sa.BigInteger,
        existing_nullable=True,
        nullable=False,
    )
