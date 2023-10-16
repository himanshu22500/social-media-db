from fb_post.utils import add_member_to_group
from fb_post.models import User
from fb_post.models import Group
from fb_post.models import UserGroup
from fb_post.tests.factories import UserFactory
from fb_post.tests.factories import GroupFactory
from fb_post.exceptions import InvalidUserException
from fb_post.exceptions import UserIsNotAdminException
import pytest

@pytest.mark.django_db
def test_add_member_to_group_with_invalid_user():
    user = UserFactory()
    group = GroupFactory()
    member = UserFactory()
    user.save()
    group.save()
    member.save()

    with pytest.raises(InvalidUserException):
        assert(add_member_to_group(user_id=-1, new_member_id=member.id, group_id=group.id))

@pytest.mark.django_db
def test_add_member_to_group_if_non_admin_adds_user():
    user = UserFactory()
    user.save()
    group = GroupFactory()
    group.save()
    group.members.add(user)
    group.save()

    with pytest.raises(UserIsNotAdminException):
        assert(add_member_to_group(user_id=user.id, new_member_id=user.id, group_id=group.id))
    
