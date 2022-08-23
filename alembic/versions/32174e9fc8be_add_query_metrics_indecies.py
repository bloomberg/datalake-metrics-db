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


add query_metrics indecies

Revision ID: 32174e9fc8be
Revises: d3cb6e144c2c
Create Date: 2022-08-23 11:19:38.183700

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "32174e9fc8be"
down_revision = "d3cb6e144c2c"
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.create_index(
            "createtime_index", "query_metrics", ["createTime"], schema="raw_metrics", postgresql_concurrently=True
        )

        op.create_index("user_index", "query_metrics", ["user"], schema="raw_metrics", postgresql_concurrently=True)


def downgrade():
    with op.get_context().autocommit_block():
        op.drop_index("createtime_index", "query_metrics", schema="raw_metrics", postgresql_concurrently=True)

        op.drop_column("user_index", "query_metrics", schema="raw_metrics", postgresql_concurrently=True)
