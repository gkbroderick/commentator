import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError

from playlist.models import PlayInstance, Comment

class PlayInstanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.play_instance = PlayInstance.objects.create(name='Dance Yrself Clean', kexp_play_id='2632178')

    def test_name_max_length(self):
        play_instance = self.play_instance
        max_length = play_instance._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)

    def test_kexp_play_id_label(self):
        play_instance = self.play_instance
        field_label = play_instance._meta.get_field('kexp_play_id').verbose_name
        self.assertEquals(field_label, "kexp play id")

    def test_airdate_label(self):
        play_instance = self.play_instance
        field_label = play_instance._meta.get_field('airdate').verbose_name
        self.assertEquals(field_label, "airdate")

    def test_airdate_default_creation_is_datetime_object(self):
        play_instance = self.play_instance
        airdate = play_instance.airdate
        self.assertTrue(type(airdate) is datetime.datetime)

    def test_object_name_is_name_colon_airdate_as_string(self):
        play_instance = self.play_instance
        time_format_string = '%Y-%m-%d %H:%M:%S'
        expected_object_name = f'{play_instance.name}: {play_instance.airdate.strftime(time_format_string)}'
        self.assertEquals(expected_object_name, str(play_instance))

class CommentInstanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.play_instance = PlayInstance.objects.create(name='Dance Yrself Clean', kexp_play_id='2632178')
        cls.comment = Comment.objects.create(play_instance=cls.play_instance, comment_text='I\'m in love')

    def test_play_instance_foreign_key_name_check(self):
        comment = self.comment
        play_instance_name = comment.play_instance.name
        self.assertEquals(play_instance_name, 'Dance Yrself Clean')

    def test_comment_text_cannot_be_blank(self):
        newComment = Comment.objects.create(play_instance=self.play_instance, comment_text='')
        with self.assertRaises(ValidationError):
            newComment.clean_fields()

    def test_date_created_label(self):
        comment = self.comment
        field_label = comment._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, "date created")

    def test_date_created_default_creation_is_datetime_object(self):
        comment = self.comment
        date_created = comment.date_created
        self.assertTrue(type(date_created) is datetime.datetime)

    def test_date_last_edited_label(self):
        comment = self.comment
        field_label = comment._meta.get_field('date_last_edited').verbose_name
        self.assertEquals(field_label, "last edited")

    def test_date_last_edited_default_creation_is_datetime_object(self):
        comment = self.comment
        date_last_edited = comment.date_last_edited
        self.assertTrue(type(date_last_edited) is datetime.datetime)

    def test_object_name_is_play_instance_name_comma_comment_on_date_created_as_string(self):
        comment = self.comment
        play_instance_string = str(comment.play_instance)
        time_format_string = '%Y-%m-%d %H:%M:%S'
        expected_object_name = f'{play_instance_string}, comment on {comment.date_created.strftime(time_format_string)}'
        self.assertEquals(expected_object_name, str(comment))
