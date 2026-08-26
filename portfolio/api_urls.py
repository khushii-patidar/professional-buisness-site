from django.urls import path
from .views import ServiceListAPI, VideoDemoListAPI, PricingPackageListAPI, TestimonialListAPI, LeadCreateAPI

urlpatterns = [
    path('services/', ServiceListAPI.as_view()),
    path('videos/', VideoDemoListAPI.as_view()),
    path('packages/', PricingPackageListAPI.as_view()),
    path('testimonials/', TestimonialListAPI.as_view()),
    path('leads/', LeadCreateAPI.as_view()),
]
