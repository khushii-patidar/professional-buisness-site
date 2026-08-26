#!/usr/bin/env python
"""Initial data setup — run once after migrate."""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'editor_lokesh.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from portfolio.models import Service, VideoDemo, PricingPackage, Testimonial, SiteSettings

print("🚀 Setting up Lokeshh Ai Tools data...")

if not User.objects.filter(username='Lokeshh_Ai_Tools').exists():
    User.objects.create_superuser('Lokeshh_Ai_Tools', 'lokeshpatidarforyou@gmail.com', 'Lokesh@2024Admin')
    print("✅ Admin: Lokeshh_Ai_Tools / Lokesh@2024Admin")

SiteSettings.get_settings()
print("✅ Site settings ready")

services = [
    ('AI Creation', 'Cutting-edge AI-powered content creation including images, videos, and animations that bring your imagination to life with stunning realism.', 'fa-robot', 1),
    ('Graphic Designing', 'Premium graphic design for banners, posters, social media, logos, and all marketing materials with a professional touch.', 'fa-palette', 2),
    ('Album Designing', 'Beautifully crafted wedding, birthday and family photo albums with creative layouts that tell your story memorably.', 'fa-images', 3),
    ('Video Editing', 'Professional video editing with color grading, transitions, music sync, and cinematic effects for weddings, events and reels.', 'fa-film', 4),
    ('YouTube Content Creation', 'Complete YouTube channel management including thumbnails, intros, editing, and content strategy to grow your audience.', 'fa-youtube', 5),
    ('RIP AI Videos', 'Heartfelt AI tribute videos to honor your loved ones, created with care, emotion and cutting-edge AI technology.', 'fa-video', 6),
]
for title, desc, icon, order in services:
    obj, c = Service.objects.get_or_create(title=title, defaults={'description': desc, 'icon': icon, 'order': order})
    if c: print(f"   ✅ {title}")

videos = [
    ('AI Creation Demo 1', 'https://youtu.be/kr0hRZkkbKc', 1),
    ('AI Creation Demo 2', 'https://youtu.be/p1ai08A3KL8', 2),
    ('AI Creation Demo 3', 'https://youtu.be/pG0QbvTL4YA', 3),
    ('AI Creation Demo 4', 'https://youtu.be/QzvsmBF6Y1Q', 4),
    ('AI Creation Demo 5', 'https://youtu.be/umjkhWbmAtY', 5),
]
for title, url, order in videos:
    obj, c = VideoDemo.objects.get_or_create(youtube_url=url, defaults={'title': title, 'order': order})
    if c: print(f"   ✅ {title}")

packages = [
    ('Basic Package', 2999, 6999, 'Perfect for simple video creation', 'HD Quality Video,Background Music,Basic Effects,2 Revisions,Fast Delivery', False, 1),
    ('Premium Package', 4999, 9999, 'Professional quality with advanced AI effects', '4K Quality Video,Premium Music,Advanced AI Effects,5 Revisions,Priority Delivery,Color Grading', True, 2),
    ('Krishna Special', 4999, 14999, 'Divine themed videos with special effects', 'Divine Theme Design,Special AI Effects,Custom Music,Unlimited Revisions,Express Delivery', False, 3),
    ('Full Realistic', 14999, 34999, 'Hyper-realistic AI video creation', 'Hyper Realistic AI,Cinematic Quality,Custom Soundtrack,Unlimited Revisions,Commercial Rights', False, 4),
    ('Jain Family', 9999, 39999, 'Complete family tribute with traditional elements', 'Full Family Tribute,Traditional Elements,Multiple Videos,Photo Enhancement,Lifetime Storage', False, 5),
]
for name, pmin, pmax, desc, feat, featured, order in packages:
    obj, c = PricingPackage.objects.get_or_create(name=name, defaults={'price_min': pmin, 'price_max': pmax, 'description': desc, 'features': feat, 'is_featured': featured, 'order': order})
    if c: print(f"   ✅ {name}")

testimonials = [
    ('Rajesh Sharma', 'Indore, MP', 'Lokeshh bhai ne meri maa ka RIP video bahut sundar banaya. Poori family ro padi. Bahut professional kaam! Highly recommended!', 5),
    ('Sunita Patel', 'Ahmedabad, Gujarat', 'Amazing work on our wedding album! The AI effects were stunning. Everyone loved it. Will definitely hire again!', 5),
    ('Amit Verma', 'Jaipur, Rajasthan', 'Mere YouTube channel ke liye bahut achi editing ki. Views 3x ho gaye. Lokeshh ji ka kaam satpratishat sahi hai!', 5),
    ('Priya Gupta', 'Bhopal, MP', 'The graphic designs were beyond my expectations. Fast delivery, great communication, top-notch quality. 10/10!', 5),
    ('Mohan Das', 'Udaipur, Rajasthan', 'Pitaji ki barsi ke liye ek bahut touching video banai. Ghar mein sabko bahut pasand aayi. Thank you Lokeshh ji!', 5),
    ('Kavita Singh', 'Lucknow, UP', 'My birthday album was absolutely gorgeous! AI effects made it look like a Bollywood production. Best money spent!', 5),
]
for name, loc, msg, rating in testimonials:
    obj, c = __import__('portfolio.models', fromlist=['Testimonial']).Testimonial.objects.get_or_create(client_name=name, defaults={'client_location': loc, 'message': msg, 'rating': rating})
    if c: print(f"   ✅ {name}")

print()
print("🎉 Done!")
print("="*45)
print("Admin URL:  http://127.0.0.1:8000/admin/")
print("Username:   Lokeshh_Ai_Tools")
print("Password:   Lokesh@2024Admin")
print("⚠️  Change password after first login!")
print("="*45)
