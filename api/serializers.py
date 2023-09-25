from rest_framework import serializers
from main.models import Modul, Post

class ModulSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modul
        fields = (
            'id',
            'title',
            'category',
            'excerpt',
            'content',
            'file',
            'status',
            'created_at',
            'updated_at',
            'slug',
            'published'
        )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'phone',
            'email',
            'invoice',
            'type',
            'date',
            'category',
        )