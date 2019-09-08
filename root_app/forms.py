from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AllTracksForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    submit = SubmitField('Create Playlist')

class ActionForm(FlaskForm):
    all_tracks = SubmitField('All Tracks Playlist')
    bpm = SubmitField('Playlists by BPM')
    key = SubmitField('Playlists by Key')

class BPMForm(FlaskForm):
    bpm = SelectField('BPM', coerce = int, validators = [DataRequired()])
    submit = SubmitField('Create Playlist')
