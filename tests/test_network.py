import pytest
from collections import Counter

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from tests import api_

from reddit_detective import (
    Comments,
    CommentsReplies,
    RedditNetwork,
)

from reddit_detective.data_models import (
    Redditor,
    Submission,
)

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "test2"

TEST_USER = "Anub_Rekhan"
TEST_SUBMISSION = "jpt7s7"


@pytest.fixture(scope="module")
def driver():
    driver_instance = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )

    yield driver_instance

    driver_instance.close()


@pytest.fixture(scope="module")
def network(driver):
    return RedditNetwork(
        driver=driver,
        components=[
            Comments(
                Redditor(
                    api_,
                    TEST_USER,
                    limit=5,
                )
            )
        ],
    )


def test_network_creation(network):
    try:
        network.run_cypher_code()

    except Neo4jError as err:
        pytest.fail(f"Neo4j error occurred: {err}")

    except Exception as err:
        pytest.fail(f"Unexpected error occurred: {err}")


def test_code_uniqueness(driver):
    obj = CommentsReplies(
        Submission(
            api_,
            TEST_SUBMISSION,
            limit=None,
        )
    )

    net = RedditNetwork(
        driver=driver,
        components=[obj],
    )

    obj_code_list = obj.code()
    net_code_list = list(net._codes())

    diff_counter = (
        Counter(obj_code_list) -
        Counter(net_code_list)
    )

    assert all(
        value <= 1
        for value in diff_counter.values()
    )


def test_network_codes_not_empty(driver):
    obj = CommentsReplies(
        Submission(
            api_,
            TEST_SUBMISSION,
            limit=10,
        )
    )

    net = RedditNetwork(
        driver=driver,
        components=[obj],
    )

    codes = list(net._codes())

    assert codes is not None
    assert isinstance(codes, list)
    assert len(codes) > 0


def test_database_connection(driver):
    try:
        with driver.session() as session:
            result = session.run(
                "RETURN 'connected' AS status"
            )

            record = result.single()

            assert record["status"] == "connected"

    except Neo4jError as err:
        pytest.fail(f"Database connection failed: {err}")


if __name__ == "__main__":
    pytest.main([__file__])
