from rest_framework import serializers
from . import models


class Definition(serializers.ModelSerializer):
    contributor = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = models.Definition
        fields = ('text', 'contributor',
                  'is_primary', 'created_at')


class Word(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='word-detail',
        lookup_field='slug',
        read_only=True)
    definitions = Definition(many=True, required=False)
    creator = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = models.Word
        fields = ('label', 'creator', 'url',
                  'created_at', 'definitions')

    def create(self, validated_data):
        definitions = []
        if 'definitions' in validated_data:
            definitions = validated_data.pop('definitions')
        word = models.Word.objects.create(**validated_data)
        for definition in definitions:
            is_primary = True if definition == definitions[0] else False
            models.Definition.objects.create(
                word=word,
                contributor=word.creator,
                is_primary=is_primary,
                **definition)
        return word