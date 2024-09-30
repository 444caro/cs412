from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from datetime import timedelta, datetime # import the datetime module
import random # import the random module
import django.templatetags.static

image = "https://images.squarespace-cdn.com/content/v1/6200d56d004f564915f49dea/536d54bf-2182-44a4-aa86-47b9b0773ffc/Ethos+1101211900.png"

def main(request):
    context = {'image': image, 'time': datetime.now().strftime("%I:%M %p")}
    return render(request, 'restaurant/main.html', context)

def order(request):
    specials = [
        {
            'name': 'Vodka Riggatoni Pasta', 
            'price': 15.99
        },
        {
            'name': 'Georges Double Burger',
            'price': 16.99
        },
        {
            'name': 'Jennies Extra Special Salad',
            'price': 10.99
        },
        {
            'name': 'Three Cheese Pizza with Mushrooms',
            'price': 13.99
        },
        {
            'name': 'Petras Flaming Hot Sandwich',
            'price': 11.99
        }
    ]
    daily_special = random.choice(specials)
    context = {'daily_special': daily_special, 'time': datetime.now().strftime("%I:%M %p")}
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        # retreive the form data
        name = request.POST['name']
        items_ordered = request.POST.getlist('items')
        total_price = 0
        ordered_items = []
        for i in items_ordered:
            i_name, i_price = i.split('-')
            ordered_items.append(i_name)
            total_price += float(i_price)
        
        # generate the 'ready time', random int between 20 and 50 minutes 
        ready_time = datetime.now() + timedelta(minutes=random.randint(20, 50))
        
        context = {'name': name,
                   'items_ordered': ordered_items,
                   'total_price': total_price,
                   'time': datetime.now().strftime("%I:%M %p"),
                   'ready_time': ready_time.strftime("%I:%M %p")}
        
        return render(request, 'restaurant/confirmation.html', context)
    else:
        return HttpResponse("Invalid request method. Please use POST.")
    