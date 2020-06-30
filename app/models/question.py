from app import db


# モデルに関する設定
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    body = db.Column(db.String(255))
    # Userに所有されている状態
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', name='user_id__question_id_fk'))

    @classmethod
    def from_args(cls, title: str, body: str, user_id: int):
        instance = cls()
        instance.title = title
        instance.body = body
        instance.user_id = user_id
        return instance