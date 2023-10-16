from .models import User
from .models import PostReaction
from .models import CommentReaction
from .models import Post
from .models import Comment
from .models import UserGroup
from .models import Group
from datetime import datetime

from .exceptions import InvalidUserException
from .exceptions import InvalidPostContent
from .exceptions import InvalidCommentContent
from .exceptions import InvalidReplyContent
from .exceptions import InvalidReactionTypeExpections
from .exceptions import UserCannotDeletePostException
from .exceptions import InvalidPostException
from .exceptions import InvalidCommentException
from .exceptions import InvalidReactionTypeException
from .exceptions import UserCannotDeletePostException
from .exceptions import InvalidMemberException
from .exceptions import UserNotInGroupException
from .exceptions import InvalidGroupException
from .exceptions import UserIsNotAdminException
from .exceptions import InvalidOffSetValueException
from .exceptions import InvalidLimitSetValueException
from .exceptions import InvalidGroupNameException

from django.db.models import Q
from django.db.models import F
from django.db.models import Count
from collections import defaultdict

DATE_FORMAT = "%Y-%m-%d"

REACTION_TYPES = [
    "WOW",
    "LIT",
    "LOVE",
    "HAHA",
    "THUMBS-UP",
    "THUMBS-DOWN",
    "ANGRY",
    "SAD"
]


def create_users(users_list):
    user_objects = []
    for user in users_list:
        user_object = User(**user)
        user_objects.append(user_object)
    User.objects.bulk_create(user_objects)


def create_posts(post_list):
    user_ids = [post['posted_by'] for post in post_list]
    user_objects = User.objects.filter(id__in=user_ids)
    cached_user_objects = {}
    for user_obj in user_objects:
        cached_user_objects[user_obj.id] = user_obj

    post_objects = []
    for post in post_list:
        user = cached_user_objects[post['posted_by']]
        date_str = post['posted_at']
        date_object = datetime.strptime(date_str, DATE_FORMAT)
        post_object = Post(
            content=post['content'], posted_at=date_object, posted_by=user)
        post_objects.append(post_object)
    Post.objects.bulk_create(post_objects)


def create_comments(comments_list):
    user_ids = [comment['commented_by'] for comment in comments_list]
    user_objects = list(User.objects.filter(id__in=user_ids))
    cached_user_objects = {}
    for user_obj in user_objects:
        cached_user_objects[user_obj.id] = user_obj

    post_ids = [comment['posted_at'] for comment in comments_list]
    post_objects = Post.objects.filter(id__in=post_ids)
    cached_post_objects = {}
    for post_obj in post_objects:
        cached_post_objects[post_obj.id] = post_obj

    comment_ids = [comment['parent_comment'] for comment in comments_list]
    comment_objects = Comment.objects.filter(id__in=comment_ids)
    cached_comment_objects = {}
    for commnet_obj in comment_objects:
        cached_comment_objects[commnet_obj.id] = commnet_obj

    comment_objects = []
    for comment in comments_list:
        post = cached_post_objects[comment['posted_at']]
        user = cached_user_objects[comment['commented_by']]
        parent_comment = cached_comment_objects[comment['parent_comment']]
        date_str = comment['commented_at']
        date_object = datetime.strptime(date_str, DATE_FORMAT)
        comment_object = Comment(content=comment['content'],
                                 post=post,
                                 commented_by=user,
                                 commented_at=date_object,
                                 parent_comment=parent_comment
                                 )
        comment_objects.append(comment_object)
    Comment.objects.bulk_create(comment_objects)


def create_post(user_id, post_content):
    """
    :returns: post_id
    """
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist as e:
        raise InvalidUserException(f'{user_id} id not in database')
    
    if post_content == "":
        raise InvalidPostContent('post_content is an empty sting')

    current_datetime = datetime.now()
    post_obj = Post.objects.create(posted_by=user_obj, posted_at=current_datetime, content=post_content)
    return post_obj.id


def create_comment(user_id, post_id, comment_content):
    """
    :returns: comment_id
    """
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        post_obj = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise InvalidPostException(f'{post_id} id not in database')

    if comment_content == "":
        raise InvalidCommentContent('Comment content is Empty')

    current_datetime = datetime.now()
    comment_obj = Comment.objects.create(
        content=comment_content,
        commented_at=current_datetime,
        commented_by=user_obj,
        post=post_obj
    )

    return comment_obj.id

# print(create_comment(23, 34, "hello How are you"))


def reply_to_comment(user_id, comment_id, reply_content):
    """
    :returns: comment_id
    """
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        comment_obj = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise InvalidCommentException(f'{comment_id} id not in database')

    if reply_content == "":
        raise InvalidReplyContent('Reply is Empty')

    post_obj = Post.objects.get(id=comment_obj.post.id)

    current_datetime = datetime.now()
    reply_object = Comment.objects.create(
        content=reply_content,
        commented_at=current_datetime,
        commented_by=user_obj,
        post=post_obj
    )

    return reply_object.id

# print(reply_to_comment(23, 1101, "Doing great Buddy"))


def react_to_post(user_id, post_id, reaction_type):
    """
    """
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        post_obj = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise InvalidPostException(f'{post_id} id not in database')

    if reaction_type not in REACTION_TYPES:
        raise InvalidReactionTypeException('Not a valid Reaction')

    try:
        post_reaction = PostReaction.objects.get(
            Q(post__id=post_id) & Q(reacted_by__id=user_id))
    except PostReaction.DoesNotExist:
        current_datetime = datetime.now()
        PostReaction.objects.create(
            reacted_by=user_obj,
            post=post_obj,
            reaction=reaction_type,
            reacted_at=current_datetime
        )
    else:
        if post_reaction.reaction == reaction_type:
            post_reaction.delete()
        else:
            post_reaction.reaction_type = reaction_type
            post_reaction.save()


# print(react_to_post(23, 34, "WOW"))

# bulkReact()


def react_to_comment(user_id, comment_id, reaction_type):
    """
    """
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        comment_obj = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise InvalidCommentException(f'{comment_id} id not in database')

    if reaction_type not in REACTION_TYPES:
        raise InvalidReactionTypeException('Not a valid Reaction')

    try:
        comment_reaction = CommentReaction.objects.get(comment__id=comment_id)
    except CommentReaction.DoesNotExist:
        current_datetime = datetime.now()
        CommentReaction.objects.create(
            reacted_by=user_obj,
            comment=comment_obj,
            reaction=reaction_type,
            reacted_at=current_datetime
        )
    else:
        if comment_reaction.reaction == reaction_type:
            comment_reaction.delete()
        else:
            comment_reaction.reaction_type = reaction_type
            comment_reaction.save()

# print(react_to_comment(23, 1101, "ANGRY"))

def get_total_reaction_count():
    """
    :returns: {'count': 10}
    """
    return PostReaction.objects.count() + CommentReaction.objects.count()

# print(get_total_reaction_count())


def get_reaction_metrics(post_id):
    """
    :returns: {'LIKE':4, 'WOW':2}
    """
    #  = PostReaction.objects.filter(post__id=post_id).values_list('reaction', flat=True)
    reaction_list = PostReaction.objects.filter(
        post__id=34).values('reaction').annotate(count=Count('*'))
    reaction_martics = {}
    for reaction in reaction_list:
        reaction_martics[reaction['reaction']] = reaction['count']

    return reaction_martics

# print(get_reaction_metrics(34))


def delete_post(user_id, post_id):
    """
    """
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    post_query_obj = Post.objects.filter(
        id=post_id).select_related('posted_by')
    if len(post_query_obj) == 0:
        raise InvalidPostException(f'{post_id} id not in database')

    post_obj = post_query_obj[0]
    if post_obj.posted_by.id != user_id:
        raise UserCannotDeletePostException(f'post not created by user')
    else:
        post_obj.delete()

# delete_post(468, 22)


def get_posts_with_more_positive_reactions():
    """
    """
    POSITIVE_REACTIONS = ["THUMBS-UP", "LIT", "LOVE", "HAHA", "WOW"]
    NEGATIVE_REACTIONS = ["SAD", "ANGRY", "THUMBS-DOWN"]
    # reaction_list = PostReaction.objects.all().values('reaction').annotate(count=Count('*'))
    reaction_list = PostReaction.objects.values(
        'post', 'reaction').annotate(Count('reaction'))
    pos_neg_count = {}
    for reaction in reaction_list:
        if pos_neg_count.get(reaction['post'], -1) == -1:
            rec_dict = {
                'post_id': reaction['post'],
                'positive_count': 0,
                'negative_count': 0
            }
            pos_neg_count[reaction['post']] = rec_dict

        if reaction['reaction'] in POSITIVE_REACTIONS:
            pos_neg_count[reaction['post']
                          ]['positive_count'] += reaction['reaction__count']
        else:
            pos_neg_count[reaction['post']
                          ]['negative_count'] += reaction['reaction__count']

    post_with_more_pos = []
    for post_id in pos_neg_count:
        if pos_neg_count[post_id]['positive_count'] > pos_neg_count[post_id]['negative_count']:
            post_with_more_pos.append(post_id)

    return post_with_more_pos

# print(get_posts_with_more_positive_reactions())


def get_posts_reacted_by_user(user_id):
    """
    :returns: list of post ids
    """
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    return list(PostReaction.objects.filter(reacted_by__id=user_id).values_list('post_id', flat=True))

# print(get_posts_reacted_by_user(34))


def get_reactions_to_post(post_id):
    """
    :returns: [
        {"user_id": 1, "name": "iB Cricket", "profile_pic": "", "reaction": "LIKE"},
        ...
    ]
    """
    try:
        post_obj = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise InvalidPostException(f'{post_id} id not in database')

    post_reactions = PostReaction.objects.filter(post__id=post_id).values(
        'reacted_by__id',
        'reacted_by__name',
        'reacted_by__profile_pic',
        'reaction'
    )
    reactions_list = []
    for reaction in post_reactions:
        reaction_obj = {
            'user_id': reaction['reacted_by__id'],
            'name': reaction['reacted_by__name'],
            'profile_pic': reaction['reacted_by__profile_pic'],
            'reaction': reaction['reaction']
        }
        reactions_list.append(reaction_obj)
    return reactions_list

# print(get_reactions_to_post(34)[0])


def get_post(post_id):
    """
    :returns: {
        "post_id": 1,
        "posted_by": {
            "name": "iB Cricket",
            "user_id": 1,
            "profile_pic": "https://dummy.url.com/pic.png"
        },
        "posted_at": "2019-05-21 20:21:46.810366"
        "post_content": "Write Something here...",
        "reactions": {
            "count": 10,
            "type": ["HAHA", "WOW"]
        },
        "comments": [
            {
                "comment_id": 1
                "commenter": {
                    "user_id": 2,
                    "name": "Yuri",
                    "profile_pic": "https://dummy.url.com/pic.png"
                },
                "commented_at": "2019-05-21 20:22:46.810366",
                "comment_content": "Nice game...",
                "reactions": {
                    "count": 1,
                    "type": ["LIKE"]
                },
                "replies_count": 1,
                "replies": [{
                    "comment_id": 2
                    "commenter": {
                        "user_id": 1,
                        "name": "iB Cricket",
                        "profile_pic": "https://dummy.url.com/pic.png"
                    },
                    "commented_at": "2019-05-21 20:22:46.810366",
                    "comment_content": "Thanks...",
                    "reactions": {
                        "count": 1,
                        "type": ["LIKE"]
                    },
                }]
            },
            ...
        ],
        "comments_count": 3,
    }
    """
    pass


def get_user_posts(user_id):
    """
    Explanation: Return a list of responses similar to get_post
    """
    pass


def get_replies_for_comment(comment_id):
    """
    :returns: [{
        "comment_id": 2
        "commenter": {
            "user_id": 1,
            "name": "iB Cricket",
            "profile_pic": "https://dummy.url.com/pic.png"
        },
        "commented_at": "2019-05-21 20:22:46.810366",
        "comment_content": "Thanks...",
    }]
    """
    try:
        comment_obj = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise InvalidCommentException(f'{comment_id} id not in database')
    replies_objects = Comment.objects.filter(parent_comment__id=comment_id).values(
        'commented_at',
        comment_id=F('id'),
        name=F('commented_by__name'),
        profile_pic=F('commented_by__profile_pic'),
        comment_content=F('content'),
        user_id=F('commented_by__id')
    )

    final_reply = []
    for reply in replies_objects:
        reply_dict = {
            "comment_id": reply['comment_id'],
            'commneter': {
                'user_id': reply['user_id'],
                'name': reply['name'],
                'profile_pic': reply['profile_pic']
            },
            'commented_at': str(reply['commented_at']),
            'commnet_content': reply['comment_content']
        }
        final_reply.append(reply_dict)

    return final_reply

# from pprint import pprint
# pprint(get_replies_for_comment(34))


##################### Assigment007 #################

def create_group(user_id, name, member_ids):
    if name == "":
        raise InvalidGroupNameException('name is an empty string')
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    fetched_member_ids = User.objects.filter(
        id__in=member_ids).values_list('id', flat=True)

    if len(set(member_ids)) != len(fetched_member_ids):
        raise InvalidMemberException(f'all {member_ids} not in database')

    member_objects = list(User.objects.filter(id__in=member_ids))
    member_objects.append(user_obj)
    group_object = Group.objects.create(name=name)
    group_object.members.add(*member_objects)
    group_id = group_object.id

    user_group_obj = UserGroup.objects.get(user__id=user_id, group__id=group_id)
    user_group_obj.is_admin = True
    user_group_obj.save()

    return group_id

# print(create_group(34, "Bro in house", [34, 1, 2, 6,7]))
# Output : 4


def add_member_to_group(user_id, new_member_id, group_id):
    try:
        group_obj = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise InvalidMemberException(f'{group_id} id not in database')

    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        new_member_obj = User.objects.get(id=new_member_id)
    except User.DoesNotExist:
        raise InvalidGroupException(f'{new_member_id} id not in database')

    try:
        user_group_obj = UserGroup.objects.get(
            user__id=user_id, group__id=group_id)
    except UserGroup.DoesNotExist:
        raise UserNotInGroupException(f'{user_id} id is not in {group_id} id')

    if user_group_obj.is_admin != True:
        raise UserIsNotAdminException(f'{user_id} is not admin in {group_id}')

    try:
        member_group_obj = UserGroup.objects.get(
            user__id=new_member_id, group__id=group_id)
    except UserGroup.DoesNotExist:
        group_obj.members.add(new_member_obj)
        group_obj.save()

# add_member_to_group(34,213,4)
# UserIsNotAdminException : 34 is not admin in 4


def remove_member_from_group(user_id, member_id, group_id):
    try:
        group_obj = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise InvalidGroupException(group_id=group_id)

    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        member_obj = User.objects.get(id=member_id)
    except User.DoesNotExist:
        raise InvalidMemberException(f'{member_id} id not in database')

    try:
        user_group_obj = UserGroup.objects.get(
            user__id=member_id, group__id=group_id)
    except UserGroup.DoesNotExist:
        raise UserNotInGroupException(
            f'{member_id} id is not in {group_id} id')
    
    if user_group_obj.is_admin != True:
        if user_id != member_id:
            raise UserIsNotAdminException(f'{user_id} is not admin in {group_id}')

    group_obj.members.remove(member_obj)
    group_obj.save()


# remove_member_from_group(34,213,4)
# UserIsNotAdminException : 34 is not admin in 4


def make_member_as_admin(user_id, member_id, group_id):
    try:
        group_obj = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise InvalidMemberException(f'{group_id} id not in database')

    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        member_obj = User.objects.get(id=member_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{member_id} id not in database')

    try:
        user_group_obj = UserGroup.objects.get(
            user__id=user_id, group__id=group_id)
    except UserGroup.DoesNotExist:
        raise UserNotInGroupException(f'{user_id} id is not in {group_id} id')

    try:
        member_group_obj = UserGroup.objects.get(
            user__id=member_id, group__id=group_id)
    except UserGroup.DoesNotExist:
        raise UserNotInGroupException(f'{user_id} id is not in {group_id} id')

    if user_group_obj.is_admin != True:
        raise UserIsNotAdminException(f'{user_id} is not admin in {group_id}')

    member_group_obj.is_admin = True
    member_group_obj.save()

# make_member_as_admin(34,7,4)


def create_group_post(user_id, post_content, group_id=None):
    """
    :returns: post_id
    """
    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        group_obj = None
        group_obj = Group.objects.get(id=group_id)
    except:
        pass

    current_datetime = datetime.now()
    post_obj = Post.objects.create(
        content=post_content,
        posted_by=user_obj,
        posted_at=current_datetime,
        group=group_obj
    )

    return post_obj.id

# print(create_post(34,"Just checked 34's post about his name reveal",4))


def get_group_feed(user_id, group_id, offset, limit):
    """
    :return: [
    {
        "post_id": 1,
        "posted_by": {
            "name": "iB Cricket",
            "user_id": 1,
            "profile_pic": "https://dummy.url.com/pic.png"
        },
        "posted_at": "2019-05-21 20:21:46.810366"
        "post_content": "Write Something here...",
        "reactions": {
            "count": 10,
            "type": ["HAHA", "WOW"]
        },
        "comments": [
            {
                "comment_id": 1
                "commenter": {
                    "user_id": 2,
                    "name": "Yuri",
                    "profile_pic": "https://dummy.url.com/pic.png"
                },
                "commented_at": "2019-05-21 20:22:46.810366",
                "comment_content": "Nice game...",
                "reactions": {
                    "count": 1,
                    "type": ["LIKE"]
                },
                "replies_count": 1,
                "replies": [{
                    "comment_id": 2
                    "commenter": {
                        "user_id": 1,
                        "name": "iB Cricket",
                        "profile_pic": "https://dummy.url.com/pic.png"
                    },
                    "commented_at": "2019-05-21 20:22:46.810366",
                    "comment_content": "Thanks...",
                    "reactions": {
                        "count": 1,
                        "type": ["LIKE"]
                    },
                }]
            },
            ...
        ],
        "comments_count": 3,
    }
    ]
    """
    if offset < 0:
        raise InvalidOffSetValueException(f'{offset} is less then 0')

    if limit < 0:
        raise InvalidLimitSetValueException(f'{limit} is less then 0')
    try:
        group_obj = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise InvalidGroupException(f'{group_id} id not in database')

    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise InvalidUserException(f'{user_id} id not in database')

    try:
        user_group_obj = UserGroup.objects.get(
            user__id=user_id, group__id=group_id)
    except UserGroup.DoesNotExist:
        raise UserNotInGroupException(f'{user_id} id is not in {group_id} id')

    # Variables to work with group_id, offset, limit
    post_objects = list(Post.objects.filter(group__id=group_id).values(
        post_id=F('id'),
        name=F('posted_by__name'),
        user_id=F('posted_by__id'),
        profile_pic=F('posted_by__profile_pic'),
        posted_at=F('posted_at'),
        post_content=F('content'),
    ))

    post_ids = [post['post_id'] for post in post_objects]

    comment_objects = Comment.objects.filter(Q(post__id__in=post_ids) & Q(parent_comment=None)).values(
        comment_id=F('id'),
        user_id=F('commented_by__id'),
        name=F('commented_by__name'),
        profile_pic=F('commented_by__profile_pic'),
        comment_content=F('content'),
    )

    comment_ids = [comment['comment_id'] for comment in comment_objects]

    # reply_objects = Comment.objects.filter(parent_comment__in=comment_ids).values(
    #     comment_id=F('id'),
    #     user_id=F('commented_by__id'),
    #     name=F('commented_by__name'),
    #     profile_pic=F('commented_by__profile_pic'),
    #     comment_content=F('content'),
    # )
    
    # I have a funtion to get replies to any comments

    comment_reaction_objects = CommentReaction.objects.filter(comment__id__in=comment_ids).values(
        'comment__id', 'reaction'
    ).annotate(Count('comment__id'))

    """
    :return: [
    {
        "post_id": 1,
        "posted_by": {
            "name": "iB Cricket",
            "user_id": 1,
            "profile_pic": "https://dummy.url.com/pic.png"
        },
        "posted_at": "2019-05-21 20:21:46.810366"
        "post_content": "Write Something here...",
        "reactions": {
            "count": 10,
            "type": ["HAHA", "WOW"]
        },
        "comments": [
            {
                "comment_id": 1
                "commenter": {
                    "user_id": 2,
                    "name": "Yuri",
                    "profile_pic": "https://dummy.url.com/pic.png"
                },
                "commented_at": "2019-05-21 20:22:46.810366",
                "comment_content": "Nice game...",
                "reactions": {
                    "count": 1,
                    "type": ["LIKE"]
                },
                "replies_count": 1,
                "replies": [{
                    "comment_id": 2
                    "commenter": {
                        "user_id": 1,
                        "name": "iB Cricket",
                        "profile_pic": "https://dummy.url.com/pic.png"
                    },
                    "commented_at": "2019-05-21 20:22:46.810366",
                    "comment_content": "Thanks...",
                    "reactions": {
                        "count": 1,
                        "type": ["LIKE"]
                    },
                }]
            },
            ...
        ],
        "comments_count": 3,
    }
    ]
    """


def get_posts_with_more_comments_than_reactions():
    """
    :returns: list of post_ids
    """
    comment_counts = Comment.objects.all().values(
        'post__id').annotate(Count('content'))
    reaction_counts = PostReaction.objects.all().values(
        'post__id').annotate(Count('reaction'))
    print(len(comment_counts), len(reaction_counts))

    cached_comment_count = {}
    for commnet_count in comment_counts:
        cached_comment_count[commnet_count['post__id']
                             ] = commnet_count['content__count']

    cached_reaction_count = {}
    for reaction_count in reaction_counts:
        cached_reaction_count[reaction_count['post__id']
                              ] = reaction_count['reaction__count']

    more_comments_post_ids = []
    for post_id in cached_comment_count:
        if cached_comment_count.get(post_id, 0) > cached_reaction_count.get(post_id, 0):
            more_comments_post_ids.append(post_id)

    return more_comments_post_ids

# print(get_posts_with_more_comments_than_reactions())


def get_user_posts(user_id):
    """
    :return: [
    {
        "post_id": 1,
        "group": {
            "group_id": 1,
            "name": "Group Name"
        },
        "posted_by": {
            "name": "iB Cricket",
            "user_id": 1,
            "profile_pic": "https://dummy.url.com/pic.png"
        },
        "posted_at": "2019-05-21 20:21:46.810366"
        "post_content": "Write Something here...",
        "reactions": {
            "count": 10,
            "type": ["HAHA", "WOW"]
        },
        "comments": [
            {
                "comment_id": 1
                "commenter": {
                    "user_id": 2,
                    "name": "Yuri",
                    "profile_pic": "https://dummy.url.com/pic.png"
                },
                "commented_at": "2019-05-21 20:22:46.810366",
                "comment_content": "Nice game...",
                "reactions": {
                    "count": 1,
                    "type": ["LIKE"]
                },
                "replies_count": 1,
                "replies": [{
                    "comment_id": 2
                    "commenter": {
                        "user_id": 1,
                        "name": "iB Cricket",
                        "profile_pic": "https://dummy.url.com/pic.png"
                    },
                    "commented_at": "2019-05-21 20:22:46.810366",
                    "comment_content": "Thanks...",
                    "reactions": {
                        "count": 1,
                        "type": ["LIKE"]
                    },
                }]
            },
            ...
        ],
        "comments_count": 3,
    }
    ]
    """


def get_silent_group_members(group_id):
    """
    """
    try:
        group_obj = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        raise InvalidMemberException(f'{group_id} id not in database')

    user_ids = list(UserGroup.objects.filter(
        group__id=group_id).values_list('user__id', flat=True))
    user_ids_with_posts = list(Post.objects.filter(Q(group__id=group_id) & Q(
        posted_by__id__in=user_ids)).values_list('posted_by__id', flat=True))
    user_ids_with_posts = set(user_ids_with_posts)

    user_ids_without_post = []
    for user_id in user_ids:
        if user_id not in user_ids_with_posts:
            user_ids_without_post.append(user_id)

    return user_ids_without_post

# print(get_silent_group_members(4))
