from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Service, VideoDemo, PricingPackage, Testimonial, Lead, SiteSettings
from .serializers import ServiceSerializer, VideoDemoSerializer, PricingPackageSerializer, TestimonialSerializer, LeadSerializer
from .forms import LeadForm

LANGUAGES = [
    'Hindi', 'English', 'Gujarati', 'Punjabi', 'Marathi',
    'Bengali', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Bhojpuri', 'Rajasthani'
]


DEFAULT_INSTAGRAM_URL = "https://www.instagram.com/lokeshh_ai_tools?igsi=MTZqeXN5emNvbHpxeQ=="
DEFAULT_YOUTUBE_URL = "https://youtube.com/@lokeshh_ai_tools?si=qtopkDZ4dVuQwoj5"


def get_base_context():
    site = SiteSettings.get_settings()
    msg = site.whatsapp_message.replace(' ', '%20')
    insta = getattr(site, 'instagram_url', None) or DEFAULT_INSTAGRAM_URL
    yt = getattr(site, 'youtube_url', None) or DEFAULT_YOUTUBE_URL
    return {
        'site': site,
        'whatsapp_url': f"https://wa.me/{site.whatsapp_number}?text={msg}",
        'call_url': f"tel:{site.phone}",
        'instagram_url': insta,
        'youtube_url': yt,
    }


def home(request):
    context = get_base_context()
    context.update({
        'services': Service.objects.filter(is_active=True),
        'videos': VideoDemo.objects.filter(is_active=True),
        'packages': PricingPackage.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'languages': LANGUAGES,
        'form': LeadForm(),
    })
    return render(request, 'portfolio/home.html', context)


def services(request):
    context = get_base_context()
    context['services'] = Service.objects.filter(is_active=True)
    return render(request, 'portfolio/services.html', context)


def gallery(request):
    context = get_base_context()
    context['videos'] = VideoDemo.objects.filter(is_active=True)
    return render(request, 'portfolio/gallery.html', context)


def pricing(request):
    context = get_base_context()
    context['packages'] = PricingPackage.objects.filter(is_active=True)
    return render(request, 'portfolio/pricing.html', context)


import logging
import urllib.parse

logger = logging.getLogger(__name__)


def _get_whatsapp_inquiry_url(lead):
    site = SiteSettings.get_settings()
    text = (
        f"🔔 *New Inquiry - Lokeshh Ai Tools*\n\n"
        f"👤 *Client Name:* {lead.name}\n"
        f"📱 *Phone / WhatsApp:* {lead.mobile}\n"
        f"✉️ *Email:* {lead.email}\n\n"
        f"📝 *Project Requirement:*\n{lead.requirement}\n\n"
        f"🌐 *Sent via Website Inquiry Form*"
    )
    encoded_text = urllib.parse.quote(text)
    return f"https://wa.me/{site.whatsapp_number}?text={encoded_text}"


def contact(request):
    context = get_base_context()
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            _send_emails(lead)
            wa_url = _get_whatsapp_inquiry_url(lead)
            messages.success(request, f'✅ Thank you {lead.name}! Your inquiry has been saved.')
            return redirect(wa_url)
        context['form'] = form
    else:
        context['form'] = LeadForm()
    return render(request, 'portfolio/contact.html', context)


def submit_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            email_sent = _send_emails(lead)
            wa_url = _get_whatsapp_inquiry_url(lead)
            return JsonResponse({
                'success': True,
                'message': f'Thank you {lead.name}! Your inquiry details have been saved.',
                'wa_url': wa_url,
                'lead_name': lead.name,
                'email_sent': email_sent,
            })
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})


def _send_emails(lead):
    site = SiteSettings.get_settings()
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'lokeshhaitools@gmail.com')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', admin_email)
    
    clean_phone = lead.mobile.replace('+', '').replace(' ', '')
    admin_subject = f"🔔 New Client Inquiry: {lead.name} ({lead.mobile})"
    admin_text = (
        f"New Inquiry Received on Lokeshh Ai Tools Website:\n\n"
        f"Name: {lead.name}\n"
        f"Phone/WhatsApp: {lead.mobile}\n"
        f"Email: {lead.email}\n"
        f"Requirement: {lead.requirement}\n"
        f"Submitted At: {lead.submitted_at}\n\n"
        f"Reply to client on WhatsApp: https://wa.me/{clean_phone}"
    )

    client_subject = f"Thank You for Contacting Lokeshh Ai Tools!"
    client_text = (
        f"Dear {lead.name},\n\n"
        f"Thank you for reaching out to Lokeshh Ai Tools. We have received your project requirement:\n\n"
        f"\"{lead.requirement}\"\n\n"
        f"We will review your details and connect with you shortly.\n\n"
        f"Best Regards,\n"
        f"Lokeshh Patidar\n"
        f"Lokeshh Ai Tools Studio\n"
        f"📞 +91 {site.phone}\n"
        f"WhatsApp: https://wa.me/{site.whatsapp_number}"
    )

    success = False
    try:
        send_mail(
            subject=admin_subject,
            message=admin_text,
            from_email=from_email,
            recipient_list=[admin_email],
            fail_silently=False,
        )
        send_mail(
            subject=client_subject,
            message=client_text,
            from_email=from_email,
            recipient_list=[lead.email],
            fail_silently=True,
        )
        success = True
    except Exception as e:
        logger.warning(f"Email notification via SMTP could not be sent: {e}")
        success = False

    return success


# ── API Views ──────────────────────────────────────────────────────────────────
class ServiceListAPI(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer


class VideoDemoListAPI(generics.ListAPIView):
    queryset = VideoDemo.objects.filter(is_active=True)
    serializer_class = VideoDemoSerializer


class PricingPackageListAPI(generics.ListAPIView):
    queryset = PricingPackage.objects.filter(is_active=True)
    serializer_class = PricingPackageSerializer


class TestimonialListAPI(generics.ListAPIView):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer


class LeadCreateAPI(APIView):
    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            _send_emails(lead)
            return Response({'success': True}, status=201)
        return Response({'success': False, 'errors': serializer.errors}, status=400)
