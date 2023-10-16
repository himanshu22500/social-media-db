from fb_post.utils import create_group
from fb_post.models import User
from fb_post.models import Group
from fb_post.models import UserGroup
from fb_post.tests.factories import UserFactory
from fb_post.exceptions import InvalidUserException
from fb_post.exceptions import InvalidMemberException
from fb_post.exceptions import InvalidGroupNameException
import pytest

@pytest.mark.django_db
def test_create_group_with_valid_inputs(user):
    user.save()
    member_ids = [user.id]
    group_id = create_group(user_id=user.id,name="group-name",member_ids=member_ids)

    group_obj = Group.objects.get(id=group_id)
    group_member_ids = list(group_obj.members.all().values_list('id',flat=True))
    assert group_member_ids == member_ids
    assert group_obj.name == "group-name"

@pytest.mark.django_db
def test_create_group_with_invalid_user():
    member = UserFactory()
    member.save()
    member_ids = [member.id]

    with pytest.raises(InvalidUserException):
        assert(create_group(user_id=-1,name="group-name",member_ids=member_ids))

@pytest.mark.django_db
def test_create_user_with_invalid_memebrs(user):
    user.save()
    member_ids = [-1]
    with pytest.raises(InvalidMemberException):
        assert(create_group(user_id=user.id, name="group-name", member_ids=member_ids))

@pytest.mark.django_db
def test_create_user_with_invalid_name(user):
    user.save()
    member_ids = [user.id]
    with pytest.raises(InvalidGroupNameException):
        assert(create_group(user_id=user.id, name="", member_ids=member_ids))


@pytest.mark.django_db
def test_create_user_with_duplicate_member_ids(user):
    user.save()
    duplicate_member_ids = [user.id, user.id] 
    unique_member_ids = list(set(duplicate_member_ids))
    group_id = create_group(user_id=user.id, name="group-name", member_ids=duplicate_member_ids)

    group_obj = Group.objects.get(id=group_id)
    group_member_ids = list(group_obj.members.all().values_list('id',flat=True))
    assert group_member_ids == unique_member_ids
    assert group_obj.name == "group-name"


@pytest.mark.django_db
def test_create_group_if_creator_is_admin(user):
    user.save()
    member_ids = [user.id]
    group_id = create_group(user_id=user.id,name="group-name",member_ids=member_ids)

    group_obj = Group.objects.get(id=group_id)
    group_member_ids = list(group_obj.members.all().values_list('id',flat=True))
    
    user_group_obj = UserGroup.objects.get(user__id=user.id, group__id=group_id)
    
    assert user_group_obj.is_admin == True
    assert group_member_ids == member_ids
    assert group_obj.name == "group-name"