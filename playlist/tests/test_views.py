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
        print(cls.response_data)

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




#Comment should not save if text blank



#---comment updating

# Comment Text should still not be blank

#Comment Last Edited time should update
#Comment last_edited time should be more recent than created

#play_instance ForeignKey should be the same
