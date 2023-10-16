from django.contrib import admin

from .models import User
from .models import PostReaction
from .models import CommentReaction
from .models import Post
from .models import Comment

admin.site.register(User)
admin.site.register(PostReaction)
admin.site.register(CommentReaction)
admin.site.register(Post)
admin.site.register(Comment)