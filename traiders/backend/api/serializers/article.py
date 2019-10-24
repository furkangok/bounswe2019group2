from rest_framework import serializers
from ..models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    def validate(self, attrs):
        attrs['author'] = self.context['request'].user
        return attrs

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id', 'url', 'created_at', 'author']