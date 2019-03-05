from django.shortcuts import render, redirect
from apps.app_reads.models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else :
        r_user = User.objects.create(first_name = request.POST['fname'], \
            last_name = request.POST['lname'], email = request.POST['email'], \
            password = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt())) 
        request.session['name'] = r_user.first_name
        request.session['id'] = r_user.id
        request.session['registered'] = True
    return redirect('/books')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors) > 0:
        for tag, error in login_errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        l_user = User.objects.get(email=request.POST['email'])
        request.session['name'] = l_user.first_name
        request.session['id'] = l_user.id
        request.session['logged_in'] = True  
    return redirect('/books')

def home(request):
    if 'id' in request.session:
        context = {
            "books": Book.objects.all(),
            "reviews": Review.objects.all(),
        }
        return render(request, "home.html", context)
    else:
        return redirect('/')

def add_book(request):
    context = {
        "books": Book.objects.all(),
        "authors": Author.objects.all(),
    }
    return render(request, "add_book.html", context)

def create_book(request):
    errors = Book.objects.book_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
    else:
        if request.POST['author1'] == '--select--':
            new_author = Author.objects.create(name=request.POST['author2'])
        else:
           new_author = Author.objects.create(name=request.POST['author1'])
        new_book = Book.objects.create(title=request.POST['title'], \
            author_id = new_author)
        Review.objects.create(review=request.POST['review'],\
            user_id = User.objects.get(id=request.session['id']),
            book_id = new_book, rating=request.POST['rating'])
        return redirect('/books')

def bookInfo(request, id):
    context = {
        "book": Book.objects.get(id=id),
        "reviews": Review.objects.all(),
    }
    return render(request, "review.html", context)

def userInfo(request, id):
    context = {
        "user": User.objects.get(id=id),
    }
    return render(request, "user.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')