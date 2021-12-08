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

from ..models import ColumnMetrics, InitialQueryMetrics, QueryMetrics

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

    conn.execute(
        """
        DROP TABLE IF EXISTS column_metrics
    """
    )

    conn.execute(
        """
        DROP TABLE IF EXISTS raw_metrics.column_metrics
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
    assert session.query(QueryMetrics).count() == 0
    assert session.query(ColumnMetrics).count() == 0


# @pytest.mark.skip()
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
        session.query(QueryMetrics.totalRows).filter_by(queryId="20210922_091002_00016_mxhhc").first()["totalRows"]
        == 687
    )

    assert (
        session.query(QueryMetrics.physicalInputRows)
        .filter_by(queryId="20210922_091002_00016_mxhhc")
        .first()["physicalInputRows"]
        == 687
    )
