from django.db import models
from django.utils import timezone


class Service(models.Model):
    ICON_CHOICES = [
        ('fa-robot', 'AI Robot'), ('fa-palette', 'Palette'), ('fa-images', 'Images'),
        ('fa-film', 'Film'), ('fa-youtube', 'YouTube'), ('fa-video', 'Video'),
        ('fa-star', 'Star'), ('fa-magic', 'Magic'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fa-star')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class VideoDemo(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def video_id(self):
        url = self.youtube_url or ""
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0].split('&')[0]
        elif 'watch?v=' in url:
            return url.split('watch?v=')[-1].split('&')[0].split('?')[0]
        elif 'embed/' in url:
            return url.split('embed/')[-1].split('?')[0].split('&')[0]
        elif 'shorts/' in url:
            return url.split('shorts/')[-1].split('?')[0].split('&')[0]
        return url.strip('/')

    @property
    def thumbnail_url(self):
        vid = self.video_id
        if vid:
            return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        return ""

    @property
    def watch_url(self):
        vid = self.video_id
        if vid and not vid.startswith('http'):
            return f"https://www.youtube.com/watch?v={vid}"
        return self.youtube_url or "https://www.youtube.com"

    @property
    def embed_url(self):
        vid = self.video_id
        return f"https://www.youtube.com/embed/{vid}?rel=0&modestbranding=1"


class PricingPackage(models.Model):
    name = models.CharField(max_length=100)
    price_min = models.PositiveIntegerField()
    price_max = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    features = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'price_min']

    def __str__(self):
        return f"{self.name} (₹{self.price_min} - ₹{self.price_max})"

    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split(',') if f.strip()]
        return []


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_location = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.rating}★"


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'), ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'), ('completed', 'Completed'), ('closed', 'Closed'),
    ]
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    requirement = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} | {self.mobile} | {self.status}"


class SiteSettings(models.Model):
    hero_headline = models.CharField(max_length=200, default="Bring Your Memories to Life with AI Magic")
    hero_subheadline = models.CharField(max_length=300, default="Professional AI Video Creation, Graphic Design & Video Editing")
    about_text = models.TextField(default="Lokeshh Patidar is a creative professional specializing in AI-powered video creation, graphic design, album designing, and premium video editing. With a passion for storytelling and cutting-edge technology, Lokeshh transforms your precious memories into breathtaking visual experiences that last forever.")
    phone = models.CharField(max_length=20, default="7803863255")
    email = models.EmailField(default="lokeshhaitools@gmail.com")
    whatsapp_number = models.CharField(max_length=20, default="917803863255")
    whatsapp_message = models.CharField(max_length=200, default="Hi Lokeshh, I am interested in your work.")
    meta_title = models.CharField(max_length=200, default="Lokeshh Ai Tools | AI Video Creation & Graphic Design")
    meta_description = models.TextField(default="Professional AI video creation, graphic design, album designing & video editing by Lokeshh Patidar.")

    @property
    def instagram_url(self):
        return "https://www.instagram.com/lokeshh_ai_tools?igsi=MTZqeXN5emNvbHpxeQ=="

    @property
    def youtube_url(self):
        return "https://youtube.com/@lokeshh_ai_tools?si=qtopkDZ4dVuQwoj5"

    class Meta:
        verbose_name = 'Site Settings'

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        if obj.email in ["lokeshpatidarforyou@gmail.com", ""]:
            obj.email = "lokeshhaitools@gmail.com"
            obj.save()
        return obj
