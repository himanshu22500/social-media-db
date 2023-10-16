import pytest
from fb_post.models import User
from fb_post.tests.factories import UserFactory

# def test_user_factory(user_factory):
#     assert user_factory == UserFactory

# def test_user(user):
#     assert isinstance(user, User)

# @pytest.mark.parametrize("user__name", ["Himanshu", "Hari"])
# @pytest.mark.parametrize("user__profile_pic", ["www.google.com", "www.fb.com"])
# def test_parametrized(user):
#     """You can set any factory attribute as a fixture using naming convention."""
#     print()
#     print(user.name, user.profile_pic)
#     assert (user.name == "Himanshu" or user.name == "Hari")
#     assert (user.profile_pic == "www.google.com" or user.profile_pic == "www.fb.com" )