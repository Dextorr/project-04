from flask import Blueprint, jsonify, request
from models.user import User, UserSchema
from models.jam import Jam, JamSchema
from models.synth import Synth
from models.drum import Drum
from models.beat import Beat
from models.poly import Poly
from models.poly_beat import PolyBeat

api = Blueprint('auth', __name__)
user_schema = UserSchema()

def new_jam(user):
    print('new_jam')

    jam = Jam(jam_name='New Jam', created_by=user, exported=False)
    jam.save()

    print('MonoSynth')

    MonoSynth = Synth(synth_name='MonoSynth', jam=jam)
    MonoSynth.save()

    print('DrumMachine')
    DrumMachine = Drum(synth_name='DrumMachine', jam=jam)
    DrumMachine.save()

    print('Beats')
    for i in range(16):
        # print(beat['pitch'])
        mono_beat = Beat(
            step=i,
            pitch="C3",
            duration="32n",
            velocity="100",
            synth=MonoSynth
        )
        mono_beat.save()

    poly_list = []
    poly_beat_list = []
    for i in range(16):
        poly = Poly(step=i, drum=DrumMachine)
        poly.save()
        # poly_list.append(poly)
        for j in range(4):
            poly_beat = PolyBeat(
                step=i,
                voice=j,
                pitch="C3",
                duration="16n",
                velocity="0",
                poly=poly
            )
            poly_beat.save()
            # poly_beat_list.append(poly_beat)

    # db.session.bulk_save_objects(poly_list)
    # db.session.bulk_save_objects(poly_beat_list)


@api.route('/register', methods=['POST'])
def register():
    user, errors = user_schema.load(request.get_json())

    if errors:
        return jsonify(errors), 422

    user.save()

    print('about to make jam')
    new_jam(user)


    return jsonify({'message': 'Registration successful'}), 201


@api.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not user.validate_password(data.get('password', '')):
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify({
        'message': 'Welcome back {}!'.format(user.username),
        'token': user.generate_token()
    })
