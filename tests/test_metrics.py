import pytest
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from reddit_detective.analytics.metrics import (
    interaction_score,
    interaction_score_normalized,
    cyborg_score_user,
    cyborg_score_submission,
    cyborg_score_subreddit,
)

from reddit_detective.analytics.utils import (
    get_redditors,
    get_user_comments_times,
    get_submission_comments_times,
    get_subreddit_comments_times,
)

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testing"

TEST_USER = "Anub_Rekhan"
TEST_SUBMISSION = "hfulq4"
TEST_SUBREDDIT = "Python"


@pytest.fixture(scope="module")
def driver():
    driver_instance = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )

    yield driver_instance

    driver_instance.close()


def assert_score(score):
    assert score is not None
    assert isinstance(score, float)
    assert 0 <= score <= 1


def assert_list(value):
    assert value is not None
    assert isinstance(value, list)


def test_get_users(driver):
    users = get_redditors(driver)

    assert_list(users)


def test_get_user_comments_times(driver):
    ids, times = get_user_comments_times(
        driver,
        TEST_USER,
    )

    assert_list(ids)
    assert_list(times)


def test_get_submission_comments_times(driver):
    ids, times = get_submission_comments_times(
        driver,
        TEST_SUBMISSION,
    )

    assert_list(ids)
    assert_list(times)


def test_get_subreddit_comments_times(driver):
    ids, times = get_subreddit_comments_times(
        driver,
        TEST_SUBREDDIT,
    )

    assert_list(ids)
    assert_list(times)


def test_interaction_score(driver):
    score = interaction_score(
        driver,
        TEST_USER,
    )

    assert_score(score)


def test_interaction_score_normalized(driver):
    score = interaction_score_normalized(
        driver,
        TEST_USER,
    )

    assert_score(score)


def test_cyborg_score_user(driver):
    score, cyborgs = cyborg_score_user(
        driver,
        TEST_USER,
    )

    assert_score(score)
    assert_list(cyborgs)


def test_cyborg_score_submission(driver):
    score, cyborgs = cyborg_score_submission(
        driver,
        TEST_SUBMISSION,
    )

    assert_score(score)
    assert_list(cyborgs)


def test_cyborg_score_subreddit(driver):
    score, cyborgs = cyborg_score_subreddit(
        driver,
        TEST_SUBREDDIT,
    )

    assert_score(score)
    assert_list(cyborgs)


def test_database_connection(driver):
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS value")
            record = result.single()

            assert record["value"] == 1

    except Neo4jError as err:
        pytest.fail(f"Neo4j connection failed: {err}")


if __name__ == "__main__":
    pytest.main([__file__])
