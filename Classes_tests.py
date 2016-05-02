import unittest
from pony import *
import sqlite3
from Classes import *


class UserTest(unittest.TestCase):

    @db_session
    def test_CRUD(self):
        # Initializing variables that are used for the test
        username = "test_username"
        password = "test_password"
        user_theme = 1
        password2 = "test_password2"
        number_of_themes = 3

        # This method has to be tested before the User is created since it will search for
        # a user with the same username as the one we pass as an argument.
        # Verify that is_user_valid() method is working as intended and doesn't return None
        self.assertTrue(User.is_user_valid(sent_username=username, sent_password=password, sent_confirm_password=password) is not None)
        self.assertTrue(User.is_user_valid(sent_username=username, sent_password=password, sent_confirm_password=password))

        # Verify that a User can be created and that it exists in the database
        test_user = User(username=username, password=password, theme=user_theme)
        commit()
        self.assertTrue(test_user is not None)
        self.assertTrue(db.exists('* from User where username = $username'))

        # Verify that if the the user already exists in the database is_user_valid will return False.
        self.assertFalse(User.is_user_valid(sent_username=username, sent_password=password, sent_confirm_password=password))

        # Verify that the password and username are the same as the ones that we created the User with
        self.assertTrue(test_user.username is not None)
        self.assertEquals(test_user.username, username)
        self.assertTrue(test_user.password is not None)
        self.assertEquals(test_user.password, password)

        # Verify that is_user_in_db() method is working as intended and doesn't return None
        self.assertTrue(User.is_user_in_db(sent_username=username) is not None)
        self.assertTrue(User.is_user_in_db(sent_username=username))

        # Verify that is_user_data_valid() method is working as intended and doesn't return None
        self.assertTrue(User.is_user_data_valid(sent_username=username, sent_password=password) is not None)
        self.assertTrue(User.is_user_data_valid(sent_username=username, sent_password=password))

        # Verify that I can get the Users row id from the database and that it is an int
        # Verify that the get_user_id() method returns the right row id from the database and that it isn't None
        user_id = test_user.id
        self.assertTrue(user_id is not None)
        self.assertEqual(type(user_id), int)
        self.assertTrue(User.get_user_id(current_username=username) is not None)
        self.assertEqual(User.get_user_id(current_username=username), user_id)

        # Verify that the get_user_theme method works as intended and that it returns an int.
        self.assertTrue(test_user.get_user_theme(current_user_id=user_id) is not None)
        self.assertEqual(test_user.get_user_theme(current_user_id=user_id), user_theme)
        self.assertEqual(type(test_user.get_user_theme(current_user_id=user_id)), int)

        # Verify that the increase_user_theme() method works as intended.
        self.assertTrue(test_user.theme is not None)
        self.assertEqual(test_user.theme, user_theme)
        test_user.increase_user_theme(current_user_id=user_id)
        self.assertTrue(test_user.get_user_theme(current_user_id=user_id) is not None)
        self.assertEqual(test_user.get_user_theme(current_user_id=user_id), (user_theme+1))
        test_user.increase_user_theme(current_user_id=user_id)
        test_user.increase_user_theme(current_user_id=user_id)
        self.assertEqual(test_user.get_user_theme(current_user_id=user_id), user_theme)

        # Verify that the change_password() method works as intended.
        self.assertTrue(test_user.change_password(current_user_id=user_id, sent_password=password2, sent_confirm_password=password2) is not None)
        self.assertTrue(test_user.change_password(current_user_id=user_id, sent_password=password2, sent_confirm_password=password2))
        self.assertTrue(test_user.password is not None)
        self.assertEqual(test_user.password, password2)

        # get_user_notes test TODO

        # Verify that a User can be deleted from the database.
        test_user.delete()
        commit()
        self.assertFalse(db.exists('* from User where username = $username'))

    @db_session
    def test_invalid_arguments(self):
        # Initializing variables that are used for the test
        username = "test_username"
        none_username = None
        password = "test_password"
        none_password = None
        user_theme = 1
        none_theme = None

        # Test creating a User when passing false arguments to the constructor
        try:
            test_user = User(username=none_username, password=password, theme=user_theme)
        except Exception, x:
            # print(str(x)+" x")
            self.assertTrue("is required" in str(x))

        try:
            test_user = User(username=username, password=none_password, theme=user_theme)
        except Exception, x2:
            # print(str(x2)+" x2")
            self.assertTrue("is required" in str(x2))

        try:
            test_user = User(username=username, password=password, theme=none_theme)
        except Exception, y:
            # print(str(y)+y)
            self.assertTrue("is required" in str(y))

        # Test is_user_in_db() with None as an argument
        try:
            User.is_user_in_db(sent_username=none_username)
        except Exception, x3:
            # print(str(x3)+" x3")
            self.assertTrue("None is not accepted" in str(x3))

        # Test is_user_valid() with None as arguments
        try:
            User.is_user_valid(sent_username=none_username, sent_password=password, sent_confirm_password=password)
        except Exception, x4:
            # print(str(x4)+" x4")
            self.assertTrue("None is not accepted" in str(x4))

        try:
            User.is_user_valid(sent_username=username, sent_password=none_password, sent_confirm_password=password)
        except Exception, x5:
            # print(str(x5)+" x5")
            self.assertTrue("None is not accepted" in str(x5))

        try:
            User.is_user_valid(sent_username=username, sent_password=password, sent_confirm_password=none_password)
        except Exception, x6:
            # print(str(x6)+" x6")
            self.assertTrue("None is not accepted" in str(x6))

        # Test is_user_data_valid() with None as arguments
        try:
            User.is_user_data_valid(sent_username=none_username, sent_password=password)
        except Exception, x7:
            # print(str(x7)+" x7")
            self.assertTrue("None is not accepted" in str(x7))

        try:
            User.is_user_data_valid(sent_username=username, sent_password=none_password)
        except Exception, x8:
            # print(str(x8)+" x8")
            self.assertTrue("None is not accepted" in str(x8))

        # Test get_user_id() with None as an argument
        try:
            User.get_user_id(current_username=none_username)
        except Exception, x9:
            # print(str(x9)+" x9")
            self.assertTrue("None is not accepted" in str(x9))


class NoteTest(unittest.TestCase):

    @db_session
    def test_CRUD(self):
        # Initializing variables and objects that are needed
        title = "test_note"
        title2= "test_note2"
        content = "test_content"
        content2 = "test_content2"
        user_id = 1

        test_user = User(username="test_username", password="test_password", theme=1)
        commit()
        self.assertTrue(test_user is not None)

        # Verify that Note can be created and that it exists in the database
        test_note = Note(user=test_user, user_id=user_id, title=title, content=content)
        self.assertTrue(test_note is not None)
        self.assertTrue(db.exists('* from Note where title = $title'))

        # Verify that the Note data in the database is matching with the note that we created
        # Get the Notes row id and verify that it is exists and that it is an int
        self.assertTrue(test_note.user is not None)
        self.assertTrue(test_note.user == test_user)
        self.assertTrue(test_note.user_id is not None)
        self.assertEqual(test_note.user_id, user_id)
        self.assertTrue(test_note.title is not None)
        self.assertEqual(test_note.title, title)
        self.assertTrue(test_note.content is not None)
        self.assertEqual(test_note.content, content)
        note_id = test_note.id
        self.assertTrue(note_id is not None)
        self.assertEqual(type(note_id), int)

        # Verify that the save_note() method works as intended and that it can update the title and the content
        test_note.save_note(note_id=note_id, sent_title=title2, sent_content=content2)
        self.assertTrue(test_note.title is not None)
        self.assertEqual(test_note.title, title2)
        self.assertTrue(test_note.content is not None)
        self.assertEqual(test_note.content, content2)

        # Verify that a note can be deleted with the delete_note() method
        Note.delete_note(note_id=test_note.id)
        self.assertFalse(db.exists('* from Note where title = $title'))
        test_user.delete()

    @db_session
    def test_invalid_arguments(self):
        # Initializing variables and objects that are needed
        title = "test_note"
        none_title = None
        content = "test_content"
        none_content = None
        user_id = 1
        none_user_id = None
        test_user = User(username="test_username", password="test_password", theme=1)
        commit()
        none_user = None
        none_note_id = None

        # Test creating a Note when passing false arguments to the constructor
        try:
            test_note = Note(user=none_user, user_id=user_id, title=title, content=content)
        except Exception, x:
            # print(str(x)+" x")
            self.assertTrue("is required" in str(x))

        try:
            test_note = Note(user=test_user, user_id=none_user_id, title=title, content=content)
        except Exception, x2:
            # print(str(x2)+" x2")
            self.assertTrue("is required" in str(x2))

        try:
            test_note = Note(user=test_user, user_id=user_id, title=none_title, content=content)
        except Exception, x3:
            # print(str(x3)+" x3")
            self.assertTrue("is required" in str(x3))

        try:
            test_note = Note(user=test_user, user_id=user_id, title=title, content=none_content)
        except Exception, x4:
            # print(str(x4)+" x4")
            self.assertTrue("is required" in str(x4))

        # Test save_note() method to see that the arguments are required and cannot be None
        try:
            test_note = Note(user=test_user, user_id=user_id, title=title, content=content)
            note_id = test_note.id
            Note.save_note(note_id=none_note_id, sent_title=title, sent_content=content)
        except Exception, x5:
            # print(str(x5)+" x5")
            self.assertTrue("cannot be set to None" in str(x5))

        try:
            test_note = Note(user=test_user, user_id=user_id, title=title, content=content)
            note_id = test_note.id
            Note.save_note(note_id=note_id, sent_title=none_title, sent_content=content)
        except Exception, x6:
            # print(str(x6)+" x6")
            self.assertTrue("cannot be set to None" in str(x6))

        try:
            test_note = Note(user=test_user, user_id=user_id, title=title, content=content)
            note_id = test_note.id
            Note.save_note(note_id=note_id, sent_title=title, sent_content=none_content)
        except Exception, x7:
            # print(str(x7)+" x7")
            self.assertTrue("cannot be set to None" in str(x7))

        test_user.delete()
