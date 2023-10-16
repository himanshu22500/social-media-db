from fb_post.utils import make_member_as_admin
from fb_post.models import User
from fb_post.models import Group
from fb_post.models import UserGroup
from fb_post.tests.factories import UserFactory
from fb_post.tests.factories import GroupFactory
from fb_post.exceptions import InvalidUserException
from fb_post.exceptions import UserNotInGroupException
import pytest

