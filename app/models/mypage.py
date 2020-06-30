from app import db


# モデルに関する設定
class Mypage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(15))
    friend_code = db.Column(db.String(14))
    profile = db.Column(db.String(255))
    before_comment = db.Column(db.String(30))
    after_comment = db.Column(db.String(30))
    # Userに所有されている状態
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', name='user_id__profile_id'))

    @classmethod
    def from_args(cls, user_name: str, friend_code: str, profile: str, before_comment: str, after_comment: str, user_id: int):
        instance = cls()
        instance.user_name = user_name
        instance.friend_code = friend_code
        instance.profile = profile
        instance.before_comment = before_comment
        instance.after_comment = after_comment
        instance.user_id = user_id
        return instance