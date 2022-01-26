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


from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import BigInteger

Base = declarative_base()


class _InitialQueryMetrics:

    queryId = Column("queryId", String(100), primary_key=True)
    transactionId = Column("transactionId", String(100))
    query = Column("query", String(10000))
    remoteClientAddress = Column("remoteClientAddress", String(100))
    user = Column("user", String(100))
    userAgent = Column("userAgent", String(100))
    source = Column("source", String(100))
    serverAddress = Column("serverAddress", String(100))
    serverVersion = Column("serverVersion", String(100))
    environment = Column("environment", String(10))
    queryType = Column("queryType", String(50))
    cpuTime = Column("cpuTime", Float)
    wallTime = Column("wallTime", Float)
    queuedTime = Column("queuedTime", Float)
    scheduledTime = Column("scheduledTime", Float)
    analysisTime = Column("analysisTime", Float)
    planningTime = Column("planningTime", Float)
    executionTime = Column("executionTime", Float)
    peakUserMemoryBytes = Column("peakUserMemoryBytes", Integer)
    peakTotalNonRevocableMemoryBytes = Column("peakTotalNonRevocableMemoryBytes", Integer)
    peakTaskUserMemory = Column("peakTaskUserMemory", Integer)
    peakTaskTotalMemory = Column("peakTaskTotalMemory", Integer)
    physicalInputBytes = Column("physicalInputBytes", Integer)
    physicalInputRows = Column("physicalInputRows", Integer)
    internalNetworkBytes = Column("internalNetworkBytes", Integer)
    internalNetworkRows = Column("internalNetworkRows", Integer)
    totalBytes = Column("totalBytes", Integer)
    totalRows = Column("totalRows", Integer)
    outputBytes = Column("outputBytes", Integer)
    outputRows = Column("outputRows", Integer)
    writtenBytes = Column("writtenBytes", Integer)
    writtenRows = Column("writtenRows", Integer)
    cumulativeMemory = Column("cumulativeMemory", Float)
    completedSplits = Column("completedSplits", Integer)
    resourceWaitingTime = Column("resourceWaitingTime", Float)
    createTime = Column("createTime", DateTime)
    executionStartTime = Column("executionStartTime", DateTime)
    endTime = Column("endTime", DateTime)


class _QueryMetricsRev2(_InitialQueryMetrics):

    peakUserMemoryBytes = Column("peakUserMemoryBytes", BigInteger)
    peakTotalNonRevocableMemoryBytes = Column("peakTotalNonRevocableMemoryBytes", BigInteger)
    peakTaskUserMemory = Column("peakTaskUserMemory", BigInteger)
    peakTaskTotalMemory = Column("peakTaskTotalMemory", BigInteger)
    physicalInputBytes = Column("physicalInputBytes", BigInteger)
    physicalInputRows = Column("physicalInputRows", BigInteger)
    internalNetworkBytes = Column("internalNetworkBytes", BigInteger)
    internalNetworkRows = Column("internalNetworkRows", BigInteger)
    totalBytes = Column("totalBytes", BigInteger)
    totalRows = Column("totalRows", BigInteger)
    outputBytes = Column("outputBytes", BigInteger)
    outputRows = Column("outputRows", BigInteger)
    writtenBytes = Column("writtenBytes", BigInteger)
    writtenRows = Column("writtenRows", BigInteger)


class _QueryMetricsRev3(_QueryMetricsRev2):

    peakTotalNonRevocableMemoryBytes = Column("peakTotalNonRevocableMemoryBytes", BigInteger, nullable=True)


class InitialQueryMetrics(Base, _InitialQueryMetrics):
    __tablename__ = "query_metrics"

    __table_args__ = {"extend_existing": True, "schema": "raw_metrics"}


class QueryMetricsRev2(Base, _QueryMetricsRev2):
    __tablename__ = "query_metrics"

    __table_args__ = {"schema": "raw_metrics", "extend_existing": True}


class QueryMetricsRev3(Base, _QueryMetricsRev3):
    __tablename__ = "query_metrics"

    __table_args__ = {"schema": "raw_metrics", "extend_existing": True}
