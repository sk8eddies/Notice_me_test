from pony.orm import *
import bcrypt
import pydoc

db = Database('sqlite', 'notice_db.sqlite', create_db=True)
# db = Database()                                                                                                                   # THIS CODE SHALL NOT BE DELETED
# db.bind('postgres', user='notice', password='Notice', host='localhost', database='notice_db', dbname='notice_db', port='5432')    # THIS CODE SHALL NOT BE DELETED
none_error_message = 'None is not accepted as an argument for this method.'
number_of_themes = 2    # Used in arrays so the actual number of themes is "number_of_themes + 1".


class User(db.Entity):

    """
    Construct a new User as an database entity

    :param username: The name of the User. String.
    :param password: The password of the User. String.
    :param: theme: The theme-index of the user. int.
    :param note: All Users can have notes and it is a one-to-many relationship between them.
    :return: Returns noting.
    """
    username = Required(str)
    password = Required(str)
    theme = Required(int)
    notes = Set("Note")
    tags = Set('Tag')

    @classmethod
    def is_user_in_db(cls, sent_username):

        """
        :argument sent_username: The currents Users username. String.

        This method checks if the User with the specified username already is in the database.
        None is not an accepted argument and if any of the arguments is None it
        will throw the "none_error_message".
        :return: True or False
        """

        if sent_username is not None:
            return db.exists("* from User where username = $sent_username")
        else:
            raise TypeError(none_error_message)

    @classmethod
    def is_user_valid(cls, sent_username, sent_password, sent_confirm_password):

        """
        :argument sent_username: The currents Users username. String.
        :argument sent_password: The Users password. String.
        :argument sent_confirm_password: Another password to compare the first one to. String.

        This method compares the passwords to see that they're the same and then check the database to
        verify that the User isn't in the database. None is not an accepted argument
        and if any of the arguments is None it will throw the "none_error_message".
        :return: True or False
        """

        if sent_username and sent_password and sent_confirm_password is not None:
            return sent_password == sent_confirm_password and not User.is_user_in_db(sent_username)
        else:
            raise TypeError(none_error_message)

    @classmethod
    @db_session
    def is_user_data_valid(cls, sent_username, sent_password):

        """
        :argument sent_username: The currents Users username. String.
        :argument sent_password: The Users password. String.

        This method authenticates the information that is sent in by the user of Notice(me senpai!).
        None is not an accepted argument and if any of the arguments is None it will throw
        the "none_error_message".
        :return: True or False
        """

        if sent_username and sent_password is not None:
            if User.is_user_in_db(sent_username=sent_username):
                password = b"{0}".format(sent_password)
                user = db.get("* from User where username = $sent_username")
                user_password = b"{0}".format(user.password)

                return sent_username == user.username and bcrypt.hashpw(password, user_password) == user_password
        else:
            raise TypeError(none_error_message)

    @classmethod
    @db_session
    def get_user_id(cls, current_username):

        """
        :argument current_username: The currents Users username. String.

        None is not an accepted argument and if any of the arguments is None it will throw
        the "none_error_message".
        :return: The row id for the User with the specified username.
        """

        if current_username is not None:
            current_user_id = db.get('id from User where username = $current_username')
            return current_user_id
        else:
            raise TypeError(none_error_message)

    @classmethod
    @db_session
    def get_user_theme(cls, current_user_id):

        """
        :argument: current_user_id: The row id of the current User. int.

        None is not an accepted argument and if any of the arguments is None it will throw
        the "none_error_message".
        :return: An int that represents the User theme.
        """
        if current_user_id is not None:
            current_user_theme = db.get('theme from User where id = $current_user_id')
            return current_user_theme
        else:
            raise TypeError(none_error_message)

    @classmethod
    @db_session
    def increase_user_theme(cls, current_user_id):

        """
        :argument: current_user_id: The row id of the current User. int.

        This method will increase the theme variable for the current User with 1 every time
        that the method is called.
        None is not an accepted argument and if any of the arguments is None it will throw
        the "none_error_message".
        """

        if current_user_id is not None:
            user = User[current_user_id]
            if user.theme < number_of_themes:
                user.theme += 1
            elif user.theme == number_of_themes:
                user.theme = 0
        else:
            raise TypeError(none_error_message)

    @classmethod
    @db_session
    def change_password(cls, sent_current_user_id, sent_password, sent_confirm_password):

        """
        :argument: current_user_id: The row id of the current User. int.
        :argument sent_password: The Users password. String.
        :argument sent_confirm_password: Another password to compare the first one to. String.

        This method is used for changing the current Users password.
        :return: True or False that is used for a pop-up to tell if the passwords didn't match.
        """

        if sent_password == sent_confirm_password:
            user = User[sent_current_user_id]
            password = b"{0}".format(sent_password)
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            user.password = hashed_password
            commit()
            return True
        else:
            return False

    @classmethod
    @db_session
    def get_user_notes(cls, sent_current_user_id):

        """
        :argument: sent_current_user_id: The row id of the current User. int.
        This method will get all of the Notes that the User with the corresponding User_id has.
        :return: A list of Notes. Note
        """

        sorted_notes = []

        notes_id = db.select('id from Note order by id desc')

        for note_id in notes_id:
            note = Note[note_id]
            if note.user_id == sent_current_user_id:
                sorted_notes.append(note)

        return sorted_notes

    @classmethod
    @db_session
    def get_user_tags(cls, sent_current_user_id):
        user = User[sent_current_user_id]
        return user.tags

    @classmethod
    @db_session
    def filter_notes_by_tag(cls, current_tag_id, current_user_id):
        notes = User.get_user_notes(sent_current_user_id=current_user_id)
        filtered_notes = []

        print("sent tag id: {0}".format(current_tag_id))        # TODO filter lambda
        for note in notes:
            print(note.id)
            print(note.tags.tag)
            for tag in note.tags.tag:
                print(tag.name)
            if note.tags.tag.id == current_tag_id:
                filtered_notes.append(note)
        return filtered_notes


class Note(db.Entity):

    """
    Construct a new Note as an database entity

    :param user: The User that the Note belongs to. A Note can only have one user.
    :param user_id: The id of the User that owns the Note. int. A quick fix used when we template the note.
    :param title: The title of the Note. String.
    :param content: The content of the Note. String.
    :return: Returns noting.
    """

    user = Required(User)
    user_id = Required(int)
    title = Required(str)
    content = Required(str)
    tags = Set('NoteTagging')

    @classmethod
    @db_session
    def save_note(cls, note_id, sent_title, sent_content):

        """
        :argument note_id: The row id of the Note that we edit. int.
        :argument sent_title: The title of the Note. String.
        :argument sent_content: The content of the Note. String.

        Saves the Note with the specified id to the database. Used for updating the title
        and content of the note after it has been created. None is not an accepted argument
        and if any argument for the method is None it will throw an exception.
        """

        note = Note[note_id]
        note.title = sent_title
        note.content = sent_content
        commit()

    @classmethod
    @db_session
    def delete_note(cls, note_id):

        """
        :argument note_id: The row id of the Note that we delete. int.

        Deletes the Note with specified id. Everything on the specified row is deleted.
        None is not an accepted argument and if any argument for the method is None
        it will throw an exception.
        """

        note = Note[note_id]
        note.delete()
        commit()
    #
    # @db_session
    # def get_note_taggings(self):
    #     sorted_taggins = []
    #     taggings = db.select('')
    #
    #     for

class Tag(db.Entity):
    name = Required(str)
    tagging = Set('NoteTagging')
    user = Required(User)

    @classmethod
    @db_session
    def is_tag_in_db(cls, sent_tag_name):
        return db.exists('* from Tag where name = $sent_tag_name')

    @classmethod
    @db_session
    def get_tag_id(cls, sent_tag_name):
        return db.get('id from Tag where name = $sent_tag_name')


class NoteTagging(db.Entity):
    note = Required(Note)
    tag = Required(Tag)


db.generate_mapping(create_tables=True)

# help('Classes')
