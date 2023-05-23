from django.shortcuts import render


def handler404(request,exception):
    return render(request,'base/nout_found_404.html')