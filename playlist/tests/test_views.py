import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from playlist.models import PlayInstance, Comment

class CommentAjaxCreationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        c = Client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        data = {
            'play_instance_kexp_id': 277951,
            'play_instance_name': 'Teen Age Riot',
            'play_instance_airdate': 'June 2, 2019, 3:15 p.m.',
            'comment_id' : 0,
            'comment_text' : 'The Perfect Summer Song',
        }
        response = c.post(reverse('comment'), data, **kwargs)
        json_string = response.content
        cls.response_data = json.loads(json_string)

    def test_comment_created_response_id_matches_latest_created_id(self):
        response_comment_id = self.response_data['comment_id']
        latest_comment_id = Comment.objects.latest('date_created').id
        self.assertEquals(response_comment_id, latest_comment_id)

    def test_comment_created_request_text_matches_latest_created_text(self):
        request_comment_text = "The Perfect Summer Song"
        latest_comment_text = Comment.objects.latest('date_created').comment_text
        self.assertEquals(request_comment_text, latest_comment_text)

    def test_comment_created_response_text_matches_latest_created_text(self):
        response_comment_text = self.response_data['comment_text']
        latest_comment_text = Comment.objects.latest('date_created').comment_text
        self.assertEquals(response_comment_text, latest_comment_text)

    def test_comment_created_request_kexp_play_id_matches_latest_comment_play_instance_kexp_id(self):
        request_play_item_kexp_id = 277951
        latest_comment_play_item_kexp_id = Comment.objects.latest('date_created').play_instance.kexp_play_id
        self.assertEquals(request_play_item_kexp_id, latest_comment_play_item_kexp_id)

    def test_comment_created_response_kexp_play_id_matches_latest_comment_play_instance_kexp_id(self):
        response_play_item_kexp_id = int(self.response_data['play_instance_kexp_id'])
        latest_comment_play_item_kexp_id = Comment.objects.latest('date_created').play_instance.kexp_play_id
        self.assertEquals(response_play_item_kexp_id, latest_comment_play_item_kexp_id)


class CommentAjaxUpdateView(TestCase):
    def setUp(self):
        self.kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        self.data_input = {
            'play_instance_kexp_id': 267953,
            'play_instance_name': 'Someone Great',
            'play_instance_airdate': 'June 2, 2019, 6:15 p.m.',
            'comment_id' : 0,
            'comment_text' : 'Another Perfect Summer Song',
        }
        response = self.client.post(reverse('comment'), self.data_input, **self.kwargs)
        json_string = response.content
        self.response_data = json.loads(json_string)

    def test_comment_created_response_id_matches_latest_created_id_again_for_update_tests(self):
        response_comment_id = self.response_data['comment_id']
        latest_comment_id = Comment.objects.latest('date_created').id
        self.assertEquals(response_comment_id, latest_comment_id)

    def test_comment_update_values_correctly_correspond(self):
        original_response = self.response_data
        new_data_input = {
            'play_instance_kexp_id': 267953,
            'play_instance_name': 'Someone Great',
            'play_instance_airdate': 'June 2, 2019, 6:15 p.m.',
            'comment_id' : original_response['comment_id'],
            'comment_text' : 'Another Perfect Summer Song, again',
        }
        response = self.client.post(reverse('comment'), new_data_input, **self.kwargs)
        json_string = response.content
        response_data_update = json.loads(json_string)

        updated_comment = Comment.objects.latest('date_created')

        # make sure ids are the same
        self.assertEquals(response_data_update['comment_id'], updated_comment.id)

        #make sure response text matches db comment text
        self.assertEquals(response_data_update['comment_text'], updated_comment.comment_text)

        #make sure different text has been added
        self.assertNotEquals(original_response['comment_text'], updated_comment.comment_text)

        #make sure original version is using the same kexp play id
        self.assertEquals(int(original_response['play_instance_kexp_id']), updated_comment.play_instance.kexp_play_id)

        #make sure update version is using the same kexp play id
        self.assertEquals(int(response_data_update['play_instance_kexp_id']), updated_comment.play_instance.kexp_play_id)
