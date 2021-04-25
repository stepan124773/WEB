import flask
from flask import jsonify, request
from data import db_session
from data.user import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'surname', 'number',
                                    'address',
                                    ))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<id>')
def get_user(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == id).first()

    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users':
                users.to_dict(only=('id', 'name', 'surname', 'number',
                                    'address',
                                    ))

        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'number',
                  'address']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    users = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        number=request.json['number'],

        address=request.json['address'],

    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id==users_id).first()
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})
