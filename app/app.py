#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Episode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


class EpisodeResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        data = [
            {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number
            }
            for episode in episodes
        ]
        return data
    
class SingleEpisodeResource(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if episode:
            data = {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number,
                'guests': [
                    {
                        'id': appearance.guest.id,
                        'name': appearance.guest.name,
                        'occupation': appearance.guest.occupation
                    }
                    for appearance in episode.appearances
                ]
            }
            return data
        else:
            return {'error': 'Episode not found'}, 404

    def delete(self, id):
        episode = Episode.query.get(id)
        if episode:
            db.session.delete(episode)
            db.session.commit()
            return '', 204
        else:
            return {'error': 'Episode not found'}, 404
class GuestResource(Resource):
    def get(self):
        guests = Guest.query.all()
        data = [
            {
                'id': guest.id,
                'name': guest.name,
                'occupation': guest.occupation
            }
            for guest in guests
        ]
        return data

class AppearanceResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rating', type=int, required=True)
    parser.add_argument('episode_id', type=int, required=True)
    parser.add_argument('guest_id', type=int, required=True)

    def post(self):
        args = self.parser.parse_args()
        rating = args['rating']
        episode_id = args['episode_id']
        guest_id = args['guest_id']

        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)

        if not episode:
            return {'error': 'Episode not found'}, 404

        if not guest:
            return {'error': 'Guest not found'}, 404

        if not (1 <= rating <= 5):
            return {'errors': ['Validation error. Rating must be between 1 and 5 (inclusive).']}, 400

        appearance = Appearance(rating=rating, episode=episode, guest=guest)
        db.session.add(appearance)
        db.session.commit()

        response_data = {
            'id': appearance.id,
            'rating': appearance.rating,
            'episode': {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number
            },
            'guest': {
                'id': guest.id,
                'name': guest.name,
                'occupation': guest.occupation
            }
        }
        return response_data, 201
api.add_resource(EpisodeResource, '/episodes')
api.add_resource(SingleEpisodeResource, '/episodes/<int:id>')
api.add_resource(GuestResource, '/guests')
api.add_resource(AppearanceResource, '/appearances')'


if __name__ == '__main__':
    app.run(port=5555)
