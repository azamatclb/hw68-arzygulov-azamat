from rest_framework import serializers
from webapp.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['likes_count', 'liked_by']

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
