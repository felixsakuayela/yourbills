from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login
from django.shortcuts import redirect

class SignOut(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/sign_out.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

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