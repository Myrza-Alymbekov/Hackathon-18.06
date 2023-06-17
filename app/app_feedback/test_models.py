from django.test import TestCase

from .models import Feedback, FeedbackFiles, FeedbackComments
from .mixins import TestMixin


class TestFeedback(TestMixin, TestCase):

    def test_feedback_fields(self):
        self.assertEqual(self.feedback.client, self.user_client)
        self.assertEqual(self.feedback.error_description, "error_description")


