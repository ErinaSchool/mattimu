from app import db

from app.models.mypage import Mypage

from sqlalchemy.exc import SQLAlchemyError


def find_all() -> [Mypage]:
    return Mypage.query.all()


def find_one(mypage_id: int) -> Mypage:
    if mypage_id is None:
        raise Exception
    return Mypage.query.filter_by(id=mypage_id).first()


def save(mypage_id: int, user_id: int, data: {}) -> Mypage:
    try:
        if mypage_id is None:
            mypage = Mypage.from_args(
                data.get('user_name'),
                data.get('friend_code'),
                data.get('profile'),
                data.get('before_comment'),
                data.get('after_comment'),
                user_id
            )
            db.session.add(mypage)
        else:
            mypage = find_one(mypage_id)
            mypage.user_name = data.get('user_name')
            mypage.friend_code = data.get('friend_code')
            mypage.profile = data.get('profile')
            mypage.before_comment = data.get('before_comment')
            mypage.after_comment = data.get('after_comment')
            mypage.user_id = user_id
        db.session.commit()
        return mypage
    except SQLAlchemyError:
        raise Exception


def delete(mypage_id: int) -> bool:
    if mypage_id is None:
        raise Exception
    try:
        mypage = find_one(mypage_id)
        db.session.delete(mypage)
        db.session.commit()
        return True
    except SQLAlchemyError:
        raise Exception