from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from reddit_detective import RedditNetwork

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testing"


def get_driver():
    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )


def test_constraint_creation():
    driver = get_driver()

    try:
        net = RedditNetwork(
            driver=driver,
            components=[],
        )

        net.create_constraints()

        print("✅ Constraints created successfully")

    except Neo4jError as err:
        print(f"❌ Neo4j error: {err}")

    except Exception as err:
        print(f"❌ Unexpected error: {err}")

    finally:
        driver.close()


def run():
    test_constraint_creation()


if __name__ == "__main__":
    run()
