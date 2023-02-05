from django.shortcuts import render
from django.http import HttpResponse
from app import qrcode_generator

# Create your views here.


def generate(request, callsign):
    qrcode_img = qrcode_generator.generate_qrcode_image(callsign.upper())

    response = HttpResponse(content_type='image/png')
    qrcode_img.save(response, 'png')

    return response
