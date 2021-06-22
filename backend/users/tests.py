import os

from django.core.files import File
from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User 

from modules.utils import get_file_by_url

class UserModelUnitTest(TestCase):

    def __init__(self, *args, **kwargs):
        """
            [HELP DOCS]
                This TestCase checks user model on creating.
                It creates user instance and then check all fields, catching 
                strange behavior of user model creating.

        """
        super(UserModelUnitTest, self).__init__(*args, **kwargs)
    def setUp(self) -> None:
        # create user instance
        self.instance = User.objects.create_user(
            email = "test@email.com",
            first_name = "Unit",
            last_name = "Test",
            birth_date = "2000-01-01",
            about_me = "I`m the most usefull user for project!",
            password = "testpassword123",
        )

        # define avatar image url
        self.instance_avatar_url = "https://images.unsplash.com/photo-1541963463532-d68292c34b19?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8Mnx8fGVufDB8fHx8&w=1000&q=80"
        
        # open image file
        with open(  get_file_by_url(self.instance_avatar_url)[0], 'rb'   ) as file:

            # save file data to check it after saving in database
            self.instance_avatar_image_data = file.read()

            # add avatar image to instance
            self.instance.avatar.save(
                os.path.basename(self.instance_avatar_url),
                File(file)
            )

            # save instance changes
            self.instance.save()

        return None

    def test_email(self) -> None:
        self.assertEqual(
            self.instance.email,
            "test@email.com",
            "Wrong email address!"
        )

        return None

    def test_first_name(self) -> None:
        self.assertEqual(
            self.instance.first_name,
            "Unit",
            "Wrong first name!"
        )

        return None

    def test_last_name(self) -> None:
        self.assertEqual(
            self.instance.last_name,
            "Test",
            "Wrong last name!"
        )

        return None

    def test_about_me(self) -> None:
        self.assertEqual(
            self.instance.about_me,
            "I`m the most usefull user for project!",
            "Wrong about_me text!"
        )

        return None


    def test_birth_date(self) -> None:
        self.assertEqual(
            self.instance.birth_date,
            "2000-01-01",
            "Wrong birth_date!"
        )

        return None

    def test_password(self) -> None:
        self.assertTrue(
            self.instance.check_password("testpassword123"),
            "Wrong password!"
        )

        return None


    def test_avatar_image(self) -> None:
        self.assertEqual(
            self.instance.avatar.file.read(),
            self.instance_avatar_image_data
        )

        return None