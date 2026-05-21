import pytest

from reddit_detective.data_models import (
    Redditor,
    Subreddit,
)

from reddit_detective.relationships import (
    Comments,
    CommentsReplies,
    Submissions,
)

from tests import api_

"""
Neo4j constraints for manual testing:

CREATE CONSTRAINT UniqueRedditor
ON (r:Redditor) ASSERT (r.id) IS UNIQUE

CREATE CONSTRAINT UniqueSubmission
ON (sm:Submission) ASSERT (sm.id) IS UNIQUE

CREATE CONSTRAINT UniqueSubreddit
ON (sr:Subreddit) ASSERT (sr.id) IS UNIQUE
"""

TEST_SUBREDDIT = "learnpython"
TEST_REDDITOR = "Anub_Rekhan"
TEST_LIMIT = 2


@pytest.fixture(scope="module")
def subreddit():
    return Subreddit.from_base_obj(
        api_.subreddit(TEST_SUBREDDIT),
        TEST_LIMIT,
    )


@pytest.fixture(scope="module")
def redditor():
    return Redditor.from_base_obj(
        api_.redditor(TEST_REDDITOR),
        TEST_LIMIT,
    )


def assert_valid_code(code):
    assert code is not None
    assert isinstance(code, list | str)

    if isinstance(code, list):
        assert len(code) > 0


def test_submissions(subreddit, redditor):
    submissions_sub = Submissions(subreddit)
    submissions_red = Submissions(redditor)

    assert_valid_code(submissions_sub.code())
    assert_valid_code(submissions_red.code())


def test_comments(subreddit, redditor):
    comments_sub = Comments(subreddit)
    comments_red = Comments(redditor)

    assert comments_sub.comments() is not None
    assert comments_red.comments() is not None

    assert_valid_code(comments_sub.code())
    assert_valid_code(comments_red.code())


def test_replies(subreddit, redditor):
    replies_sub = CommentsReplies(subreddit)
    replies_red = CommentsReplies(redditor)

    assert replies_sub.comments() is not None
    assert replies_red.comments() is not None

    assert_valid_code(replies_sub.code())
    assert_valid_code(replies_red.code())


def test_generated_code_contains_merge(subreddit):
    submissions = Submissions(subreddit)

    code = submissions.code()

    if isinstance(code, list):
        joined_code = " ".join(code)
    else:
        joined_code = code

    assert "MERGE" in joined_code or "CREATE" in joined_code


if __name__ == "__main__":
    pytest.main([__file__])
