from fb_post.utils import remove_member_from_group
from fb_post.models import User
from fb_post.models import Group
from fb_post.models import UserGroup
from fb_post.tests.factories import UserFactory
from fb_post.tests.factories import GroupFactory
from fb_post.exceptions import InvalidUserException
from fb_post.exceptions import UserNotInGroupException
import pytest

@pytest.mark.django_db
def test_remove_member_from_group_when_user_to_remove_not_in_group():
    user = UserFactory.create()
    member = UserFactory()

    group = GroupFactory()
    group.members.add(user)

    user_group = UserGroup.objects.get(user=user, group=group)
    user_group.is_admin = True
    user_group.save()

    with pytest.raises(UserNotInGroupException):
        remove_member_from_group(user_id=user.id, member_id=member.id, group_id=group.id)
    
@pytest.mark.django_db
def test_remove_member_from_group_when_admin_user_removes_itself():
    user = UserFactory()
    user.save()
    group = GroupFactory()
    group.save()
    group.members.add(user)
    group.save()

    user_group = UserGroup.objects.get(user=user, group=group)
    user_group.is_admin = True
    user_group.save()

    remove_member_from_group(user_id=user.id, member_id=user.id, group_id=group.id)

    assert group.members.all().count() == 0


@pytest.mark.django_db
def test_remove_member_from_group_non_admin_leaves_group():
    user = UserFactory()
    user.save()
    group = GroupFactory()
    group.save()
    group.members.add(user)
    group.save()

    remove_member_from_group(user_id=user.id, member_id=user.id, group_id=group.id)

    assert group.members.all().count() == 0


    
    