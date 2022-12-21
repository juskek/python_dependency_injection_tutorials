from unittest import mock

import pytest

from .containers import Container

'''
Software test fixtures initialize test functions. They provide a fixed baseline so that tests execute reliably and produce consistent, repeatable, results. Initialization may setup services, state, or other operating environments. These are accessed by test functions through arguments; for each fixture used by a test function there is typically a parameter (named after the fixture) in the test function’s definition.
'''


@pytest.fixture
def test_container():
    return Container(
        config={
            "database": {
                "dsn": ":memory:"
            },
            "aws": {
                "access_key_id": "TEST_KEY",
                "secret_access_key": "TEST_SECRET"
            },
            "auth": {
                "token_ttl": "3600"
            }
        },
        # logging does not need to be overwritten
    )


def test_get_user(test_container: Container):
    user_service_mock = mock.Mock()
    user_service_mock.get_user.return_value = {
        "email": "test@email.com", "password_hash": "test_password"}
    
    with test_container.user_service.override(user_service_mock):
        user_service = test_container.user_service()
        user = user_service.get_user()
        assert user["email"] == "test@email.com"
        assert user["password_hash"] == "test_password"

# def test_movies_directed_by(test_container):
#     finder_mock = mock.Mock()
#     finder_mock.find_all.return_value = [
#         test_container.movie("The 33", 2015, "Patricia Riggen"),
#         test_container.movie("The Jungle Book", 2016, "Jon Favreau"),
#     ]

#     with test_container.finder.override(finder_mock):
#         lister = test_container.lister()
#         movies = lister.movies_directed_by("Jon Favreau")

#     assert len(movies) == 1
#     assert movies[0].title == "The Jungle Book"


# def test_movies_released_in(container):
#     finder_mock = mock.Mock()
#     finder_mock.find_all.return_value = [
#         container.movie("The 33", 2015, "Patricia Riggen"),
#         container.movie("The Jungle Book", 2016, "Jon Favreau"),
#     ]

#     with container.finder.override(finder_mock):
#         lister = container.lister()
#         movies = lister.movies_released_in(2015)

#     assert len(movies) == 1
#     assert movies[0].title == "The 33"
