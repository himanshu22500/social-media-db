from fb_post.utils import create_post
from fb_post.models import User
from fb_post.models import Post
from fb_post.exceptions import InvalidUserException
from fb_post.exceptions import InvalidPostContent
import pytest

@pytest.mark.django_db
def test_create_post_with_valid_input(user):
    user.save()
    user_id = user.id
    post_id = create_post(user_id, "Post-content")
    post_obj = Post.objects.get(id=post_id)

    assert post_obj.id == post_id
    assert post_obj.content == 'Post-content'

@pytest.mark.django_db
def test_create_post_with_invalid_user():
    with pytest.raises(InvalidUserException):
        assert(create_post(1, "Post-contnet"))

@pytest.mark.django_db
def test_create_post_with_empty_post_content(user):
    user.save()
    with pytest.raises(Exception):
        assert(create_post(1, ""))


