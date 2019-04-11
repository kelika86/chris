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

def add(request):
    if not 'user_id' in request.session:
        return redirect('/chrisgrafil')
    if request.method!='POST':
        return redirect ('/dashboard')
    Ticket.objects.create(venue=request.POST['venue'], quantity=request.POST['quantity'], loop=request.POST['loop'], purchaser=User.objects.get(id=request.session['user_id']))
    return redirect ('/confirmation')
    

def confirmation(request):
    if not 'user_id' in request.session:
        return redirect('/chrisgrafil')
    
    context={
        "user":User.objects.get(id=request.session['user_id']),
        "tickets": Ticket.objects.filter(purchaser=User.objects.get(id=request.session['user_id'])).annotate(total=Sum(F('quantity') * F('price'),  output_field=FloatField())).annotate(tax=ExpressionWrapper(F('quantity') * F('price')*0.0725,  output_field=FloatField())).annotate(total_price=ExpressionWrapper(F('quantity') * F('price') + F('tax'),  output_field=FloatField())),
        
    }
    return render(request, 'first_app/confirmation.html', context)

def edit(request, tic_id):
    context={
        "ticket": Ticket.objects.get(id=tic_id)
    }
    return render(request, 'first_app/edit.html', context)

def modify(request, tic_id):
    if request.method!='POST':
        return redirect('/dashboard')
    t=Ticket.objects.get(id=tic_id)
    t.venue=request.POST['venue']
    t.quantity=request.POST['quantity']
    t.loop=request.POST['loop']
    t.save()
    return redirect('/confirmation')

def delete(request, tic_id):
    if not 'user_id' in request.session:
        return redirect ('/chrisgrafil')
    Ticket.objects.get(id=tic_id).delete()
    return redirect ('/confirmation')

def payment(request):
    context={
        "tickets": Ticket.objects.filter(purchaser=User.objects.get(id=request.session['user_id'])).annotate(total=Sum(F('quantity') * F('price'),  output_field=FloatField())).annotate(tax=ExpressionWrapper(F('quantity') * F('price')*0.0725,  output_field=FloatField())).annotate(total_price=ExpressionWrapper(F('quantity') * F('price') + F('tax'),  output_field=FloatField())),
    }
    return render(request, 'first_app/payment.html', context)

def process(request):
    if request.method!='POST':
        return redirect('/payment')
    error=False
    print(request.POST)
    if len(request.POST['full_name'])<2:
        messages.error(request, "Full name must be greater than 2 characters")
        error=True
    if len(request.POST['cc_number'])!=16:
        messages.error(request, "Credit card must be valid and contain 16 numbers")
        error=True
   
    if len(request.POST['cvc'])!=3:
        messages.error(request, "CVC must be valid and contain 3 numbers")
        error=True
    if error:
        return redirect('/payment')
    else:
        
        Order.objects.create(full_name=request.POST['full_name'], cc_number=request.POST['cc_number'],exp_date=request.POST['exp_date'], cvc=request.POST['cvc']) 

        return redirect('/checkout')

def checkout(request):
    context={
        "user":User.objects.get(id=request.session['user_id']),
        
        "tickets": Ticket.objects.filter(purchaser=User.objects.get(id=request.session['user_id'])).annotate(total=Sum(F('quantity') * F('price'),  output_field=FloatField())).annotate(tax=ExpressionWrapper(F('quantity') * F('price')*0.0725,  output_field=FloatField())).annotate(total_price=ExpressionWrapper(F('quantity') * F('price') + F('tax'),  output_field=FloatField())),

        "order":Order.objects.all()
    }
    return render(request, 'first_app/checkout.html', context)

def contact(request):
    return render(request, 'first_app/contact.html')
