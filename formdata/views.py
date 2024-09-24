from django.shortcuts import render


#show the contact form
def show_form (request):
    template_name = "formdata/form.html"
    return render(request, template_name)

#process the form submission and generate a result 
def submit(request):
    template_name = "formdata/confirmation.html"
    if request.POST:
        name = request.POST('name')
        favorite_color = request.POST('favorite_color')
    context = {
        'name': name,
        'favorite_color': favorite_color
    }
    return render(request, template_name, context=context)

