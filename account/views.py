from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout
from django.shortcuts import redirect

def SignOut(request):
    logout(request)
    return redirect('signin')

class SignIn(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = 'account/sign_in.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.request.session.flush()
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)