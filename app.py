# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from datetime import date
import json
import os
import re
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from flask.globals import session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
# from requests import delete
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

Session(app)

socketio = SocketIO(app, manage_session=False)

# DONE: connect to a local postgresql database
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# Model generate by SQLAlchemy (db.create_all()) DONE, so no need to write sql commands to generate te tables.

      

class Forum(db.Model):
    __tablename__ = 'Forum'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    title = db.Column(db.String)
    look_for_counselor = db.Column(db.Boolean) # checkbox
    description = db.Column(db.String(500))
    # listeners = db.Column(db.String, db.ForeignKey('listener.id'), nullable=False)
    # TODO: QA.
   

class Listener(db.Model):
    __tablename__ = 'Listener'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    topic = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120)) # list. no type of list
    # image_link = db.Column(db.String(500))
    # website_link = db.Column(db.String(120))
    description = db.Column(db.String(500))
    # forum = db.relationship("Show", backref = db.backref("listener", lazy = True))
    # forum = db.relationship("Forum")





# db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def login():
  return render_template('pages/login.html')


@app.route('/category')
def index():
  return render_template('pages/category.html')


@app.route('/supports')
def homepage():
  return render_template('pages/home.html')


#  Forums
#  ----------------------------------------------------------------
@app.route('/forum')
def forum():
    fake_data=[
      {
    "topic": "Anxiety",  
    "forums": [{
      "id": 1,
      "title": "Fear to fail the exam",
      "description": "The algorithm course is too hard for me. I am anxious about the exam. Is anyone here can help me. Maybe We can form a study group. ",
    }]
    }, 
    {
    "topic": "Lonliness",
     "forums": [{
      "id": 2,
      "title": "Want to make new friends",
      "description": "I am new to New York and want to meet new people with same interest.",
    }]
    }, 
    {
    "topic": "Relationship",
     "forums": [{
      "id": 3,
      "title": "Just break up",
      "description": "Heartbroken",
    }]
    }
    ]
    return render_template('pages/forums.html', areas=fake_data)

@app.route('/forum/search', methods=['POST'])
def search_Forums():
  # DONE: num_upcoming_show
  # DONE: implement search on listeners with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   },
  #   {
  #     "id": 3,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 1,
  #   }]
  # }
  search_term = request.form.get('search_term', '')
  # print("search_term", search_term)
  search = "%{}%".format(search_term)
  search_res = Forum.query.filter(Forum.name.ilike(search))
  forum = search_res.all()
  # print(forum)
  count = search_res.count()
  data_list = []
  for Forum in forum:
        data_dict = {}
        data_dict["id"] = Forum.id
        data_dict["name"] = Forum.name
        # data_dict["num_upcoming_show"] = listener.
        
        data_list.append(data_dict)

  response = {
    "count" : count,
    "data": data_list
  }
  return render_template('pages/search_Forums.html', results=response, search_term= search_term)

@app.route('/forum/<int:Forum_id>')
def show_Forum(Forum_id):
  # shows the Forum page with the given Forum_id
  # DONE: replace with real Forum data from the forum table, 
  # TODo: using Forum_id in Show?
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "topic": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local listener to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "listener_id": 4,
      "listener_name": "Guns N Petals",
      "listener_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  # data_list = [data1, data2, data3] # just for test
  data_list = []
  forum = Forum.query.all()
  for Forum in forum:
    data_dict = {}
    data_dict["id"] = Forum.id
    data_dict["title"] = Forum.title
    data_dict["topic"] = Forum.topic
    data_dict["seeking_counselors"] = Forum.look_for_counselors
    data_dict["image_link"] = Forum.image_link
    # print(past_shows.count(), coming_shows.count() )
    data_list.append(data_dict)
    # print("genre", Forum.genres)
  data = list(filter(lambda d: d['id'] == Forum_id, data_list))[0]
  # print("data",data)
  return render_template('pages/show_Forum.html', Forum=data)

#  Create Forum
#  ----------------------------------------------------------------

@app.route('/forum/create', methods=['GET'])
def create_Forum_form():
  form = ForumForm()
  return render_template('forms/new_Forum.html', form=form)

@app.route('/forum/create', methods=['POST'])
def create_Forum_submission():
  # DONE: insert form data as a new Forum record in the db, instead
  print("requesr.form",request.form)
  form = ForumForm()
  if 'seeking_talent' in request.form:
      look_for_counselor= True
  else: 
      look_for_counselor = False
  Forum =  Forum(
    title= form.title.data, 
    topic = form.topic.data,
    image_link = form.image_link.data,
    look_for_counselor = look_for_counselor,
    description = form.seeking_description.data,
    )
  db.session.add(Forum)
  try:
    db.session.commit()
    flash('Forum ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:  
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Forum ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    print(e)
    flash('An error occurred. Forum ' + request.form['name'] + ' could not be listed.') # did not work when the seeking_talent is y.
    db.session.rollback()
  return render_template('pages/home.html')

#


#  listeners
#  ----------------------------------------------------------------
@app.route('/listeners')
def listeners():
  # DONE: replace with real data returned from querying the database
  fake_data=[{
    "id": 4,
    "name": "Jessica Healy",
  }, {
    "id": 5,
    "name": "Jamel Burroughs",
  }, {
    "id": 6,
    "name": "Claire Golden",
  }, { 
    "id": 7,
    "name": "Alexa Wallerstein",
  }]
  listeners = Listener.query.all()
  data_list = []
  if not listeners:
      data_list = [{"name":"there is no listener right now"}]  
  else:
    for listener in listeners:
      data_dict = {}
      data_dict["id"] = listener.id
      data_dict["name"] = listener.name
      data_list.append(data_dict)
  return render_template('pages/listeners.html', listeners=fake_data)

@app.route('/listeners/search', methods=['POST'])
def search_listeners():
  # DONE: num_upcoming_show
  # DONE: implement search on listeners with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  search_term = request.form.get('search_term', '')
  print("search_term", search_term)
  search = "%{}%".format(search_term)
  search_res = listener.query.filter(listener.name.ilike(search))
  listeners = search_res.all()
  print(listeners)
  count = search_res.count()
  data_list = []
  # Session = sessionmaker(bind = engine)
  # session = Session()
  # session.query(show).all()
  for listener in listeners:
        data_dict = {}
        data_dict["id"] = listener.id
        data_dict["name"] = listener.name
        coming_shows = Show.query.filter(
          and_(Show.Forum_id == listener.id,
          func.date(Show.start_time)  >= datetime.now()
          )
        )
        data_dict["num_upcoming_show"] = coming_shows.count()
        data_list.append(data_dict)

  response = {
    "count" : count,
    "data": data_list
  }
  return render_template('pages/search_listeners.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/listeners/<int:listener_id>')
def show_listener(listener_id):
  # DONE:genre, show
  # shows the listener page with the given listener_id
  # DONE: replace with real listener data from the listener table, using listener_id
  f_data1={
    "id": 4,
    "name": "Jessica Healy",
    "genres": ["CBT"],
    "topic": "Stress",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_Forum": True,
    "seeking_description": "I specialize in evaluating children and adults who are struggling to succeed in school and at work. If you are hungry for personal growth and willing to work at it, the breakthrough you are seeking is within reach at Academe",
    "image_link": "img/thrapy-male.jpeg",
    "past_shows": [{
      "Forum_id": 1,
      "Forum_name": "The Musical Hop",
      "Forum_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  
  data_list = []
  listeners = Listener.query.all()
    
  for listener in listeners:
    data_dict = {}
    data_dict["id"] = listener.id
    data_dict["name"] = listener.name
    if listener.genres:
        genres = listener.genres.lstrip("{")
        genres = genres.rstrip("}")
        # print(genres)
        data_dict["genres"] = list(genres.split(","))  # ["Jazz", "Reggae", "Swing", "Classical", "Folk"]
        # genres = [genre for genre in listener.genres]
        # print("this listener's genre", listener.name, listener.genres)
    else:
        genres = "None"  # default
    data_dict["topic"] = listener.topic
    data_dict["state"] = listener.state
    data_dict["phone"] = listener.phone
    data_dict["seeking_Forum"] = listener.look_for_Forums 
    data_dict["image_link"] = listener.image_link 
    data_dict["website_link"] = listener.website_link 
    #todo: past_shows, upcoming shows, "past_shows_count": 1,"upcoming_shows_count": 1, >show.time
    # past_show
    past_shows_list = []
    past_shows = Show.query.filter(
      and_(Show.Forum_id == listener.id,
      func.date(Show.start_time)  < datetime.now()
      )
    )
    for past_show in past_shows:
      past_show_dict = {}
      past_show_dict["Forum_id"] = past_show.Forum_id
      past_show_dict["Forum_name"] = past_show.Forum.name
      past_show_dict["Forum_image_link"] = past_show.Forum.image_link
      past_show_dict["start_time"] = str(past_show.start_time)
      past_shows_list.append(past_show_dict) 
    # upcoming_show    
    coming_shows = Show.query.filter(
          and_(Show.Forum_id == listener.id,
          func.date(Show.start_time)  >= datetime.now()
          )
        )
    coming_shows_list = []
    for coming_show in coming_shows:
      coming_show_dict = {}
      coming_show_dict["Forum_id"] = coming_show.Forum_id
      coming_show_dict["Forum_name"] = coming_show.Forum.name
      coming_show_dict["Forum_image_link"] = coming_show.Forum.image_link
      coming_show_dict["start_time"] = str(coming_show.start_time)
      coming_shows_list.append(coming_show_dict)
    data_dict["past_shows"] = past_shows_list  
    data_dict["upcoming_shows"] = coming_shows_list
    data_dict["past_shows_count"] = past_shows.count() 
    data_dict["upcoming_shows_count"] = coming_shows.count()

    
    data_list.append(data_dict)
    # print("genres", listener.genres)

  # data = list(filter(lambda d: d['id'] == listener_id, data_list))[0]
  return render_template('pages/show_listener.html', listener=f_data1)







#  Update
#  ----------------------------------------------------------------
@app.route('/listeners/<int:listener_id>/edit', methods=['GET'])
def edit_listener(listener_id):
  form = ListenerForm()
  # listener={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "topic": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_Forum": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  listener = listener.query.filter_by(id = listener_id).all() 
  # print("listener", listener, listener[0])
  # DONE: populate form with fields from listener with ID <listener_id>
  form.name.data = listener[0].name
  form.topic.data = listener[0].topic
  form.phone.data = listener[0].phone 
  # print("phone", listener[0].phone)
  form.genres.data = listener[0].genres
  form.image_link.data = listener[0].image_link
  form.website_link.data = listener[0].website_link
  form.seeking_counselor.data = listener[0].look_for_counselor
  form.seeking_description.data = listener[0].description
  return render_template('forms/edit_listener.html', form=form, listener=listener[0])

@app.route('/listeners/<int:listener_id>/edit', methods=['POST'])
def edit_listener_submission(listener_id):
  # DONE: take values from the form submitted, and update existing
  # listener record with ID <listener_id> using the new attributes
  # update
  print("request",request.form)
  listener =  listener.query.get(listener_id)
  listener.name= request.form['name'] 
  listener.topic = request.form['topic']
  listener.phone = request.form['phone']
  listener.genres = request.form.getlist('genres')
  listener.image_link = request.form['image_link']
  print("img", listener.image_link)
  listener.website_link = request.form['website_link']
  if 'seeking_Forum' in request.form:
      look_for_counselor = True
  else: 
      look_for_counselor = False
  listener.look_for_counselor = look_for_counselor
  listener.description = request.form['seeking_description']
  db.session.add(listener)
  db.session.commit()
  print("success")
  return redirect(url_for('show_listener', listener_id=listener_id))

@app.route('/forum/<int:Forum_id>/edit', methods=['GET'])
def edit_Forum(Forum_id):
  form = ForumForm()
  # Forum={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "topic": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local listener to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  Forum = Forum.query.filter_by(id = Forum_id).all() 
  print("Forum", Forum, Forum[0])
  # DONE: populate form with values from Forum with ID <Forum_id>
  form.name.data = Forum[0].name
  form.topic.data = Forum[0].topic
  form.state.data = Forum[0].state 
  form.address.data = Forum[0].address 
  form.phone.data = Forum[0].phone 
  # print("phone", Forum[0].phone)
  form.genres.data = Forum[0].genres
  form.facebook_link.data = Forum[0].facebook_link
  form.image_link.data = Forum[0].image_link
  form.website_link.data = Forum[0].website_link
  form.seeking_talent.data = Forum[0].look_for_listeners
  form.seeking_description.data = Forum[0].description
  return render_template('forms/edit_Forum.html', form=form, Forum=Forum[0])

@app.route('/forum/<int:Forum_id>/edit', methods=['POST'])
def edit_Forum_submission(Forum_id):
  # DONE: take values from the form submitted, and update existing
  # Forum record with ID <Forum_id> using the new attributes
  print("request",request.form)
  Forum=  Forum.query.get(Forum_id)
  Forum.name= request.form['name'] 
  Forum.topic = request.form['topic']
  Forum.state = request.form['state']
  Forum.address = request.form['address']
  Forum.phone = request.form['phone']
  Forum.genres = request.form.getlist('genres')
  Forum.facebook_link = request.form['facebook_link']
  Forum.image_link = request.form['image_link']
  print("img", Forum.image_link)
  Forum.website_link = request.form['website_link']
  if 'seeking_talent' in request.form:
      look_for_listeners = True
  else: 
      look_for_listeners = False
  # print(look_for_listeners)    
  Forum.seeking_talent = look_for_listeners
  Forum.description = request.form['seeking_description']
  db.session.add(Forum)
  db.session.commit()
  print("success")
  return redirect(url_for('show_Forum', Forum_id=Forum_id))

#  Create listener
#  ----------------------------------------------------------------

@app.route('/listeners/create', methods=['GET'])
def create_listener_form():
  form = ListenerForm()
  return render_template('forms/new_listener.html', form=form)

@app.route('/listeners/create', methods=['POST'])
def create_listener_submission():
  # called upon submitting the new listener listing form
  # DONE: insert form data as a new Forum record in the db, instead
  print(request.form)
  if 'seeking_Forum' in request.form:
      look_for_Forums = True
  else: 
      look_for_Forums = False
  # print(request.form.getlist('genres'))    
  listener =  listener(
    name= request.form['name'], 
    topic = request.form['topic'],
    state = request.form['state'],
    phone = request.form['phone'],
    genres = request.form.getlist('genres'),
    image_link = request.form['image_link'],
    website_link = request.form['website_link'],
    look_for_Forums = look_for_Forums,
    description = request.form['seeking_description'],
    )
  db.session.add(listener)
  # TODO?: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  try:
    db.session.commit()
    flash('listener ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:  
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. listener ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/  
    print(e)
    flash('An error occurred. listener ' + request.form['name'] + ' could not be listed.') # did not work when the seeking_talent is y.
    db.session.rollback()  
 
  return render_template('pages/home.html')

# call
@app.route('/listeners/<int:listener_id>/call')
def call(listener_id):
  print("callllll")
  return render_template('pages/call.html')


#  chat
#  ----------------------------------------------------------------

@app.route('/listeners/<int:listener_id>/chat', methods = ['GET','POST'])
def chat(listener_id):
  session['username'] = 'test_username'
  session['room'] = 'test_room'
  return render_template('pages/chat.html', session = session)

@socketio.on('join', namespace='/listeners/<int:listener_id>/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/listeners/<int:listener_id>/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/listeners/<int:listener_id>/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# # Default port:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    socketio.run(app,host='127.0.0.1', port=port)


# Or specify port manually:
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 8080))
#     app.run(host='0.0.0.0', port=port)

