from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('books:get-obj')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            print('welcome')
            return redirect('books:get-obj')
        else:
            print('go away')
            return redirect('auth:register')
    return render(request, 'authenticate/login.html')

# def cabinet(request):
#     if request.user.is_authenticated:

# username
# password
# email 
# firstname 
# lastname

def register_view(request):
    if request.user.is_authenticated:
        return redirect('books:get-obj')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        firstname = request.POST.get('firstname', None) 
        lastname = request.POST.get('lastname', None)
        print(f'username: {username}\npassword: {password}\nemail: {email}\nfirstname: {firstname}\nlastname: {lastname}')
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=firstname,
                last_name=lastname
            )
            user.set_password(password)
            user.save()
        except:
            return redirect('auth:login')
        return redirect('auth:login')
    return render(request, 'authenticate/register.html')

def logout_view(request):
    logout(request)
    return redirect('books:get-obj')