from lib.classes.user import User


class Status:
    def __init__(self, status):
        self.text = status.text
        self.id = status.id
        self.retweeted = status.retweeted
        self.source = status.source
        self.in_reply_to_screen_name = status.in_reply_to_screen_name
        self.retweet_count = status.retweet_count
        self.in_reply_to_user_id_str = status.in_reply_to_user_id_str
        self.in_reply_to_status_id_str = status.in_reply_to_status_id_str
        self.created_at = status.created_at
        self.author = User(status.author)
        self.user = User(status.user)

    def as_dict(self):
        return {
            "text": self.text,
            "id": self.id,
            "retweeted": self.retweeted,
            "source": self.source,
            "in_reply_to_screen_name": self.in_reply_to_screen_name,
            "retweet_count": self.retweet_count,
            "in_reply_to_user_id_str": self.in_reply_to_user_id_str,
            "in_reply_to_status_id_str": self.in_reply_to_status_id_str,
            "created_at": self.created_at,
            "author": User(self.author).as_dict(),
            "user": User(self.user).as_dict()
        }