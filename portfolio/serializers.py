from rest_framework import serializers
from .models import Service, VideoDemo, PricingPackage, Testimonial, Lead


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'icon', 'order']


class VideoDemoSerializer(serializers.ModelSerializer):
    embed_url = serializers.ReadOnlyField()

    class Meta:
        model = VideoDemo
        fields = ['id', 'title', 'youtube_url', 'embed_url', 'description', 'order']


class PricingPackageSerializer(serializers.ModelSerializer):
    features_list = serializers.SerializerMethodField()

    class Meta:
        model = PricingPackage
        fields = ['id', 'name', 'price_min', 'price_max', 'description', 'features_list', 'is_featured']

    def get_features_list(self, obj):
        return obj.get_features_list()


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'client_name', 'client_location', 'message', 'rating']


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'mobile', 'email', 'requirement']
