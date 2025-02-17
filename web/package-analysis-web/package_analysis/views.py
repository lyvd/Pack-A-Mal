from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .forms import PackageSubmitForm

from .helper import Helper
import json

from django.core.files.storage import FileSystemStorage




def dashboard(request):
    if request.method == 'POST':
        form = PackageSubmitForm(request.POST)
        if form.is_valid():
            package_name = form.cleaned_data['package_name'].removesuffix('.apk')
            package_version = form.cleaned_data['package_version']
            ecosystem = form.cleaned_data['ecosystem']
            # Process the form data (e.g., save to database, call an API, etc.)
            # For now, just print the data to the console
            print(f"Package Name: {package_name}, Package Version: {package_version}, Ecosystem: {ecosystem}")

            reports = Helper.run_package_analysis(package_name, package_version, ecosystem)
            form = PackageSubmitForm()
            return render(request, 'package_analysis/dashboard.html', {'form': form, 'reports': reports})
    else:
        form = PackageSubmitForm()
    return render(request, 'package_analysis/dashboard.html', {'form': form})




def upload(request):
    print("request: ", request)
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        # Helper.handle_uploaded_file(uploaded_file_url)
        print("uploaded_file_url: ", uploaded_file_url)
        return HttpResponse(uploaded_file_url   )
    
    return HttpResponse("Error")
    

def submit(request):
    pass
    # if request.method == 'POST':
    #     form = PackageSubmitForm(request.POST)
    #     if form.is_valid():
    #         package_name = form.cleaned_data['package_name']
    #         package_version = form.cleaned_data['package_version']
    #         ecosystem = form.cleaned_data['ecosystem']
    #         # Process the form data (e.g., save to database, call an API, etc.)
    #         # For now, just print the data to the console
    #         print(f"Package Name: {package_name}, Package Version: {package_version}, Ecosystem: {ecosystem}")

    #         reports = Helper.run_package_analysis(package_name, package_version, ecosystem)
    #         return JsonResponse(reports)
    # else:
    #     form = PackageSubmitForm()
    # return render(request, 'package_analysis/submit.html', {'form': form})


def get_wolfis_packages(request):
    return JsonResponse(Helper.get_wolfis_packages())


def configure(request):
    return render(request, "package_analysis/configureSubmit.html")

def analyze(request):
    return render(request, "package_analysis/analyzing.html")

def results(request):
    return render(request, "package_analysis/results.html")



