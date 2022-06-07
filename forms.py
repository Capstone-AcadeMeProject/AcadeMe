from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length, ValidationError

from enum import Enum


class ForumForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Anxiety', 'Anxiety'),
            ('Stress', 'Stress'),
            ('Relationships', 'Relationships'),
            ('Loneliness', 'Loneliness'),
            ('Grief', 'Grief'),
            ('Other', 'Other'),
        ]
    )

    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )



class ListenerForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    phone = StringField(
        # DONE implement validation logic for state
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
          choices=[
            ('Anxiety', 'Anxiety'),
            ('Stress', 'Stress'),
            ('Relationships', 'Relationships'),
            ('Loneliness', 'Loneliness'),
            ('Grief', 'Grief'),
            ('Other', 'Other'),
        ]
     )


    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

