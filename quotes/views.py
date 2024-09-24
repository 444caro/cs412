from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import datetime # import the datetime module
import random # import the random module
import django.templatetags.static

quotes = [
   "What really changed was when I moved to LA and my eyes were open to so many new things and fun people. I started doing things I never thought I would do and the new sound reflected what was genuinely going on in my life. - Chappell Roan",
   "Give it a chance, it's going to feel silly. Allow yourself to feel silly and fun. - Chappell Roan",
   "If I saw myself now when I was 16 I would be like no way there's no way I would do that. Let myself write a song that's about being a hot person and being a cheerleader, I'm too serious for that. If I had to give her advice I would say follow your gut and that you're cool. I always told myself I wish I was cooler, prettier, smarter, I would have told her that you are enough exactly how you are in every aspect. - Chappell Roan",
   "It's awesome to say no to things, even though they're offering a lot of money. I have the power to say no. - Chappell Roan" 
]

images = [
    "images/chappell1.jpg",
    "images/chappell2.jpg",
    "images/chappell3.jpg",
    "images/chappell4.jpg"
]

# show a random quote and image
def quote(request):
    # get a random quote
    quote = random.choice(quotes)
    image = random.choice(images)
    current_time = datetime.datetime.now()
    # pass the quote to the template
    return render(request, 'quotes/quote.html', {'quote': quote, 'image': image, 'current_time': current_time})

# show all quotes
def show_all(request):
    current_time = datetime.datetime.now()
    context={
        'quotes': quotes,
        'images': images,
        'current_time': current_time
    }
    # pass all quotes to the template
    return render(request, 'quotes/show_all.html', context)

# show the about page
def about(request):
    current_time = datetime.datetime.now()
    bio = "Chappell Roan is a singer-songwriter from Willard, Missouri. She moved to Los Angeles to pursue her music career and has released several singles and an EP. Her music is a mix of pop, rock, and alternative influences. She has been praised for her powerful voice and emotional lyrics."
    context = {'bio': bio,
               'current_time': current_time}
    return render(request, 'quotes/about.html', context)