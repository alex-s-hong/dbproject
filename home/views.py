from django.shortcuts import render

def post_list(request):
    return render(request, 'home/post_list.html', {})
    
    