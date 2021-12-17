from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import SignUpForm, SignInForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile
from blog.models import Article
from braces.views import AnonymousRequiredMixin

# Create your views here.

class SignUpView(AnonymousRequiredMixin, View):
	form_class = SignUpForm
	template_name = 'accounts/sign_up.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class
		context = {"form": form}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			password2 = form.cleaned_data.get('password2')
			try:
				user = User.objects.create_user(username=username, email=email, password=password)
			except:
				user = None

			if user != None:
				messages.success(request, 'ثبت نام با موفقیت انجام شد!', 'success')
				return redirect('accounts:sign_in')
			else:
				messages.error(request, 'ثبت نام با موفقیت انجام نشد!', 'warning')

		context = {"form": form}
		return render(request, self.template_name, context)


class SignInView(AnonymousRequiredMixin, View):
	form_class = SignInForm
	template_name = 'accounts/sign_in.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class
		context = {"form": form}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST or None)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password=password)

			if user != None:
				login(request, user)
				messages.success(request, 'شما وارد شدید.', 'success')
				return redirect('blog:articles_list')
			else:
				messages.error(request, 'نام کاربری یا رمز عبور نامعتبر است!', 'warning')

		context = {"form": form}
		return render(request, self.template_name, context)


class SignOutView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.info(request, 'شما خارج شدید!', 'info')
		return redirect('blog:articles_list')


class DashboardView(LoginRequiredMixin, View):
	template_name = 'accounts/dashboard.html'
	form_class = ProfileForm

	def get(self, request, pk, *args, **kwargs):
		user = get_object_or_404(User, pk=pk)
		articles = Article.objects.filter(author=user)
		Profile.objects.get_or_create(user=request.user)
		context = {"user": user, "articles":articles,  "form": self.form_class}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'حساب کاربری شما بروزرسانی با موفقیت بروزرسانی شد.', 'success')
			return redirect('accounts:dashboard', request.user.pk)