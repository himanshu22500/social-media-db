from faker import Faker
import random
from pprint import pprint

# from .models import User
# from .models import Reaction
# from .models import Post
# from .models import Comment

fake = Faker()

def generate_user():
    users_list = []
    for i in range(1000):
        user_dict = {
            "name": fake.name(),
            "profile_pic":fake.image_url()
        }
        users_list.append(user_dict)
    return users_list

user_ids = [i for i in range(1,1001)]


def generate_post():
    post_list = []
    for i in range(3000):
        post_dict = {
            "content": fake.paragraph(nb_sentences=random.randint(5,40)),
            "posted_at": f"{random.randint(2000, 2023)}-{random.randint(1, 12)}-{random.randint(1, 28)}",
            "posted_by": random.choice(user_ids)
        }
        post_list.append(post_dict)
    return post_list

post_ids = [i for i in range(1,3001)]

parent_comments = [i for i in range(1,101)]

def generate_comment():
    comment_list = []
    for i in range(1000):
        comment_dict = {
            "content": fake.paragraph(nb_sentences=random.randint(5,20)),
            "commented_at": f"{random.randint(2000, 2023)}-{random.randint(1, 12)}-{random.randint(1, 28)}",
            "commented_by": random.choice(user_ids),
            "posted_at": random.choice(post_ids),
            "parent_comment": random.choice(parent_comments)
        }
        comment_list.append(comment_dict)
    return comment_list

# comment_list = generate_comment()

# users_list = generate_user()
# print("users_list = ", end="")
# pprint(users_list)


# post_list = generate_post()
# print("post_list = ", end="")
# pprint(post_list)


comment_list = generate_comment()
print("users_list = ", end="")
pprint(comment_list)