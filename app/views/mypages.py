from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.services import mypage_service

mypages = Blueprint('mypages', __name__)


@mypages.route('/')
@login_required  # ログインしていないと表示できないようにする
def find_all():
    mypages = mypage_service.find_all()
    return render_template('mypages/index.html', mypages=mypages)


@mypages.route('/<mypage_id>')
@login_required  # ログインしていないと表示できないようにする
def find_one(mypage_id: int):
    mypage = mypage_service.find_one(mypage_id)
    return render_template('mypages/show.html', mypage=mypage)


@mypages.route('/add', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def add():
    try:
        if request.method == 'GET':
            return render_template('mypages/post.html')
        else:
            # postとputを一つのメソッドでできるようにquestion_idを入れてあるが、
            # 新規作成時はNoneにしておく。二つ目のrequet.formはformから送られてくる情報をそのままserviceに渡す
            # current_userはflask_loginの機能で、現在ログインしているユーザーの情報を取得することができる。
            mypage = mypage_service.save(None, current_user.id, request.form)
            if mypage is None:
                flash('プロフィールを追加することができませんでした。')
                return redirect(url_for('mypages.add'))
            flash('プロフィールを追加しました。')
            return redirect(url_for('mypages.find_all'))
    except Exception:
        flash('プロフィールを追加することができませんでした。')
        return redirect(url_for('mypages.add'))


@mypages.route('/update/<mypage_id>', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def update(mypage_id: int):
    try:
        if request.method == 'GET':
            mypage = mypage_service.find_one(mypage_id)
            return render_template('mypages/update.html', mypage=mypage)
        else:
            mypage = mypage_service.save(mypage_id, current_user.id, request.form)
            if mypage is None:
                flash('プロフィールを修正することができませんでした。')
                return redirect(url_for('mypages.update', mypage_id=mypage_id))
            flash('プロフィールを修正しました。')
            return redirect(url_for('mypages.find_all'))
    except Exception:
        flash('プロフィールを修正することができませんでした。')
        return redirect(url_for('mypages.update', mypage_id=mypage_id))


@mypages.route('/delete/<mypage_id>', methods=['POST'])
@login_required  # ログインしていないと表示できないようにする
def delete(mypage_id: int):
    try:
        mypage_service.delete(mypage_id)
        flash('プロフィールを削除しました。')
        return redirect(url_for('mypages.find_all'))
    except Exception:
        flash('プロフィールを削除することができませんでした。')
        return redirect(url_for('mypages.find_all'))