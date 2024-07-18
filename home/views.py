from django.shortcuts import render,redirect
from datetime import datetime
from home.api_calls.weatherAPI import get_weather_data
from django.views.decorators.csrf import csrf_exempt
from home.AI_Model.ai_train import predict_fire

from django.conf import settings
import os

from .forms import ImageUploadForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage
from userauths.models import User

def send_wildfire_result_email(user_emails, result, image_path):
    subject = 'Wildfire Detection Result'
    from_email = settings.EMAIL_HOST_USER
    
    for user_email in user_emails:
        to_email = user_email.email  # Assuming 'email' is the field name
        html_content = render_to_string('home/app/email.html', {'result': result})
        
        msg = EmailMultiAlternatives(subject, '', from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        
        # Attach the uploaded image
        with open(image_path, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<uploaded_image>')
            img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
            msg.attach(img)
        
        msg.send()

#----------------------------------------------------------------------------
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def unix_to_human_readable(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
#----------------------------------------------------------------------------

@csrf_exempt
def loading(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        weather_data = get_weather_data(latitude, longitude)
        
        request.session['weather_data'] = weather_data
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        return redirect("home:home")
    else:
        latitude = 22.7179
        longitude = 75.8333
    return render(request, 'home/app/loading_page.html')

def home(request):
    weather_data = request.session.get('weather_data')
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')
    image_filename = None
    result=0

    # Convert temperatures to Celsius
    weather_data['main']['temp'] = kelvin_to_celsius(weather_data['main']['temp'])
    weather_data['main']['feels_like'] = kelvin_to_celsius(weather_data['main']['feels_like'])

    # Convert Unix time to human-readable format
    weather_data['sys']['sunrise'] = unix_to_human_readable(weather_data['sys']['sunrise'])
    weather_data['sys']['sunset'] = unix_to_human_readable(weather_data['sys']['sunset'])

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_filename = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            result = predict_fire(image_path)
            user_emails = User.objects.all()  # Assuming User is your model
            print(image_filename)
            send_wildfire_result_email(user_emails, result, image_path)
    else:
        form = ImageUploadForm()
        
    context = {
        'form':form,
        'result': result,
        'weather_data': weather_data,
        'longitude': longitude,
        'latitude': latitude,
        'image_path': image_filename,
    }
    return render(request, 'home/app/home.html', context)

def mapview(request):
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')
    api_key = 'WeDkOLJgAzvafGXb9MVB'
    context = {
        'longitude': longitude,
        'latitude': latitude,
        'api_key_map': api_key,
    }
    return render(request, 'home/app/map.html', context)


