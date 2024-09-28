from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from datetime import timedelta, datetime # import the datetime module
import random # import the random module
import django.templatetags.static

image = "https://images.squarespace-cdn.com/content/v1/6200d56d004f564915f49dea/536d54bf-2182-44a4-aa86-47b9b0773ffc/Ethos+1101211900.png"

def main(request):
    context = {'image': image}
    return render(request, 'restaurant/main.html', context)

def order(request):
    specials = [
        {
            'name': 'Pasta',
            'price': 15.99
        },
        {
            'name': 'Burger',
            'price': 12.99
        },
        {
            'name': 'Salad',
            'price': 8.99
        },
        {
            'name': 'Pizza',
            'price': 10.99
        },
        {
            'name': 'Sandwich',
            'price': 7.99
        }
    ]
    daily_special = random.choice(specials)
    context = {'daily_special': daily_special}
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        # retreive the form data
        name = request.POST['name']
        items_ordered = request.POST['items_ordered']
        total_price = sum([float(price) for price in request.POST.getlist('price')])
        
        # generate the 'ready time', random int between 20 and 50 minutes 
        ready_time = datetime.now() + timedelta(minutes=random.randint(20, 50))
        
        context = {'name': name,
                   'items_ordered': items_ordered,
                   'total_price': total_price,
                   'ready_time': ready_time}
        
        return render(request, 'restaurant/confirmation.html', context)
    else:
        return HttpResponse("Invalid request method. Please use POST.")
    