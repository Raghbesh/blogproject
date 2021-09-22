from django.shortcuts import reverse ,redirect
from django.views.generic import * #TemplateView,ListView,DetailView,CreateView,UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings

class HomeView(TemplateView):
	template_name = 'base.html'


class SignupFormView(FormView):
	template_name='signupform.html'
	form_class= SignupForm
	success_url=reverse_lazy('raghavapp:login')

	def form_valid(self,form):
		u_name=form.cleaned_data['username']
		p_word=form.cleaned_data['password']
		cp_word=form.cleaned_data['confirm_password']
		if p_word==cp_word:
			if User.objects.filter(username=u_name):
				return render(self.request,self.template_name,{
				'form':form,
				'error':"Email is already taken"})
			else:
				User.objects.create_user(username=u_name,password=p_word)
		else:
			return render(self.request,self.template_name,{
				'form':form,
				'error':"Password do not match"})

		return super().form_valid(form)


class LoginFormView(FormView):
	template_name='login.html'
	form_class=LoginForm
	success_url=reverse_lazy('raghavapp:bloglist')

	def get(self,request):
		if request.user.is_authenticated:
			return redirect('raghavapp:bloglist')
		return super().get(request)

	def form_valid(self,form):
		u_name=form.cleaned_data['username']
		p_word=form.cleaned_data['password']
		user=authenticate(username=u_name,password=p_word)
		if user is not None:
			login(self.request,user)
		else:
			return render(self.request,self.template_name,{'form':form,'error':"Invalid Candential"})
		return super().form_valid(form)

	def get_success_url(self,**kwargs):
		self.next_url=self.request.POST.get('next')
		if self.next_url is not None:
			return self.next_url
		else:
			return self.success_url


class LogoutView(View):
	def get(self,request):
		logout(request)
		return redirect('raghavapp:login')

class BlogCreateView(LoginRequiredMixin, CreateView):
	template_name= 'blogcreate.html'
	model = Profile
	form_class = BlogCreateForm
	success_url = reverse_lazy('raghavapp:home')

	def dispatch(self,request):
		if not request.user.is_authenticated:
			return redirect('raghavapp:login')
		return super().dispatch(request)

class BloglistView(LoginRequiredMixin, ListView):
	template_name = 'profile.html'
	queryset = Profile.objects.all()
	context_object_name = 'postlist'

class BlogUpdateView(UpdateView):
	template_name = 'profileupdate.html'
	model= Profile
	form_class = BlogUpdateForm
	success_url= '/bloglist/'


class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Django Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("raghavapp:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)
# Create your views here.
