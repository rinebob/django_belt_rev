from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
# from django.contrib.messages import get_messages
from .models import *
import bcrypt

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    # context = {

    # }
    return render(request,'rev_belt/index.html')

def register(request):

    if request.method == "POST":
        # print(User.objects.all().values())

        errors = User.objects.reg_validator(request.POST)
        print("errors = ",errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            print("password hash = ",password_hash)
            User.objects.create(alias=request.POST['alias'],name = request.POST['name'],email = request.POST['email'],password_hash = password_hash)
            x = User.objects.get(email = request.POST['email'])
            request.session['id'] = x.id
            request.session['alias'] = x.alias
            print("query set = ",User.objects.all().values())
            print("THE END")
            return redirect('/welcome')
            
    else:
        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/')

def login(request):
   
    if request.method == "POST":
        
        login_errors = User.objects.login_validator(request.POST)
        print("login_errors = ",login_errors)
        if len(login_errors):
            for key, value in login_errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        else:
            x = User.objects.get(email=request.POST['log_eml'])
            request.session['id'] = x.id
            request.session['alias'] = x.alias
            print("request.session['id'] = ",request.session['id'])
            print("request.session['alias'] = ",request.session['alias'])
            print("THE END")
            return redirect('/welcome')
    else:

        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/')

def welcome(request):
    print("r.s[id] = ",request.session['id'])
        
    context = {
        "reviews" : Review.objects.order_by('-created_at')[:3],
        "reviewed_books" : Book.objects.filter(book_review__book_id__gt=0).distinct()
    }

    return render(request, "rev_belt/welcome.html",context)
    


def book(request,id):

    context = {
        "book" : Book.objects.get(id=id),
        "reviews" : Review.objects.filter(book_id=id).order_by('-created_at')
    }
    
    return render(request, "rev_belt/book.html",context)

def books(request):

    context = {
        "book" : Book.objects.get(id=1),
        "books" : Book.objects.all(),
        "reviews" : Review.objects.filter(book_id=1)
        
    }
    return render(request, "rev_belt/book.html",context)

def addbook(request):

    return render(request, "rev_belt/addbook.html")

def addreview(request,id):
    context = {
        "book" : Book.objects.get(id=id),
    }
    
    Review.objects.create(book_id=Book.objects.get(id=id),user_id = User.objects.get(id=request.session['id']),text = request.POST['review_text'],rating = request.POST['rating'])

    book_id = context['book'].id
    return redirect("/book/"+str(book_id))
    
def user(request):
    context = {
        "user" : User.objects.get(id=request.session['id']),
        "reviews" : Review.objects.filter(user_id=request.session['id']).order_by('-created_at')
    }
    print("context['user'].id = ",context['user'].id)
    print("context['user'].alias = ",context['user'].alias)
    print("context['reviews'].count() = ",context['reviews'].count())

    num_revs = Review.objects.filter(user_id=request.session['id']).count()

    print("review count =",num_revs)

    return render(request, "rev_belt/user.html",context)

def logout(request):

    request.session.clear()

    return redirect('/')

    # context = {
    #         "user" : User.objects.get(id=request.session['id'])
    #     }
    # print("context  = 'user' : User.objects.get(id=request.session['id'])")
    # print("user = ",user)
    # # print("context['user'].values() = ",context['user'].all().values())
    # print("context['user'].alias = ",context['user'].alias)
    # print("context['user'].name = ",context['user'].name)

    # people = {
    #     "users" : User.objects.all()
    # }
    # print("users  = 'users' : User.objects.all()")
    # # print("users = ",users)
    # print("people['users'].values() = ",people['users'].all().values())
    # print("people['users'][0].alias = ",people['users'][0].alias)
    # print("people['users'][0].name = ",people['users'][0].name)

    # for key, value in people.items():
    #     print("key = ",key," value = ",value)

  