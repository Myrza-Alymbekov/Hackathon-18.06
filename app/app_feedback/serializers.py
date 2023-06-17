from rest_framework import serializers

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_button')

    class Meta:
        model = Feedback
        fields = '__all__'
