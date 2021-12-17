from django import forms
from django.contrib.auth.models import User
from .models import Profile

my_default_errors = {
    'required': 'پر کردن ای فیلد الزامی است.',
    'invalid': 'عبارت وارد شده نامعتبر است!',
	'max_length': 'تعداد کاراکترها بیش از حد مجاز است!',
	'min_length': 'تعداد کاراکترها کمتر از حد مجاز است!'
}


class SignUpForm(forms.Form):
	username = forms.CharField(error_messages=my_default_errors, label='نام کاربری', max_length=15, min_length=8, 
		widget=forms.TextInput(attrs={"placeholder": "نام کاربری", "class": "form-control"}))

	email = forms.EmailField(error_messages=my_default_errors, label='ایمیل',
		widget=forms.EmailInput(attrs={"placeholder": "ایمیل", "class": "form-control"}))

	password = forms.CharField(error_messages=my_default_errors, label='رمز عبور', min_length=8, 
		widget=forms.PasswordInput(attrs={"placeholder": " رمز عبور", "class": "form-control"}))
	
	password2 = forms.CharField(error_messages=my_default_errors, label='تکرار رمز عبور', min_length=8, 
		widget=forms.PasswordInput(attrs={"placeholder": "تکرار رمز عبور", "class": "form-control"}))

	class Meta:
		model = User
		fields = '__all__'

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username__iexact=username)
		if qs.exists():
			raise forms.ValidationError('نام کاربری وارد شده نامعتبر است!')
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email__iexact=email)
		if qs.exists():
			raise forms.ValidationError('ایمیل وارد شده نامعتبر است!')
		return email

	def clean(self):
		data = self.cleaned_data
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError(" رمز عبور و تکرار رمز عبور مطابقت ندارند!")
		return data


class SignInForm(forms.Form):
	username = forms.CharField(label='نام کاربری یا ایمیل', 
		widget=forms.TextInput(attrs={"placeholder": "نام کاربری یا ایمیل", "class": "form-control"}))

	password = forms.CharField(label='رمز عبور', 
		widget=forms.PasswordInput(attrs={"placeholder": "رمز عبور", "class": "form-control"}))

	class Meta:
		model = User
		fields = '__all__'


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('image',)