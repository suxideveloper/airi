from django.shortcuts import render

# Create your views here.
def kurish( request):
    return render(request, 'testBg/index.html')