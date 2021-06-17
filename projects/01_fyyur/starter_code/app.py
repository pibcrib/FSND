#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from models import *
from flask import render_template, request, Response, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

    # handled in models.py

#----------------------------------------------------------------------------#
# Models.

    #imported from models.py

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
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues(): #DONE
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #       ***I didn't bother implementing num_shows here since the view at the route doesn't display this information,
  #             this is implemented on the each venue's distinct page

  locations = Venue.query.distinct('city', 'state').all()
  def get_venue_data(venue_list):
      data = []
      for v in venue_list:
          a_venue = {
            'id': v.id,
            'name': v.name}
          data.append(a_venue)

      return data

  data = [{
            'city': location.city,
            'state': location.state,
            'venues': get_venue_data
                (db.session.query(Venue.name, Venue.id).filter_by(city=location.city).filter_by(state=location.state).all())}
        for location in locations]

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues(): #DONE!!!
  # Implements search on artists' names with partial string search. Ensures it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  venues_match = db.session.query(Venue.id, Venue.name).filter(Venue.name.ilike(f'%{search_term}%')).all()
  response = {
    "count": len(venues_match),
    "data": [{'id':v.id, 'name': v.name} for v in venues_match]
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id): #DONE!!!
  # shows the venue page with the given venue_id

  now = datetime.utcnow()
  a_venue = Venue.query.get(venue_id)
  upcoming_shows = db.session.query(Show).join(Venue, Show.venue_id == venue_id).filter(Show.start_time>now).all()
  past_shows = db.session.query(Show).join(Venue, Show.venue_id == venue_id).filter(Show.start_time<now).all()
  data = {
    'id': a_venue.id,
    "name": a_venue.name,
    "genres": a_venue.genres,
    "address": a_venue.address,
    "city": a_venue.city,
    "state": a_venue.state,
    "phone": a_venue.phone,
    "website": a_venue.website,
    "facebook_link": a_venue.facebook_link,
    "seeking_talent": a_venue.seeking_talent,
    "seeking_description": a_venue.seeking_description,
    "image_link": a_venue.image_link,
    "past_shows": [{
        "artist_id": a_show.artist_id,
        "artist_name": a_show.artist.name,
        "artist_image_link": a_show.artist.image_link,
        "start_time": (a_show.start_time).strftime("%y-%m-%d %H:%M:%S")
        } for a_show in past_shows],
    "upcoming_shows":  [{
        "artist_id": a_show.artist_id,
        "artist_name": a_show.artist.name,
        "artist_image_link": a_show.artist.image_link,
        "start_time": (a_show.start_time).strftime("%y-%m-%d %H:%M:%S")
        } for a_show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)}

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission(): #DONE

  form = VenueForm(meta={'csrf': False})
  #'if' prints errors if invalid data is submitted and rerenders html template
  if not(form.validate_on_submit()):
      for error in form.errors.values():
          flash(error[0])

      return render_template('forms/new_venue.html', form=form)

  else:
      try:
          new_venue = Venue(
              name = request.form.get('name'),
              city = request.form.get('city'),
              state = request.form.get('state'),
              address = request.form.get('address'),
              phone = request.form.get('phone'),
              genres = request.form.getlist('genres'),
              image_link = request.form.get('image_link'),
              website = request.form.get('website'),
              facebook_link = request.form.get('facebook_link'),
              seeking_talent = True if request.form.get('seeking_talent')=='y' else False,
              seeking_description = request.form.get('seeking_description'))

          db.session.add(new_venue)
          db.session.commit()
          flash('Venue ' + request.form.get('name') + ' was successfully listed!')

      except Exception as e:
          db.session.rollback()
          print(e)
          flash('An error occurred. Venue ' +  request.form.get('name') + ' could not be listed.')

      finally:
          db.session.close()

      return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id): #DONE, CONSIDER BONUS CHALLENGE!
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
      Venue.query.filter_by(id=venue_id).delete()
      db.session.commit()
      flash(' Venue ' + venue_id + 'was successfully de-listed.')
  except:
      db.session.rollback()
      flash('An error occurred. Venue ' + venue_id + 'could not be de-listed.')

  finally:
      db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():  #DONE!!!
  # TODO: replace with real data returned from querying the database
  data = db.session.query(Artist.name, Artist.id).order_by('name').all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists(): #DONE
  # Implements search on artists with partial string search. Ensures it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term')
  artist_match = db.session.query(Artist.id, Artist.name).filter(Artist.name.ilike(f'%{search_term}%')).all()
  response = {
    "count": len(artist_match),
    "data": [{'id':a.id, 'name': a.name} for a in artist_match]
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id): #DONE
  # shows the artist page with the given artist_id

  now = datetime.utcnow()
  an_artist = db.session.query(Artist).filter_by(id=artist_id).first()
  upcoming_shows = db.session.query(Show).join(Artist, Show.artist_id==artist_id).filter(Show.start_time>now).all()
  past_shows = db.session.query(Show).join(Artist, Show.artist_id==artist_id).filter(Show.start_time<now).all()

  data = {
    'id': an_artist.id,
    "name": an_artist.name,
    "genres": an_artist.genres,
    "city": an_artist.city,
    "state": an_artist.state,
    "phone": an_artist.phone,
    "website": an_artist.website,
    "facebook_link": an_artist.facebook_link,
    "seeking_venue": an_artist.seeking_venue,
    "seeking_description": an_artist.seeking_description,
    "image_link": an_artist.image_link,
    "past_shows": [{
        "venue_id": a_show.venue_id,
        "venue_name": a_show.venue.name,
        "venue_image_link": a_show.venue.image_link,
        "start_time": (a_show.start_time).strftime("%y-%m-%d %H:%M:%S")
        } for a_show in past_shows],
    "upcoming_shows":  [{
        "venue_id": a_show.venue_id,
        "venue_name": a_show.venue.name,
        "venue_image_link": a_show.venue.image_link,
        "start_time": (a_show.start_time).strftime("%y-%m-%d %H:%M:%S")
        } for a_show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)}

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id): #DONE
    #autopopulates form with artist data
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):  #DONE

  form = ArtistForm(meta={'csrf': False})
  # 'if' prints errors if invalid data is submitted and redirects to edit endpoint
  if not(form.validate_on_submit()):
      for error in form.errors.values():
          flash(error[0])

      return redirect(url_for('edit_artist', artist_id=artist_id))

  else:
      try:
          artist = Artist.query.get(artist_id)
          artist.name =  request.form.get('name')
          artist.genres = request.form.getlist('genres')
          artist.city = request.form.get('city')
          artist.state = request.form.get('state')
          artist.phone = request.form.get('phone')
          artist.website = request.form.get('website')
          artist.facebook_link = request.form.get('facebook_link')
          artist.seeking_venue = True if request.form.get('seeking_venue')== 'y' else False
          artist.seeking_description = request.form.get('seeking_description')
          artist.image_link = request.form.get('image_link')
          db.session.commit()
          flash('Artist ' + artist.name + ' was successfully updated!')

      except Exception as e:
          db.session.rollback()
          print(e)
          flash('An error occured. Artist ' + request.form.get('name' )+ ' could not be updated!')
      finally:
          db.session.close()

      return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id): #DONE
  #autopopulates form with venue data
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):  #DONE
  # takes values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  form = VenueForm(meta={'csrf': False})
  # 'if' prints errors if invalid data is submitted and redirects to edit_venue endpoint
  if not(form.validate_on_submit()):
      for error in form.errors.values():
          flash(error[0])

      return redirect(url_for('edit_venue', venue_id=venue_id))

  else:
      try:
          venue = Venue.query.get(venue_id)
          venue.name =  request.form.get('name')
          venue.genres = request.form.getlist('genres')
          venue.city = request.form.get('city')
          venue.state = request.form.get('state')
          venue.address = request.form.get('address')
          venue.phone = request.form.get('phone')
          venue.website = request.form.get('website')
          venue.facebook_link = request.form.get('facebook_link')
          venue.seeking_talent = True if request.form.get('seeking_talent')=='y' else False
          venue.seeking_description = request.form.get('seeking_description')
          venue.image_link = request.form.get('image_link')
          db.session.commit()
          flash('Venue ' + venue.name + ' was successfully updated!')
      except:
          db.session.rollback()
          flash('An error occured! Venue ' + request.form.get('name') + ' could not be updated!')
      finally:
          db.session.close()

      return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():  #DONE
 # called upon submitting the new artist listing form

 form = ArtistForm(meta={'csrf': False})
 #prints errors if invalid data is submitted and rerenders html template
 if not(form.validate_on_submit()):
     for error in form.errors.values():
         flash(error[0])

     return render_template('forms/new_artist.html', form=form)

 else:
      try:
          new_artist = Artist(
            name = request.form.get('name'),
            city = request.form.get('city'),
            state = request.form.get('state'),
            phone = request.form.get('phone'),
            genres = request.form.getlist('genres'),
            image_link = request.form.get('image_link'),
            website = request.form.get('website'),
            facebook_link = request.form.get('facebook_link'),
            seeking_venue = True if request.form.get('seeking_venue')=='y' else False,
            seeking_description = request.form.get('seeking_description'))

          db.session.add(new_artist)
          db.session.commit()
          flash('Artist ' + request.form.get('name') + ' was successfully listed!')

      except:
          # on unsuccessful db insert, flash an error instead.
          db.session.rollback()
          flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')

      finally:
         db.session.close()

      return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():    #DONE
  # displays list of shows at /shows
  list_shows = db.session.query(Show).order_by('start_time').all()
  data = [{
    "venue_id" : a_show.venue_id,
    "venue_name": a_show.venue.name,
    "artist_id": a_show.artist_id,
    "artist_name": a_show.artist.name,
    "artist_image_link": a_show.artist.image_link,
    "start_time" : (a_show.start_time).strftime("%y-%m-%d %H:%M:%S")
  } for a_show in list_shows]

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission(): #DONE
  # called to create new shows in the db, upon submitting new show listing form

  form = ShowForm(meta={'csrf': False})
  #prints errors if invalid data is submitted and re-renders html template
  if not(form.validate_on_submit()):
      for error in form.errors.values():
          flash(error[0])

      return render_template('forms/new_show.html', form=form)

  else:
      try:
          new_show = Show(
            venue_id = request.form.get('venue_id'),
            artist_id = request.form.get('artist_id'),
            start_time = request.form.get('start_time'))

          db.session.add(new_show)
          db.session.commit()
          flash('Show was successfully listed!')

      except Exception as e:
          db.session.rollback()
          print(e)
          flash('An error occurred. Show could not be listed.')
      finally:
         db.session.close()

      return render_template('pages/home.html')

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

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
