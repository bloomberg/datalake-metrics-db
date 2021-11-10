from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

from ._query_metrics import QueryMetrics

Base = declarative_base()


class ColumnMetrics(Base):
    __tablename__ = "column_metrics"

    queryId = Column("queryId", String(100), ForeignKey(QueryMetrics.queryId), primary_key=True)
    catalogName = Column("catalogName", String(100), primary_key=True)
    schemaName = Column("schemaName", String(100), primary_key=True)
    tableName = Column("tableName", String(100), primary_key=True)
    columnName = Column("columnName", String(100), primary_key=True)
    physicalInputBytes = Column("physicalInputBytes", Integer)
    physicalInputRows = Column("physicalInputRows", Integer)

    __table_args__ = {"extend_existing": True, "schema": "raw_metrics"}
