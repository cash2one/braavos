import datetime
from flask import current_app as app

from libs.signals import add_comment_signal
from models.comment import Comment


class CommentMixin():

    def add_comment(self, user, msg):
        c = Comment.add(self.target_type, self.target_id, msg, user, datetime.datetime.now())
        if app.config['MAIL_DEBUG'] is not True:
            add_comment_signal.send(c)

    def get_comments(self):
        return Comment.query.filter_by(target_type=self.target_type,
                                       target_id=self.target_id).order_by(Comment.create_time.desc())

    def get_mention_users(self, except_user):
        return list(set([c.creator for c in self.get_comments() if c.creator is not except_user]))
