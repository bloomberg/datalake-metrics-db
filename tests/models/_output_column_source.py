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


from sqlalchemy import BigInteger, Column, ForeignKeyConstraint, String
from sqlalchemy.orm import declarative_base

from ._output_column import OutputColumn

Base = declarative_base()


class _OutputColumnSourceInitial:

    id = Column("id", BigInteger, autoincrement=True, primary_key=True)
    queryId = Column("queryId", String(100), primary_key=True)
    catalogName = Column("catalogName", String(100), primary_key=True)
    schemaName = Column("schemaName", String(100), primary_key=True)
    tableName = Column("tableName", String(100), primary_key=True)
    columnName = Column("columnName", String(100), primary_key=True)
    sourceCatalogName = Column("sourceCatalogName", String(100))
    sourceSchemaName = Column("sourceSchemaName", String(100))
    sourceTableName = Column("sourceTableName", String(100))
    sourceColumnName = Column("sourceColumnName", String(100))


class OutputColumnSource(_OutputColumnSourceInitial, Base):

    __tablename__ = "output_column_sources"

    __table_args__ = (
        ForeignKeyConstraint(
            [
                _OutputColumnSourceInitial.queryId,
                _OutputColumnSourceInitial.catalogName,
                _OutputColumnSourceInitial.schemaName,
                _OutputColumnSourceInitial.tableName,
                _OutputColumnSourceInitial.columnName,
            ],
            [
                OutputColumn.queryId,
                OutputColumn.catalogName,
                OutputColumn.schemaName,
                OutputColumn.tableName,
                OutputColumn.columnName,
            ],
        ),
        {"extend_existing": True, "schema": "raw_metrics"},
    )
