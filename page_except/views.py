from django.shortcuts import render

# Create your views here.
def handler404(request,exception):

    return render(request,'base/nout_found_404.html')