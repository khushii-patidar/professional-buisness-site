from django.contrib import admin
from django.utils.html import format_html
from .models import Service, VideoDemo, PricingPackage, Testimonial, Lead, SiteSettings


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title']


@admin.register(VideoDemo)
class VideoDemoAdmin(admin.ModelAdmin):
    list_display = ['title', 'youtube_url', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(PricingPackage)
class PricingPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_range', 'is_featured', 'order', 'is_active']
    list_editable = ['is_featured', 'order', 'is_active']

    def price_range(self, obj):
        return f"₹{obj.price_min:,} – ₹{obj.price_max:,}"
    price_range.short_description = 'Price Range'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_location', 'rating', 'is_active', 'created_at']
    list_editable = ['is_active']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'email', 'status', 'submitted_at', 'whatsapp_link']
    list_editable = ['status']
    list_filter = ['status']
    search_fields = ['name', 'mobile', 'email']
    readonly_fields = ['submitted_at']

    def whatsapp_link(self, obj):
        url = f"https://wa.me/91{obj.mobile}"
        return format_html('<a href="{}" target="_blank">📱 Chat</a>', url)
    whatsapp_link.short_description = 'WhatsApp'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Section', {'fields': ('hero_headline', 'hero_subheadline')}),
        ('About Section', {'fields': ('about_text',)}),
        ('Contact Details', {'fields': ('phone', 'email', 'whatsapp_number', 'whatsapp_message')}),
        ('SEO', {'fields': ('meta_title', 'meta_description')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
