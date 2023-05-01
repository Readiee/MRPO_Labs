from flask import Flask, request, jsonify, render_template, redirect
import json

import models
import repositories
import services
import unit_of_work
import views

app = Flask(__name__)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        uow = unit_of_work.SqlAlchemyUnitOfWork()
        user_id = services.create_user(uow, name, email, password)

        return redirect(f'/users/{user_id}', code=301, Response=None)

    else:
        return render_template('create_user.html')


@app.route('/users', methods=['GET'])
def show_users():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    all_users = views.get_users(uow)

    if not all_users:
        return 'Not found', 404
    return jsonify(all_users), 200


@app.route('/users/<user_id>', methods=['GET'])
def user_view(user_id):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user = views.get_user_by_id(user_id, uow)
    if not user:
        return 'Not found', 404
    return render_template('user.html', user=user)

#
# @app.route('/group_chats', methods=['GET'])
# def show_group_chats():
#     uow = unit_of_work.SqlAlchemyUnitOfWork()
#     all_group_chats = views.get_group_chats(uow)
#
#     if not all_group_chats:
#         return 'Not found', 404
#     return jsonify(all_group_chats), 200
#
#
# @app.route('/group_chats/<group_chat_id>', methods=['GET'])
# def group_chat_view(group_chat_id):
#     uow = unit_of_work.SqlAlchemyUnitOfWork()
#     group_chat = views.get_group_chat_by_id(group_chat_id, uow)
#     if not group_chat:
#         return 'Not found', 404
#     return render_template('group_chat.html', group_chat=group_chat)


if __name__ == '__main__':
    app.run(debug=True)
