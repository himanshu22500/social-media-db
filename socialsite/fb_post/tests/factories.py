from fb_post.models import User
from fb_post.models import Group
from fb_post.models import UserGroup
from fb_post.models import CommentReaction
from fb_post.models import Comment
from fb_post.models import Post
from fb_post.models import PostReaction

import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    name = factory.Sequence(lambda n: 'user%d' % n)
    profile_pic = factory.Sequence(lambda n: 'url%d' % n)

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
    
    name = factory.Sequence(lambda n: 'group%d' % n)
    members = factory.RelatedFactory(UserFactory)

class UserGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserGroup
    
    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
    is_admin = False
    