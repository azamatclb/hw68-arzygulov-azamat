from rest_framework import serializers
from webapp.models import Article, Tag

class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'status', 'tags']

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Длина должна быть больше 3 символов')
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        instance.tags.set(tags)
        return instance
