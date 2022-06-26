from django.shortcuts import render
from django import forms

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

import numpy as np

# Create your views here.
class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Upload Image')

def index(request):
    return render(request, 'index.html')

def processUploadedFile(file):
    with open('img.jpg', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def processImage(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        processUploadedFile(request.FILES['image'])

        model = ResNet50(weights='imagenet')

        img_path = 'img.jpg'
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        preprocessed_image = preprocess_input(x)

        prdctns = model.predict(preprocessed_image)

        html = decode_predictions(prdctns, top=3)[0]
        res = []
        for en in html:
            res.append((en[1], np.round(en[2]*100,2)))
        return render(request, 'result.html', {'res': res })

    return render(request, 'result.html')
