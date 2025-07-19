from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .models import student
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')  # Change 'home' to your homepage url name
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomerSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, is_customer=True)
        return user

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerSignupForm()
    return render(request, 'customer_signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Custom redirect based on profile
            try:
                if user.userprofile.is_customer:
                    return render(request,'home.html')  # Change to your customer home url name
            except UserProfile.DoesNotExist:
                pass
            return redirect('home')  # Default home
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signin(request):
    return login_view(request)

def mensclothing(request):
    return render(request, 'mensclothing.html')

def womens(request):
    return render(request, 'womens.html')

def kidsclothing(request):
    return render(request, 'kids.html')

class StudentForm(forms.ModelForm):
    class Meta:
        model = student
        fields = ['name', 'age', 'email']

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'home2.html')  # Change 'home' to your homepage url name
    else:
        form = StudentForm()
    return render(request, 'home.html', {'form': form})

def home2(request):
    return render(request, 'home2.html')