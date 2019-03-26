from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime 
from . models import *
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt

def chrisgrafil(request):
    return render(request, 'first_app/chrisgrafil.html')

def tickets(request):
    return render(request, 'first_app/tickets.html')

def register(request):
    if request.method!='POST':
        return redirect('/tickets')
    error=False
    print(request.POST)
    if len(request.POST['first_name'])<2:
        messages.error(request, "First name must be greater than 2 characters")
        error=True
    if len(request.POST['last_name'])<2:
        messages.error(request, "Last name must be greater than 2 characters")
        error=True
    if len(request.POST['password'])<8:
        messages.error(request, "Password must be greater than 8 characters")
        error=True
    if request.POST['password']!=request.POST['c_password']:
        messages.error(request, "Passwords must match")
        error=True
    
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, "Email must be in accurate format")
        error=True
    if len(User.objects.filter(email=request.POST['email']))>0:
        messages.error(request, "Email is already taken")
        error=True
    if error:
        return redirect('/tickets')
    
    hashed_pw=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    print (hashed_pw)
    the_user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
    request.session['user_id']=the_user.id 
    return redirect('/dashboard')

def login(request):
    if request.method!='POST':
        return redirect('/tickets')
    try: 
        the_user=User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, "Email or Password invalid")
        return redirect ('/tickets')
    if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):              
        request.session['user_id']=the_user.id
        return redirect('/dashboard')
    messages.error(request, "Email/Password do not match")
    return redirect('/tickets')

def logout(request):
    request.session.clear()
    return redirect('/chrisgrafil')

def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('/chrisgrafil')
    context={
        "user":User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'first_app/dashboard.html', context)

