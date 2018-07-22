from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
# from django.contrib.messages import get_messages
from .models import *
import bcrypt

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    # context = {

    # }
    return render(request,'reg_login/index.html')

def register(request):

    if request.method == "POST":
        # print(User.objects.all().values())

        # print("==================== FIRST NAME ==================================== Validating name: ", request.POST['first_name'])
        # if len(request.POST['first_name']) < 2:
        #     print("First Name must be 2+ characters")
        #     messages.error(request,"First Name must be 2+ characters",extra_tags="first_name")
        #     # return redirect('/')
        # elif request.POST['first_name'].isalpha() == False:
        #     print("First Name can only contain letters")
        #     messages.error(request,"First Name can only contain letters",extra_tags="first_name")
        #     # return redirect('/')
        # else:
        #     request.session['first_name'] = request.POST['first_name']
        #     print("pass")
        
        # print("==================== LAST NAME ==================================== Validating name: ", request.POST['last_name'])
        # if len(request.POST['last_name']) < 2:
        #     print("Last Name must be 2+ characters")
        #     messages.error(request,"Last Name must be 2+ characters",extra_tags="last_name")
        #     # return redirect('/')
        # elif request.POST['last_name'].isalpha() == False:
        #     print("Last Name can only contain letters")
        #     messages.error(request,"Last Name can only contain letters",extra_tags="last_name")
        #     # return redirect('/')
        # else:
        #     request.session['last_name'] = request.POST['last_name']
        #     print("pass")

        # print("====================== EMAIL ======================================== Validating email: ", request.POST['email'])
        # if len(request.POST['email']) < 1:
        #     print("Email cannot be blank!")
        #     messages.error(request,"Email cannot be blank!",extra_tags="email")
        #     # return redirect('/')
        # elif not EMAIL_REGEX.match(request.POST['email']):
        #     print("Invalid email address!")
        #     messages.error(request,"Invalid email address!",extra_tags="email")
        #     # return redirect('/')
        # else:
        #     request.session['email'] = request.POST['email']

        #     dupe_check = User.objects.filter(email=request.POST['email'])
        #     if len(dupe_check):
        #         messages.error(request,"Email exists in database!  Please try again!",extra_tags="email")
        #         # return redirect('/')
        #     else:
        #         request.session['email'] = request.POST['email']
        #         print("pass")

        # print("====================== PASSWORD ====================================== Validating password: ", request.POST['password'])
        # if len(request.POST['password']) < 8:
        #     print("Password must be 8+ characters.")
        #     messages.error(request,"Password must be 8+ characters.",extra_tags="pw")
        #     return redirect('/')
        # else:
        #     print("pass")
            
        #     # return redirect('/show')
        #     # return redirect('/')
            
        # print("====================== CONFIRM PASSWORD ================================ Validating password: ", request.POST['conf_password'])
        # if len(request.POST['conf_password']) > 0:
        #     if request.POST['password'] == request.POST['conf_password']:
        #         print("Passwords match! ")
        #         print("pass")
                
        #     else:
        #         print("submitted passwords don't match")
        #         messages.error(request,"Passwords don't match!",extra_tags="conf_password")
        #         return redirect('/')
        # else:
        #     print("Confirm password blank")
        #     messages.error(request,"Confirm password blank",extra_tags="conf_password")
        #     return redirect('/')

   
        # print("messges.error = ",messages.error)
        # if (messages.error):
            
        #     print("messges.error = ",messages.error)
        #     print("errors so redirect same page")
        #     return redirect('/')

        errors = User.objects.reg_validator(request.POST)
        print("errors = ",errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            print("password hash = ",password_hash)
            User.objects.create(first_name=request.POST['first_name'],last_name = request.POST['last_name'],email = request.POST['email'],password_hash = password_hash)
            print("query set = ",User.objects.all().values())
            print("THE END")
            return redirect('/show')
            
    else:
        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/')


def rest(request):
    
        context = {
            "users" : User.objects.all()
        }
        return render(request,"reg_login/rest_index.html",context)

def destroy(request,userid):
    u = User.objects.get(id=userid)
    u.delete()
    return redirect('/')


def login(request):
   
    if request.method == "POST":
        
        # if len(request.POST['log_eml']) < 1:
        #     print("Email cannot be blank!")
        #     messages.error(request,"We are unable to log you in.  Please try again.",extra_tags="log_eml")
        #     return redirect('/')
        # elif not EMAIL_REGEX.match(request.POST['log_eml']):
        #     print("Invalid log_eml address!")
        #     messages.error(request,"We are unable to log you in.  Please try again.",extra_tags="log_eml")
        #     return redirect('/')
        # else:
        #     dupe_check = User.objects.filter(email=request.POST['log_eml'])
        #     if len(dupe_check) <1 :
        #         print("dupe_check fail")
        #         messages.error(request,"We are unable to log you in.  Please try again.",extra_tags="log_eml")
        #         return redirect('/')
            

        # print("====================== CONFIRM PASSWORD =============== Validating password: ", request.POST['conf_pw'])
        # if len(request.POST['conf_pw']) > 0:
        #     print("in confirm")
            
        #     compare = bcrypt.checkpw(request.POST['conf_pw'].encode(), dupe_check[0].password_hash.encode())
        #     print("compare result = ",compare)
        #     if not compare:
        #         print("compare result fail")
        #         messages.error(request,"We are unable to log you in.  Please try again.",extra_tags="pw_conf")
        #         return redirect('/')
        #     else:
        #         return redirect('/show')
            
        # else:
        #     messages.error(request,"We are unable to log you in.  Please try again.",extra_tags="pw_conf")
        #     print("Confirm password can't be blank")
        #     return redirect('/')

        login_errors = User.objects.login_validator(request.POST)
        print("login_errors = ",login_errors)
        if len(login_errors):
            for key, value in login_errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        else:
            print("THE END")
            return redirect('/show')


    else:

        print("This was supposed to be a post but you're in the else statement...  why???")
        return redirect('/')

def show(request):

    return render(request, "reg_login/success.html")


