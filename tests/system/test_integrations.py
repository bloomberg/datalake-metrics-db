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


from __future__ import annotations

import os
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, sessionmaker

import alembic.config

from ..models import (
    ClientTagsInitial,
    ColumnMetrics,
    FailedEventInitial,
    InitialQueryMetrics,
    OperatorSummariesInitial,
    OutputColumn,
    OutputColumnSource,
    QueryMetricsRev2,
    QueryMetricsRev4,
    ResourceGroupsInitial,
)

engine = create_engine(os.environ.get("SQLALCHEMY_URL").strip(), echo=True)


def upgrade_once():
    alembic.config.main(argv=["-c", "alembic.local.ini", "upgrade", "+1"])


@pytest.fixture()
def conn() -> Generator[Connection]:
    with engine.connect() as conn:
        yield conn


@pytest.fixture()
def session() -> Generator[Session]:
    Session = sessionmaker(bind=engine)
    with Session() as session:
        yield session


@pytest.fixture()
def _cleanup(conn: Connection):
    yield

    for table in [
        "output_column_sources",
        "output_columns",
        "column_metrics",
        "client_tags",
        "operator_summaries",
        "resource_groups",
        "failed_events",
    ]:
        conn.execute(
            f"""
            DROP TABLE IF EXISTS {table}
        """
        )

        conn.execute(
            f"""
            DROP TABLE IF EXISTS raw_metrics.{table}
        """
        )

    conn.execute(
        """
        DROP TABLE IF EXISTS query_metrics
    """
    )

    conn.execute(
        """
        DROP TABLE IF EXISTS raw_metrics.query_metrics
    """
    )

    conn.execute(
        """
        DROP TABLE IF EXISTS public.alembic_version
    """
    )

    conn.execute(
        """
        DROP TABLE IF EXISTS alembic_version
    """
    )


@pytest.mark.usefixtures("_cleanup")
def test_empty_migrations(session: Session):
    # Given
    alembicArgs = ["-c", "alembic.local.ini", "upgrade", "head"]

    # When
    alembic.config.main(argv=alembicArgs)

    # Then
    assert session.query(QueryMetricsRev2).count() == 0
    assert session.query(ColumnMetrics).count() == 0
    assert session.query(OperatorSummariesInitial).count() == 0
    assert session.query(ResourceGroupsInitial).count() == 0
    assert session.query(ClientTagsInitial).count() == 0
    assert session.query(FailedEventInitial).count() == 0
    assert session.query(OutputColumn).count() == 0
    assert session.query(OutputColumnSource).count() == 0


@pytest.mark.usefixtures("_cleanup")
def test_first_to_second_keeps_data(session: Session):
    # Given
    upgrade_once()

    session.add(
        InitialQueryMetrics(
            queryId="20210922_091002_00016_mxhhc",
            transactionId="c0d1f42d-8b58-4dfc-bb74-1a2a9b4078df",
            query="SELECT * FROM table",
            remoteClientAddress="127.0.0.1",
            user="test-user",
            userAgent="python-requests/2.25.1",
            source="datalake-python-client",
            serverAddress="0.0.0.0",
            serverVersion="358",
            environment="dev",
            queryType="SELECT",
            cpuTime=0.07,
            wallTime=0.37,
            queuedTime=0.001,
            scheduledTime=0.428,
            analysisTime=0.088,
            planningTime=0.043,
            executionTime=0.281,
            peakUserMemoryBytes=0,
            peakTotalNonRevocableMemoryBytes=60185,
            peakTaskUserMemory=0,
            peakTaskTotalMemory=60185,
            physicalInputBytes=18120,
            physicalInputRows=687,
            internalNetworkBytes=58985,
            internalNetworkRows=687,
            totalBytes=18120,
            totalRows=687,
            outputBytes=61120,
            outputRows=687,
            writtenBytes=0,
            writtenRows=0,
            cumulativeMemory=0,
            completedSplits=17,
            resourceWaitingTime=0.087,
            createTime=None,
            executionStartTime=None,
            endTime=None,
        )
    )

    session.commit()

    session.add(
        ColumnMetrics(
            queryId="20210922_091002_00016_mxhhc",
            catalogName="test-catalog",
            schemaName="test-schema",
            tableName="test-table",
            columnName="test-column",
            physicalInputBytes=18120,
            physicalInputRows=687,
        )
    )

    session.commit()

    # When
    upgrade_once()

    # Then

    assert (
        session.query(QueryMetricsRev2.totalRows)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["totalRows"]
        == 687
    )

    assert (
        session.query(QueryMetricsRev2.physicalInputRows)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["physicalInputRows"]
        == 687
    )


@pytest.mark.usefixtures("_cleanup")
def test_third_peakTotalNonRevocableMemoryBytes_nullable(session: Session):
    # Given
    alembicArgs = ["-c", "alembic.local.ini", "upgrade", "head"]
    alembic.config.main(argv=alembicArgs)

    # When
    session.add(
        InitialQueryMetrics(
            queryId="20210922_091002_00016_mxhhc",
            transactionId="c0d1f42d-8b58-4dfc-bb74-1a2a9b4078df",
            query="SELECT * FROM table",
            remoteClientAddress="127.0.0.1",
            user="test-user",
            userAgent="python-requests/2.25.1",
            source="datalake-python-client",
            serverAddress="0.0.0.0",
            serverVersion="358",
            environment="dev",
            queryType="SELECT",
            cpuTime=0.07,
            wallTime=0.37,
            queuedTime=0.001,
            scheduledTime=0.428,
            analysisTime=0.088,
            planningTime=0.043,
            executionTime=0.281,
            peakUserMemoryBytes=0,
            peakTotalNonRevocableMemoryBytes=None,
            peakTaskUserMemory=0,
            peakTaskTotalMemory=60185,
            physicalInputBytes=18120,
            physicalInputRows=687,
            internalNetworkBytes=58985,
            internalNetworkRows=687,
            totalBytes=18120,
            totalRows=687,
            outputBytes=61120,
            outputRows=687,
            writtenBytes=0,
            writtenRows=0,
            cumulativeMemory=0,
            completedSplits=17,
            resourceWaitingTime=0.087,
            createTime=None,
            executionStartTime=None,
            endTime=None,
        )
    )

    session.commit()

    # Then
    assert (
        session.query(QueryMetricsRev2.totalRows)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["totalRows"]
        == 687
    )


@pytest.mark.usefixtures("_cleanup")
def test_fourth_extra_columns(session: Session):
    # Given
    alembicArgs = ["-c", "alembic.local.ini", "upgrade", "head"]
    alembic.config.main(argv=alembicArgs)

    # When
    session.add(
        QueryMetricsRev4(
            queryId="20210922_091002_00016_mxhhc",
            transactionId="c0d1f42d-8b58-4dfc-bb74-1a2a9b4078df",
            query="SELECT * FROM table",
            remoteClientAddress="127.0.0.1",
            user="test-user",
            userAgent="python-requests/2.25.1",
            source="datalake-python-client",
            serverAddress="0.0.0.0",
            serverVersion="358",
            environment="dev",
            queryType="SELECT",
            uri="http://localhost:8080/v1/query/20220505_100804_00003_7dpwd",
            plan="Fragment 0 [SINGLE]\n    CPU: 5.48ms, Scheduled: 27.03ms, \
                Blocked 7.72s (Input: 7.72s, Output: 0.00ns), \
                Input: 1 row (571B); per task: avg.: 1.00 std.dev.: 0.00, \
                Output: 1 row (571B) └─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓",
            payload={
                "stageId": "20220505_100804_00003_7dpwd.0",
                "state": "FINISHED",
                "coordinatorOnly": False,
                "types": [],
                "stageStats": {},
            },
            planNodeStatsAndCosts={"stats": {}, "costs": {}},
            sessionProperties="{}",
            cpuTime=0.07,
            failedCpuTime=0,
            wallTime=0.37,
            queuedTime=0.001,
            scheduledTime=0.428,
            failedScheduledTime=1,
            analysisTime=0.088,
            planningTime=0.043,
            executionTime=0.281,
            inputBlockedTime=7.72,
            failedInputBlockedTime=0.1,
            outputBlockedTime=0.2,
            failedOutputBlockedTime=0.3,
            peakUserMemoryBytes=0,
            peakTotalNonRevocableMemoryBytes=0,
            peakTaskUserMemory=0,
            peakTaskTotalMemory=60185,
            physicalInputBytes=18120,
            physicalInputRows=687,
            internalNetworkBytes=58985,
            internalNetworkRows=687,
            processedInputBytes=100,
            processedInputRows=101,
            totalBytes=18120,
            totalRows=687,
            outputBytes=61120,
            outputRows=687,
            writtenBytes=0,
            writtenRows=0,
            cumulativeMemory=0,
            completedSplits=17,
            resourceWaitingTime=0.087,
            createTime=None,
            executionStartTime=None,
            endTime=None,
        )
    )

    session.commit()

    session.add(
        ColumnMetrics(
            queryId="20210922_091002_00016_mxhhc",
            catalogName="test-catalog",
            schemaName="test-schema",
            tableName="test-table",
            columnName="test-column",
            physicalInputBytes=18120,
            physicalInputRows=687,
        )
    )

    session.add(
        ClientTagsInitial(queryId="20210922_091002_00016_mxhhc", clientTag="superset")
    )
    session.add(
        ClientTagsInitial(queryId="20210922_091002_00016_mxhhc", clientTag="metadata")
    )

    session.add(
        ResourceGroupsInitial(
            queryId="20210922_091002_00016_mxhhc", resourceGroup="limited_user"
        )
    )
    session.add(
        ResourceGroupsInitial(
            queryId="20210922_091002_00016_mxhhc", resourceGroup="admin"
        )
    )

    session.add(
        OperatorSummariesInitial(
            queryId="20210922_091002_00016_mxhhc",
            operatorSummary={
                "stageId": 0,
                "pipelineId": 0,
                "operatorId": 1,
                "planNodeId": "6",
                "operatorType": "TaskOutputOperator",
                "totalDrivers": 8,
                "addInputCalls": 1,
                "addInputWall": "738.20us",
                "addInputCpu": "376.80us",
                "physicalInputDataSize": "0B",
                "physicalInputPositions": 0,
                "physicalInputReadTime": "0.00ns",
                "internalNetworkInputDataSize": "0B",
                "internalNetworkInputPositions": 0,
                "rawInputDataSize": "0B",
            },
        )
    )
    session.add(
        OperatorSummariesInitial(
            queryId="20210922_091002_00016_mxhhc",
            operatorSummary={
                "stageId": 1,
                "pipelineId": 0,
                "operatorId": 0,
                "planNodeId": "0",
                "operatorType": "TableScanOperator",
                "totalDrivers": 1,
                "addInputCalls": 0,
                "addInputWall": "0.00ns",
                "addInputCpu": "0.00ns",
                "physicalInputDataSize": "0B",
                "physicalInputPositions": 1,
                "physicalInputReadTime": "0.00ns",
                "internalNetworkInputDataSize": "0B",
                "internalNetworkInputPositions": 0,
                "rawInputDataSize": "0B",
                "info": {
                    "@type": "splitOperator",
                    "catalogName": "trino_anlytics",
                    "splitInfo": {
                        "@type": "../../plugin/trino-postgresql/pom.xml:io.trino.plugin.jdbc.JdbcSplit"
                    },
                },
            },
        )
    )

    session.commit()

    # Then
    assert "Fragment 0" in (
        session.query(QueryMetricsRev4.plan)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["plan"]
    )
    assert "└─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓" in (
        session.query(QueryMetricsRev4.plan)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["plan"]
    )

    assert (
        session.query(QueryMetricsRev4.payload)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["payload"]["stageId"]
        == "20220505_100804_00003_7dpwd.0"
    )

    assert (
        session.query(QueryMetricsRev4.processedInputBytes)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["processedInputBytes"]
        == 100
    )

    assert (
        session.query(QueryMetricsRev4.processedInputRows)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["processedInputRows"]
        == 101
    )

    assert (
        session.query(ClientTagsInitial)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .filter_by(clientTag="superset")
        .count()
        == 1
    )
    assert (
        session.query(ClientTagsInitial)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .filter_by(clientTag="metadata")
        .count()
        == 1
    )

    assert (
        session.query(ResourceGroupsInitial)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .filter_by(resourceGroup="limited_user")
        .count()
        == 1
    )
    assert (
        session.query(ResourceGroupsInitial)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .filter_by(resourceGroup="admin")
        .count()
        == 1
    )

    operator_summaries = [
        r["operatorSummary"]
        for r in session.query(OperatorSummariesInitial.operatorSummary)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .all()
    ]
    assert any(
        os["stageId"] == 0 and os["operatorType"] == "TaskOutputOperator"
        for os in operator_summaries
    )
    assert any(
        os["stageId"] == 1 and os["operatorType"] == "TableScanOperator"
        for os in operator_summaries
    )


@pytest.mark.usefixtures("_cleanup")
def test_fourth_null_extra_columns(session: Session):
    # Given
    alembicArgs = ["-c", "alembic.local.ini", "upgrade", "head"]
    alembic.config.main(argv=alembicArgs)

    # When
    session.add(
        QueryMetricsRev4(
            queryId="20210922_091002_00016_mxhhc",
            transactionId="c0d1f42d-8b58-4dfc-bb74-1a2a9b4078df",
            query="SELECT * FROM table",
            remoteClientAddress="127.0.0.1",
            user="test-user",
            userAgent="python-requests/2.25.1",
            source="datalake-python-client",
            serverAddress="0.0.0.0",
            serverVersion="358",
            environment="dev",
            queryType="SELECT",
            uri=None,
            plan=None,
            payload=None,
            planNodeStatsAndCosts=None,
            sessionProperties=None,
            cpuTime=0.07,
            wallTime=0.37,
            queuedTime=0.001,
            scheduledTime=0.428,
            analysisTime=0.088,
            planningTime=0.043,
            executionTime=0.281,
            peakUserMemoryBytes=0,
            peakTotalNonRevocableMemoryBytes=0,
            peakTaskUserMemory=0,
            peakTaskTotalMemory=60185,
            physicalInputBytes=18120,
            physicalInputRows=687,
            internalNetworkBytes=58985,
            internalNetworkRows=687,
            processedInputBytes=None,
            processedInputRows=None,
            totalBytes=18120,
            totalRows=687,
            outputBytes=61120,
            outputRows=687,
            writtenBytes=0,
            writtenRows=0,
            cumulativeMemory=0,
            completedSplits=17,
            resourceWaitingTime=0.087,
            createTime=None,
            executionStartTime=None,
            endTime=None,
        )
    )

    session.commit()

    # Then
    assert (
        session.query(QueryMetricsRev4)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .count()
        == 1
    )


@pytest.mark.usefixtures("_cleanup")
def test_fifth_failed_events(session: Session):
    # Given
    alembicArgs = ["-c", "alembic.local.ini", "upgrade", "head"]
    alembic.config.main(argv=alembicArgs)

    # When
    session.add(
        FailedEventInitial(event='{"queryId": "1234", "query": "select * from *"}')
    )
    session.commit()

    # Then
    failed_event = session.query(FailedEventInitial).first()

    assert failed_event is not None
    assert failed_event.id is not None
    assert failed_event.event == '{"queryId": "1234", "query": "select * from *"}'
    assert failed_event.createTime is not None


@pytest.mark.usefixtures("_cleanup")
def test_output_columns_and_sources(session: Session):
    # Given
    alembicArgs = ["-c", "alembic.local.ini", "upgrade", "head"]
    alembic.config.main(argv=alembicArgs)

    # When
    session.add(
        QueryMetricsRev4(
            queryId="20210922_091002_00016_mxhhc",
            transactionId="c0d1f42d-8b58-4dfc-bb74-1a2a9b4078df",
            query="SELECT * FROM table",
            remoteClientAddress="127.0.0.1",
            user="test-user",
            userAgent="python-requests/2.25.1",
            source="datalake-python-client",
            serverAddress="0.0.0.0",
            serverVersion="358",
            environment="dev",
            queryType="SELECT",
            uri=None,
            plan=None,
            payload=None,
            planNodeStatsAndCosts=None,
            sessionProperties=None,
            cpuTime=0.07,
            wallTime=0.37,
            queuedTime=0.001,
            scheduledTime=0.428,
            analysisTime=0.088,
            planningTime=0.043,
            executionTime=0.281,
            peakUserMemoryBytes=0,
            peakTotalNonRevocableMemoryBytes=0,
            peakTaskUserMemory=0,
            peakTaskTotalMemory=60185,
            physicalInputBytes=18120,
            physicalInputRows=687,
            internalNetworkBytes=58985,
            internalNetworkRows=687,
            processedInputBytes=None,
            processedInputRows=None,
            totalBytes=18120,
            totalRows=687,
            outputBytes=61120,
            outputRows=687,
            writtenBytes=0,
            writtenRows=0,
            cumulativeMemory=0,
            completedSplits=17,
            resourceWaitingTime=0.087,
            createTime=None,
            executionStartTime=None,
            endTime=None,
        )
    )
    session.commit()

    session.add(
        OutputColumn(
            queryId="20210922_091002_00016_mxhhc",
            catalogName="test-catalog",
            schemaName="test-schema",
            tableName="test-table",
            columnName="test-output-column",
        )
    )
    session.commit()

    session.add(
        OutputColumnSource(
            queryId="20210922_091002_00016_mxhhc",
            catalogName="test-catalog",
            schemaName="test-schema",
            tableName="test-table",
            columnName="test-output-column",
            sourceCatalogName="test-source-catalog",
            sourceSchemaName="test-source-schema",
            sourceTableName="test-source-table",
            sourceColumnName="test-source-column",
        )
    )
    session.commit()

    # Then
    result = session.query(OutputColumn).first()
    assert result is not None
    assert result.queryId == "20210922_091002_00016_mxhhc"
    assert result.catalogName == "test-catalog"
    assert result.schemaName == "test-schema"
    assert result.tableName == "test-table"
    assert result.columnName == "test-output-column"

    result = session.query(OutputColumnSource).first()
    assert result is not None
    assert result.queryId == "20210922_091002_00016_mxhhc"
    assert result.catalogName == "test-catalog"
    assert result.schemaName == "test-schema"
    assert result.tableName == "test-table"
    assert result.columnName == "test-output-column"
    assert result.sourceCatalogName == "test-source-catalog"
    assert result.sourceSchemaName == "test-source-schema"
    assert result.sourceTableName == "test-source-table"
    assert result.sourceColumnName == "test-source-column"


@pytest.mark.usefixtures("_cleanup")
def test_seventh_query_column_size_increase(session: Session):
    # Given
    alembicArgs = ["-c", "alembic.local.ini", "upgrade", "d3cb6e144c2c"]
    alembic.config.main(argv=alembicArgs)

    # When
    session.add(
        QueryMetricsRev4(
            queryId="20210922_091002_00016_mxhhc",
            query="a" * 10_100,
        )
    )

    # Then
    assert (
        session.query(QueryMetricsRev4)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()
        .query
        == "a" * 10_100
    )


@pytest.mark.usefixtures("_cleanup")
@pytest.mark.parametrize(
    "query_value",
    [
        pytest.param(None, id="NONE_QUERY"),
        pytest.param("", id="EMPTY_QUERY"),
        pytest.param(
            "SELECT * from catalog.schema.table where 'column' = 'hello'",
            id="NORMAL_QUERY",
        ),
        pytest.param("A" * 10_000, id="LONG_QUERY"),
        pytest.param(
            "└─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓", id="SPECIAL_UTF8_QUERY"
        ),
    ],
)
def test_seventh_query_column_data_not_lost(session: Session, query_value: str | None):
    # Given
    alembicArgs = ["-c", "alembic.local.ini", "upgrade", "d3cb6e144c2c-1"]
    alembic.config.main(argv=alembicArgs)
    session.add(
        QueryMetricsRev4(queryId="20210922_091002_00016_mxhhc", query=query_value)
    )

    # Given
    upgrade_once()

    # Then
    assert (
        session.query(QueryMetricsRev4)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()
        .query
        == query_value
    )
