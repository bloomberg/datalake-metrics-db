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


from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import BigInteger

from ._query_metrics import InitialQueryMetrics

Base = declarative_base()


class _OperatorSummariesInitial:

    id = Column("id", BigInteger, autoincrement=True, primary_key=True)
    operatorSummary = Column("operatorSummary", JSON(none_as_null=True), nullable=False)


class OperatorSummariesInitial(Base, _OperatorSummariesInitial):

    __tablename__ = "operator_summaries"

    queryId = Column("queryId", String(100), ForeignKey(InitialQueryMetrics.queryId), primary_key=True)

    __table_args__ = {"extend_existing": True, "schema": "raw_metrics"}
