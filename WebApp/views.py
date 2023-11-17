import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import GeneralInformation, Tutorial
from .forms import GeneralInformationForm, TutorialForm
from django.contrib import messages

api_key = '06dad2aacc0f5e3a3ec93ae82eefb2d4'

"""
Renders the 'index.html' template with a list of GeneralInformation objects.
Displays general information on the index page.
"""

def index(request):
    general_info_list = GeneralInformation.objects.all()
    return render(request, 'index.html', {'general_info_list': general_info_list})

"""Handles the addition of GeneralInformation via a form submission.
If the form is valid, saves the new GeneralInformation, displays a success message, 
and redirects to the index page. If the form is invalid, displays an error message and redirects to the index page.
"""

def add_general_info(request):
    if request.method == 'POST':
        form = GeneralInformationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'General information added successfully.')
            return redirect('index')
        else:
            messages.error(
                request, 'There was an error. Please check your input.', extra_tags='danger')

    return redirect('index')  # Redirect to 'index' after processing the form

"""
Handles the update of GeneralInformation via a form submission.
Retrieves the existing GeneralInformation object based on the provided info_id. 
If the form is valid, updates the GeneralInformation, displays a success message, and redirects to the index page. 
If the form is invalid, displays an error message and redirects to the index page.
"""

def update_general_info(request, info_id):
    info = get_object_or_404(GeneralInformation, id=info_id)
    if request.method == 'POST':
        form = GeneralInformationForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            print("test here")
            messages.success(
                request, 'General information updated successfully.')
            return redirect('index')
        else:
            messages.error(
                request, 'There was an error. Please check your input.', extra_tags='danger')

    return redirect('index')

"""
Handles the deletion of GeneralInformation.
Retrieves the existing GeneralInformation object based on the provided info_id. 
If the form is submitted as a POST request,it tries to delete the GeneralInformation, 
displays a success message if successful, and redirects to the index page. 
If the deletion didn't succeed, displays an error message and redirects to the index page.
"""

def delete_general_info(request, info_id):
    info = get_object_or_404(GeneralInformation, id=info_id)

    if request.method == 'POST':
        try:
            info.delete()
            messages.success(
                request, 'General information deleted successfully.')
            return redirect('index')
        except Exception as e:
            messages.error(
                request, f'There was an error. The information could not be deleted. Error: {e}', extra_tags='danger')
            return redirect('index')

"""
Renders the 'tutorials.html' template with a list of Tutorial and GeneralInformation objects.
Displays a list of tutorials along and passes associated general information for linking tutorials to specific informations.
"""

def tutorials(request):
    tutorial_list = Tutorial.objects.all()
    general_info_list = GeneralInformation.objects.all()
    return render(request, 'tutorials.html', {'tutorial_list': tutorial_list, 'general_info_list': general_info_list})

"""
Handles the addition of Tutorial via a form submission.
If the form is valid, saves the new Tutorial, displays a success message, and redirects to the tutorials page. 
If the form is invalid, displays an error message and redirects to the tutorials page.
"""

def add_tutorial(request):
    if request.method == 'POST':
        form = TutorialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tutorial added successfully.')
            return redirect('tutorials')
        else:
            messages.error(
                request, 'There was an error. Please check your input.', extra_tags='danger')

    return redirect('tutorials')

"""
Handles the update of Tutorial via a form submission.
Retrieves the existing Tutorial object based on the provided tutorial_id. 
If the form is valid, updates the Tutorial, displays a success message, and redirects to the tutorials page. 
If the form is invalid, displays an error message and redirects to the tutorials page.
"""

def update_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    if request.method == 'POST':
        form = TutorialForm(request.POST, instance=tutorial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tutorial updated successfully.')
            return redirect('tutorials')
        else:
            messages.error(
                request, 'There was an error. Please check your input.', extra_tags='danger')

    return redirect('tutorials')

"""
Handles the deletion of Tutorial.
Retrieves the existing Tutorial object based on the provided tutorial_id. 
If the form is submitted as a POST request,it tries to delete the Tutorial, 
displays a success message if successful, and redirects to the tutorials page. 
If the deletion didn't succeed, displays an error message and redirects to the tutorials page.
"""

def delete_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    if request.method == 'POST':
        try:
            tutorial.delete()
            messages.success(
                request, 'Tutorial deleted successfully.')
            return redirect('tutorials')
        except Exception as e:
            messages.error(
                request, f'There was an error. The tutorial could not be deleted. Error: {e}', extra_tags='danger')
            return redirect('tutorials')

    return redirect('tutorials')


"""
Retrieves weather data for a given city from the OpenWeatherMap API.
Constructs an API URL based on the provided city name and sends a request to the OpenWeatherMap API. 
If successful, extracts temperature, humidity, and weather description from the API response and returns this information in a JsonResponse. 
If there is an error in the API request, returns a JsonResponse with an error message and a status code of 500.
"""

def get_weather_data(request, city):
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    try:
        response = requests.get(api_url)
        data = response.json()

        weather_info = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
        }
        print(weather_info)
        return JsonResponse(weather_info)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
