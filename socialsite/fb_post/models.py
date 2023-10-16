from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    profile_pic = models.TextField()

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, 
                                    through='UserGroup',
                                    through_fields=("group", "user")
                                )

    def __str__(self):
        return self.name

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

class Post(models.Model):
    content = models.TextField()
    posted_at = models.DateTimeField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    content = models.TextField()
    commented_at = models.DateTimeField()
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content


class PostReaction(models.Model):
    WOW = "WOW"
    LIT = "LIT"
    LOVE = "LOVE"
    HAHA = "HAHA"
    THUMBSUP = "THUMBS-UP"
    THUMBSDOWN = "THUMBS-DOWN"
    ANGRY = "ANGRY"
    SAD = "SAD"

    REACTION_CHOICES = [
        (WOW, "WOW"),
        (LIT, "LIT"),
        (LOVE, "LOVE"),
        (HAHA, "HAHA"),
        (THUMBSUP, "THUMBS-UP"),
        (THUMBSDOWN, "THUMBS-DOWN"),
        (ANGRY, "ANGRY"),
        (SAD, "SAD"),
    ]

    reaction = models.CharField(
        max_length=20,
        choices=REACTION_CHOICES,
        null=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reacted_at = models.DateField()
    reacted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.reaction


class CommentReaction(models.Model):
    WOW = "WOW"
    LIT = "LIT"
    LOVE = "LOVE"
    HAHA = "HAHA"
    THUMBSUP = "THUMBS-UP"
    THUMBSDOWN = "THUMBS-DOWN"
    ANGRY = "ANGRY"
    SAD = "SAD"

    REACTION_CHOICES = [
        (WOW, "WOW"),
        (LIT, "LIT"),
        (LOVE, "LOVE"),
        (HAHA, "HAHA"),
        (THUMBSUP, "THUMBS-UP"),
        (THUMBSDOWN, "THUMBS-DOWN"),
        (ANGRY, "ANGRY"),
        (SAD, "SAD"),
    ]

    reaction = models.CharField(
        max_length=20,
        choices=REACTION_CHOICES,
        null=True
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reacted_at = models.DateField()
    reacted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reaction


