class InvalidUserException(Exception):
    pass

class InvalidPostContent(Exception):
    pass

class InvalidCommentContent(Exception):
    pass

class InvalidReplyContent(Exception):
    pass

class InvalidReactionTypeExpections(Exception):
    pass

class UserCannotDeletePostException(Exception):
    pass

class InvalidPostException(Exception):
    pass

class InvalidCommentException(Exception):
    pass

class InvalidReplyContent(Exception):
    pass

class InvalidReactionTypeException(Exception):
    pass

class UserCannotDeletePostException(Exception):
    pass

class InvalidMemberException(Exception):
    pass

class InvalidGroupException(Exception):
    def __init__(self, group_id: int):
        self.group_id = group_id

class UserNotInGroupException(Exception):
    pass

class UserIsNotAdminException(Exception):
    pass

class InvalidOffSetValueException(Exception):
    pass

class InvalidLimitSetValueException(Exception):
    pass

class InvalidGroupNameException(Exception):
    pass