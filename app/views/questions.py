from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.services import question_service

questions = Blueprint('questions', __name__)


@questions.route('/')
@login_required  # ログインしていないと表示できないようにする
def find_all():
    questions = question_service.find_all()
    return render_template('questions/index.html', questions=questions)


@questions.route('/<question_id>')
@login_required  # ログインしていないと表示できないようにする
def find_one(question_id: int):
    question = question_service.find_one(question_id)
    return render_template('questions/show.html', question=question)


@questions.route('/add', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def add():
    try:
        if request.method == 'GET':
            return render_template('questions/post.html')
        else:
            # postとputを一つのメソッドでできるようにquestion_idを入れてあるが、
            # 新規作成時はNoneにしておく。二つ目のrequet.formはformから送られてくる情報をそのままserviceに渡す
            # current_userはflask_loginの機能で、現在ログインしているユーザーの情報を取得することができる。
            question = question_service.save(None, current_user.id, request.form)
            if question is None:
                flash('プロフィールを追加することができませんでした。')
                return redirect(url_for('questions.add'))
            flash('プロフィールを追加しました。')
            return redirect(url_for('questions.find_all'))
    except Exception:
        flash('プロフィールを追加することができませんでした。')
        return redirect(url_for('questions.add'))


@questions.route('/update/<question_id>', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def update(question_id: int):
    try:
        if request.method == 'GET':
            question = question_service.find_one(question_id)
            return render_template('questions/update.html', question=question)
        else:
            question = question_service.save(question_id, current_user.id, request.form)
            if question is None:
                flash('プロフィールを修正することができませんでした。')
                return redirect(url_for('questions.update', question_id=question_id))
            flash('プロフィールを修正しました。')
            return redirect(url_for('questions.find_all'))
    except Exception:
        flash('プロフィールを修正することができませんでした。')
        return redirect(url_for('questions.update', question_id=question_id))


@questions.route('/delete/<question_id>', methods=['POST'])
@login_required  # ログインしていないと表示できないようにする
def delete(question_id: int):
    try:
        question_service.delete(question_id)
        flash('プロフィールを削除しました。')
        return redirect(url_for('questions.find_all'))
    except Exception:
        flash('プロフィールを削除することができませんでした。')
        return redirect(url_for('questions.find_all'))