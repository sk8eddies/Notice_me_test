from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3
from Classes import *
from pony.orm import *
import bcrypt


# create the application object
app = Flask(__name__)

app.secret_key = "tomato"
app.database = "notice_db.db"


# ------------------------------------ LOGIN ------------------------------------
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Access denied: You must login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
@db_session
def login():
    error = None
    if request.method == 'POST':
        if User.is_user_data_valid(sent_username=request.form['username'], sent_password=request.form['password']):
            session['logged_in'] = True
            session["current_username"] = request.form['username']
            flash(request.form['username']+' logged in')
            return redirect(url_for('home'))
        else:
            error = "invalid username or password, please try again"
            flash("invalid username or password, please try again")
            return redirect(url_for('login'))
    return render_template('index.html', error=error)


# ------------------------------------------ EDITING NOTES ----------------------------------------
@app.route('/note/<note_id>/edit', methods=['POST'])
@app.route('/filtered_home/note/<note_id>/edit', methods=['POST'])
@login_required
@db_session
def redirect_edit_note(note_id):
    session['note_id'] = note_id
    return redirect(url_for('edit_note'))


@app.route('/note/<note_id>/delete', methods=['POST'])
@app.route('/filtered_home/note/<note_id>/delete', methods=['POST'])
@login_required
@db_session
def delete_note(note_id):
    Note.delete_note(note_id=note_id)
    return redirect(url_for('home'))


@app.route('/edit_note', methods=['GET', 'POST'])
@login_required
@db_session
def edit_note():
    note_id = session['note_id']
    current_note = Note[note_id]
    if request.method == 'POST':
        Note.save_note(note_id=note_id, sent_title=request.form['title'], sent_content=request.form['content'])
        return redirect(url_for('home'))
    return render_template('edit_note.html', note=current_note, note_id=note_id)


# ----------------------------------------TAG NOTE -------------------------------------------------------
@app.route('/note/<note_id>/tag', methods=['POST'])
@app.route('/filtered_home/note/<note_id>/tag', methods=['POST'])
@login_required
@db_session
def redirect_tag_note(note_id):
    session['note_id'] = note_id
    return redirect(url_for('new_tag'))


@app.route('/new_tag', methods=['GET', 'POST'])
@login_required
@db_session
def new_tag():
    note_id = session['note_id']
    current_note = Note[note_id]
    current_user = User[User.get_user_id(session['current_username'])]
    if request.method == 'POST':
        tag_name = request.form['create_tag']
        if Tag.is_tag_in_db(sent_tag_name=tag_name) and Tag.is_tag_in_db_for_user(sent_tag_name=tag_name, sent_current_user_id=User.get_user_id(session['current_username'])):
            tag = Tag[Tag.get_tag_id(sent_tag_name=tag_name)]
            tagging = NoteTagging(tag=tag, note=current_note)
        elif Tag.is_tag_in_db(sent_tag_name=tag_name) and not Tag.is_tag_in_db_for_user(sent_tag_name=tag_name, sent_current_user_id=User.get_user_id(session['current_username'])):
            new_tag = Tag(name=tag_name, user=current_user, user_id=User.get_user_id(session['current_username']))
            tagging = NoteTagging(tag=new_tag, note=current_note)
        else:
            new_tag = Tag(name=tag_name, user=current_user, user_id=User.get_user_id(session['current_username']))
            tagging = NoteTagging(tag=new_tag, note=current_note)
        return redirect(url_for('home'))
    return render_template('new_tag.html')


@app.route('/tag/<tag_id>/filter', methods=['POST'])
@app.route('/filtered_home/tag/<tag_id>/filter', methods=['POST'])
@login_required
@db_session
def filter_notes_by_tag(tag_id):
    return redirect(url_for('filtered_home', tag_id=tag_id))


@app.route('/tag/<tag_id>/delete', methods=['POST'])
@app.route('/filtered_home/tag/<tag_id>/delete', methods=['POST'])
@login_required
@db_session
def delete_tag(tag_id):
    Tag.delete_tag(current_tag_id=tag_id)
    return redirect(url_for('home'))


# --------------------------------------------- HOME ----------------------------------------------------
@app.route('/home', methods=['GET', 'POST'])
@login_required
@db_session
def home():
    current_user_id = User.get_user_id(session['current_username'])
    session['theme'] = User.get_user_theme(current_user_id)

    sorted_notes = User.get_user_notes(sent_current_user_id=current_user_id)
    tags = User.get_user_tags(sent_current_user_id=current_user_id)

    if request.method == 'POST' and request.form['identifier'] == "theme":
        User.increase_user_theme(current_user_id)
        return redirect(url_for('home'))
    return render_template('home.html', notes=sorted_notes, tags=tags)


@app.route('/filtered_home/<tag_id>', methods=['GET', 'POST'])
@login_required
@db_session
def filtered_home(tag_id):
    current_user_id = User.get_user_id(session['current_username'])
    filtered_notes = User.filter_notes_by_tag(current_tag_id=tag_id, current_user_id=current_user_id)
    tags = User.get_user_tags(sent_current_user_id=current_user_id)
    return render_template('home.html', tags=tags, notes=filtered_notes)


# ----------------------------------------------- NEW NOTE -------------------------------------------------
@app.route('/new_note', methods=['GET', 'POST'])
@app.route('/filtered_home/new_note', methods=['GET', 'POST'])
@login_required
@db_session
def new_note():
    if request.method == 'POST':
        current_user_id = User.get_user_id(session['current_username'])
        note = Note(user=current_user_id, user_id=current_user_id, title=request.form['title'], content=request.form['content'])
        return redirect(url_for('home'))
    return render_template('new_note.html')


# ----------------------------------------------- LOGOUT ---------------------------------------------------
# There is no need to POST to this method. !Potato!
# If someone gets to /logout they are automatically logged out !Potato!
@app.route('/logout')
@login_required
def logout():
    flash(session['current_username']+' logged out')
    session.pop('logged_in', None)
    session.pop('current_username', None)
    return redirect(url_for('login'))


# -------------------------------------------------- NEW ACCOUNT -------------------------------------------
@app.route('/new_account', methods=['GET', 'POST'])
@db_session
def new_account():
    error = None
    if request.method == 'POST':

        password = b"{0}".format(request.form['password'])
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        confirm_password = b"{0}".format(request.form['confirm_password'])
        hash_confirm_password = bcrypt.hashpw(confirm_password, hash_password)

        if User.is_user_valid(sent_username=request.form['username'],
                              sent_password=hash_password,
                              sent_confirm_password=hash_confirm_password):
            user = User(username=request.form['username'], password=hash_password, theme=0)
            commit()
            return redirect(url_for("login"))
        else:
            flash("Username taken or password mismatch. Please try again.")
    return render_template('new_account.html', error=error)


# ----------------------------------------- CHANGE PASSWORD -------------------------------------------
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
@db_session
def change_password():
    error = None
    current_user_id = User.get_user_id(session['current_username'])
    if request.method == 'POST':
        if User.change_password(sent_current_user_id=current_user_id,
                                sent_password=request.form['password'],
                                sent_confirm_password=request.form['confirm_password']):
            return redirect(url_for('logout'))
        else:
            flash('password mismatch')
    return render_template('change_password.html', error=error)


# ---------------------------------- FLASK STUFF ---------------------------------------------
def connect_db():
    return sqlite3.connect(app.database) #!TOMATO!

if __name__ == '__main__':
    app.run(debug=True)

# Do not put anything here!
