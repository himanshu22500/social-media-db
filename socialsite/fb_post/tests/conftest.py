from fb_post.tests.factories import UserFactory
from fb_post.tests.factories import GroupFactory
from fb_post.tests.factories import UserGroupFactory
from pytest_factoryboy import register
import pytest

register(UserFactory)
register(GroupFactory)
register(UserGroupFactory)