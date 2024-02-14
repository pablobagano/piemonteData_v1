from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
from .utils import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm


# Create your views here.
@login_required
def index(request):
    return HttpResponse('<h1>Hi</h1>')

@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'user':request.user})

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'