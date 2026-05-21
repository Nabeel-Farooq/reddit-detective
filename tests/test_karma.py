import pytest
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from tests import api_
from reddit_detective import RedditNetwork

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testing"


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
        components=[],
    )


def test_karma(network):
    try:
        result = network.add_karma(api_)

        assert result is not None

    except Neo4jError as err:
        pytest.fail(f"Neo4j error occurred: {err}")

    except Exception as err:
        pytest.fail(f"Unexpected error occurred: {err}")


if __name__ == "__main__":
    pytest.main([__file__])
