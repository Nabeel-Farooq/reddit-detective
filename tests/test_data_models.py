import pytest

from reddit_detective.data_models import (
    Comment,
    Redditor,
    Submission,
    Subreddit,
)

from tests import api_

"""
Tests for Reddit Detective data models.
"""


@pytest.fixture(scope="module")
def subreddit():
    return Subreddit.from_base_obj(
        api_.subreddit("learnpython"),
        limit=100,
    )


@pytest.fixture(scope="module")
def submission():
    return Submission.from_base_obj(
        api_.submission("jhd0px"),
        limit=100,
    )


@pytest.fixture(scope="module")
def redditor():
    return Redditor.from_base_obj(
        api_.redditor("Anub_Rekhan"),
        limit=100,
    )


@pytest.fixture(scope="module")
def suspended_redditor():
    return Redditor.from_base_obj(
        api_.redditor("deleted"),
        limit=100,
    )


@pytest.fixture(scope="module")
def comment():
    return Comment.from_base_obj(
        api_.comment("gcltb0o"),
    )


@pytest.fixture(scope="module")
def deleted_author_comment():
    return Comment.from_base_obj(
        api_.comment("fo2ap22"),
    )


def test_subreddit(subreddit):
    assert subreddit.main_type in subreddit.types

    assert subreddit.properties.get("created_utc")

    assert subreddit.submissions() is not None

    assert subreddit.subscribers is not None


def test_submission(submission):
    assert submission.main_type in submission.types

    assert submission.properties.get("created_utc")

    assert isinstance(submission.subreddit, Subreddit)

    assert submission.comments() is not None

    assert submission.score is not None

    assert submission.upvote_ratio is not None

    assert submission.author_accessible, (
        "Submission has no accessible author."
    )

    assert isinstance(submission.author, Redditor)


def test_redditor(redditor, suspended_redditor):
    assert redditor.main_type in redditor.types

    assert redditor.properties.get("created_utc")

    assert redditor.submissions() is not None

    assert redditor.comments() is not None

    assert redditor.link_karma is not None

    assert redditor.comment_karma is not None

    assert "Suspended" in suspended_redditor.types

    assert suspended_redditor.comments() == []

    assert suspended_redditor.submissions() == []


def test_comment(comment, deleted_author_comment):
    assert comment.properties.get("text")

    assert isinstance(comment.submission, Submission)

    assert comment.replies() is not None

    assert comment.score is not None

    assert comment.author_accessible, (
        "Comment has no accessible author."
    )

    assert isinstance(comment.author, Redditor)

    assert not deleted_author_comment.author_accessible


def test_cypher_codes_node(subreddit):
    types_code = subreddit.types_code()
    props_code = subreddit.props_code()
    merge_code = subreddit.merge_code()

    assert types_code
    assert subreddit.types[0] in types_code
    assert ":" in types_code

    assert props_code
    assert str(subreddit.properties["id"]) in props_code
    assert ":" in props_code
    assert "{" in props_code and "}" in props_code

    assert merge_code
    assert "MERGE" in merge_code
    assert types_code in merge_code
    assert props_code in merge_code


if __name__ == "__main__":
    pytest.main([__file__])
