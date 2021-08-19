from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from stringWagon.db import get_db

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    db = get_db()
    instruments = db.execute(
        'SELECT * '
        ' FROM instrument '
    ).fetchall()
    return render_template('instrument.html', instruments=instruments)
    
@bp.route('/add', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        typeOfInstrument = request.form['typeOfInstrument']
        comments = request.form['comments']
        error = None

        if not typeOfInstrument:
            error = 'Type of Instrument is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO instrument (brand, model, typeOfInstrument, comments)'
                ' VALUES (?, ?, ?, ?)',
                (brand, model, typeOfInstrument, comments)
            )
            db.commit()
            return redirect('/')
            
    return render_template('add.html')     
            
def get_instrument(id):
    instrument = get_db().execute(
        'SELECT i.id, typeOfInstrument, brand, model, comments'
        ' FROM instrument '
        ' WHERE i.id = ?',
        (id,)
    ).fetchone()

    if instrument is None:
        abort(404, f"Instrument id {id} doesn't exist.")

    return instrument            

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    instrument = get_instrument(id)

    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        typeOfInstrument = request.form['typeOfInstrument']
        comments = request.form['comments']
        error = None

        if not typeOfInstrument:
            error = 'Type of Instrument is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE instrument SET typeOfInstrument = ?, brand = ?, model = ?, comments = ? '
                ' WHERE id = ?',
                (typeOfInstrument, brand, model, comments, id)
            )
            db.commit()
            return redirect('/')
            
@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_instrument(id)
    db = get_db()
    db.execute('DELETE FROM instrument WHERE id = ?', (id,))
    db.commit()
    return redirect('/')           

    return render_template('index/update.html', instrument=instrument)   