import flask
from flask import jsonify, request
from data import db_session
from data.Ad import Ad

blueprint = flask.Blueprint(
    'ads_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/ads')
def get_ads():
    db_sess = db_session.create_session()
    ads = db_sess.query(Ad).all()
    return jsonify(
        {
            'ads':
                [item.to_dict(only=('id', 'name', 'address', 'description', 'number', 'category',
                                    'user_id',
                                    ))
                 for item in ads]
        }
    )


@blueprint.route('/api/ads/<id>')
def get_ad(id):
    db_sess = db_session.create_session()
    ads = db_sess.query(Ad).filter(Ad.id == id).first()

    if not ads:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'ads':
                ads.to_dict(only=('id', 'name', 'address', 'description', 'number', 'category',
                                  'user_id',
                                  ))

        }
    )


@blueprint.route('/api/ads', methods=['POST'])
def create_ads():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'address', 'description', 'number', 'category',
                  'user_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    ads = Ad(
        id=request.json['id'],
        name=request.json['name'],
        address=request.json['address'],
        description=request.json['description'],
        number=request.json['number'],
        category=request.json['category'],
        user_id=request.json['user_id']

    )
    db_sess.add(ads)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/ads/<int:ads_id>', methods=['DELETE'])
def delete_ads(ads_id):
    db_sess = db_session.create_session()
    ads = db_sess.query(Ad).get(ads_id)
    if not ads:
        return jsonify({'error': 'Not found'})
    db_sess.delete(ads)
    db_sess.commit()
    return jsonify({'success': 'OK'})
