from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request,"login_registration.html")
    elif request.method == "POST":
        if request.POST['myform'] == "1":
            errors = User.objects.registration_validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value, extra_tags=key)
                return redirect('/')
            else:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
                print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'    
                # be sure you set up your database so it can store password hashes this long (60 characters)
                # make sure you put the hashed password in the database, not the one from the form!
                User.objects.create(first_name =request.POST['first_name'], last_name =request.POST['last_name'],email=request.POST['email'],birthday_date=request.POST['birthday_date'],password=pw_hash) 
                return redirect("/") # never render on a post, always redirect! 
        elif request.POST['myform'] == "2":
            errors = User.objects.login_validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    print(key,value)
                    messages.error(request, value, extra_tags=key)
                return redirect('/')
            else:
                # # see if the username provided exists in the database
                # user = User.objects.filter(email=request.POST['login_email']) # why are we using filter here instead of get?
                # if user: # note that we take advantage of truthiness here: an empty list will return false
                #     logged_user = user[0] 
                #     # assuming we only have one user with this username, the user would be first in the list we get back
                #     # of course, we should have some logic to prevent duplicates of usernames when we create users
                #     # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
                #     if bcrypt.checkpw(request.POST['login_password'].encode('utf8'), logged_user.password.encode()):
                #         # if we get True after checking the password, we may put the user id in session
                #         request.session['userid'] = logged_user.id
                #         # never render on a post, always redirect!
                myuser = User.objects.filter(email=request.POST['login_email'])
                print(myuser)
                if myuser: # note that we take advantage of truthiness here: an empty list will return false
                    logged_user = myuser[0] 
                    print(logged_user.id)
                    request.session['username'] =logged_user.first_name
                    request.session['user_id'] = logged_user.id
                    return redirect('/thoughts')
                #if we didn't find anything in the database by searching by username or if the passwords don't match, 
                # redirect back to a safe route
                return redirect("/")

def wallFrontPageFunc(request):
    if 'username' not in request.session:
        return redirect("/")
    context={
        "posts":Post.objects.all()
    }
    return render(request,"thoughts.html",context)

def clearSessionsFunc(request):
    request.session.flush()
    return redirect("/")

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request,"login_registration.html")
    elif request.method == "POST":
        if request.POST['myform'] == "1":
            errors = User.objects.registration_validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value, extra_tags=key)
                return redirect('/')
            else:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
                print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'    
                # be sure you set up your database so it can store password hashes this long (60 characters)
                # make sure you put the hashed password in the database, not the one from the form!
                User.objects.create(first_name =request.POST['first_name'], last_name =request.POST['last_name'],email=request.POST['email'],birthday_date=request.POST['birthday_date'],password=pw_hash) 
                return redirect("/") # never render on a post, always redirect! 
        elif request.POST['myform'] == "2":
            errors = User.objects.login_validate(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    print(key,value)
                    messages.error(request, value, extra_tags=key)
                return redirect('/')
            else:
                # # see if the username provided exists in the database
                # user = User.objects.filter(email=request.POST['login_email']) # why are we using filter here instead of get?
                # if user: # note that we take advantage of truthiness here: an empty list will return false
                #     logged_user = user[0] 
                #     # assuming we only have one user with this username, the user would be first in the list we get back
                #     # of course, we should have some logic to prevent duplicates of usernames when we create users
                #     # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
                #     if bcrypt.checkpw(request.POST['login_password'].encode('utf8'), logged_user.password.encode()):
                #         # if we get True after checking the password, we may put the user id in session
                #         request.session['userid'] = logged_user.id
                #         # never render on a post, always redirect!
                myuser = User.objects.filter(email=request.POST['login_email'])
                print(myuser)
                if myuser: # note that we take advantage of truthiness here: an empty list will return false
                    logged_user = myuser[0] 
                    print(logged_user.id)
                    request.session['username'] =logged_user.first_name+' '+logged_user.last_name
                    request.session['user_id'] = logged_user.id
                    return redirect('/thoughts')
                #if we didn't find anything in the database by searching by username or if the passwords don't match, 
                # redirect back to a safe route
                return redirect("/")

def wallFrontPageFunc(request):
    if 'username' not in request.session:
        return redirect("/")
    context={
        "posts":Post.objects.all().order_by("-likecount") 
    }
    return render(request,"thoughts.html",context)

def clearSessionsFunc(request):
    request.session.flush()
    return redirect("/")

def addPostFunc(request):
    if(request.method == "POST"):
        errors = Post.objects.postvalidate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                print(key,value)
                messages.error(request, value, extra_tags=key)
                return redirect('/thoughts')
        else:
            userobj = User.objects.get(id=request.session['user_id'])
            Post.objects.create(message=request.POST['Postmessage'],likecount = 0,user=userobj)
            return redirect("/thoughts")

def PostLikeFunc(request,my_post_id):
    if(request.method == "POST"):
        userobj = User.objects.get(id =request.session['user_id'])
        postobj = Post.objects.get(id = my_post_id)
        flag = False
        userobj_likes = userobj.user_likes.all()
        for i in userobj_likes:
            if i.post ==postobj:
                flag = True
        if flag == False:
            Like.objects.create(user=userobj,post=postobj)
            postobj.likecount = postobj.likecount + 1
            postobj.save()
            return redirect("/thoughts/"+str(my_post_id))
    else:
        return redirect("/thoughts/"+str(my_post_id))

def PostUnLikeFunc(request,my_post_id):
    if(request.method == "POST"):
        userobj = User.objects.get(id =request.session['user_id'])
        postobj = Post.objects.get(id = my_post_id)
        userobj_likes = userobj.user_likes.all()
        postobj.likecount = postobj.likecount - 1
        postobj.save()
        lobj=Like.objects.get(user = userobj,post=postobj)
        lobj.delete()
        return redirect("/thoughts/"+str(my_post_id))
    else:
        return redirect("/thoughts/"+str(my_post_id))

def DeletePostFunc(request,my_post_id):
        postobj = Post.objects.get(id = my_post_id)
        postobj.delete()
        return redirect("/thoughts")

def ViewUserPostsFunc(request,my_post_id):
    userobj = User.objects.get(id =request.session['user_id'])
    postobj = Post.objects.get(id=my_post_id)
    flag = "False"
    userobj_likes = userobj.user_likes.all()
    for i in userobj_likes:
        if i.post ==postobj:
                flag = "True"
    context={
        "post":postobj,
        "likeflag":flag,
    }
    return render(request,"tboard.html",context)



