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
"""


from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import declarative_base

from ._query_metrics import QueryMetricsRev4

Base = declarative_base()


class _ResourceGroupsInitial:

    resourceGroup = Column("resourceGroup", String(255), primary_key=True)


class ResourceGroupsInitial(Base, _ResourceGroupsInitial):

    __tablename__ = "resource_groups"

    queryId = Column("queryId", String(100), ForeignKey(QueryMetricsRev4.queryId), primary_key=True)

    __table_args__ = {"extend_existing": True, "schema": "raw_metrics"}
