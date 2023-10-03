from django.shortcuts import render
from .models import *
from django.http import *
from .form import *
from django.http import *

# Create your views here.


def home(req):
    context = {}
    context['title'] = "Home"
    return render(req, 'index.html', context)


def login(req):
    context = {}
    context['title'] = "Login"
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = User.objects.filter(username=username, password=password)
        if len(user):
            req.session['id'] = user[0].id
            req.session['username'] = user[0].username
            req.session['password'] = user[0].password
            req.session['is_admin'] = user[0].is_admin
            return render(req, 'index.html')
        else:
            context = {'msg': "Invalid Username or Password.", "color": "red"}
            return render(req, 'login.html', context)
    return render(req, 'login.html')  # GET


def logout(req):
    req.session.clear()
    req.session.flush()
    context = {'msg': "Logged out Successfully.", 'color': 'green'}
    context['title'] = "Logout"

    return render(req, 'login.html', context)


def signup(req):
    context = {}
    context['title'] = "Sign Up"
    if(req.method == 'POST'):
        User.objects.create(
            username=req.POST['username'], password=req.POST['password'])
        context = {'msg': "Signed Up Successfully, Please Log In.",
                   "color": "green"}
        return render(req, 'login.html', context)
    return render(req, 'signup.html')


def list_users(req):
    context = {}
    context['title'] = "List Users"
    if req.method == 'POST':
        users = User.objects.filter(id=req.POST['id'])
        context['users'] = users
    else:
        users = User.objects.all()
        context['users'] = users
    return render(req, 'listusers.html', context)


def studentDetails(req, ID):
    context = {}
    context['title'] = "Student Details"
    user = User.objects.filter(id=ID, is_admin=False)[0]
    form = UserForm(instance=user)
    context = {}
    context['form'] = form
    return render(req, 'studentDetails.html', context)


def changePass(req):
    context = {}
    context['title'] = "Change Own Password"
    user = User.objects.filter(id=req.session['id'])[0]
    if req.method == 'POST':
        currPass = req.POST['currPass']
        newPass = req.POST['password']
        newPass2 = req.POST['newPass2']
        if req.session['password'] == currPass and newPass == newPass2:
            obj = ChangePassForm(instance=user, data=req.POST)
            if obj.is_valid():
                obj.save()
                context = {"msg": "Changed Successfully.",
                           "color": "green", "form": obj}
                req.session['password'] = newPass2
                return render(req, 'changePass.html', context)
            else:
                context = {"msg": "Invalid Password.",
                           "color": "red", "form": obj}
                return render(req, 'changePass.html', context)
        else:
            context = {"msg": "Invalid Passwords.",
                       "color": "red", "form": ChangePassForm()}
            return render(req, 'changePass.html', context)

    else:
        form = ChangePassForm()
        context = {"form": form}
        return render(req, 'changePass.html', context)


def addBook(req):
    context = {'operation': "Add"}
    context['title'] = "Add Book"
    form = BookForm()
    context['form'] = form
    if req.method == 'POST':
        book = BookForm(req.POST)
        if book.is_valid():
            book.save()
            context['msg'] = "Added Successfully"
            context['color'] = 'green'
            return render(req, 'book.html', context)
        else:
            context['msg'] = "Invalid Input"
            context['color'] = 'red'
            return render(req, 'book.html', context)

    else:
        return render(req, 'book.html', context)


def allBooks(req):
    books = Book.objects.all()
    booksAndBorrowers = []
    for b in books:
        obj = {'id': b.id, 'name': b.name, 'description': b.description,
               "is_borrowed": b.is_borrowed, "photoName": b.photoName}
        if b.is_borrowed:
            obj['borrowed_by_id'] = b.borrowed_by_id.id
            obj['borrowerName'] = b.borrowed_by_id.username
        booksAndBorrowers.append(obj)

    context = {'books': booksAndBorrowers}
    context['title'] = "All Books"
    return render(req, 'allBooks.html', context)


def updateBook(req, ID):
    context = {}
    context['title'] = "Update Book"
    book = Book.objects.filter(id=ID)[0]
    form = BookForm(instance=book)
    context = {'form': form, 'operation': "Update"}
    if req.method == 'POST':
        bookForm = BookForm(data=req.POST, instance=book)
        if bookForm.is_valid():
            bookForm.save()
            context['msg'] = "Updated Successfully."
            context['color'] = "green"
            book = Book.objects.filter(id=ID)[0]
            form = BookForm(instance=book)
            context['form'] = form
            context['operation'] = "Update"
            return render(req, 'book.html', context)
        else:
            context = {'msg': "Invalid Input.", 'color': "red"}
            return render(req, 'book.html', context)

    return render(req, 'book.html', context)


def deleteBook(req, ID):
    context = {}
    context['title'] = "Delete Book"
    Book.objects.get(id=ID).delete()
    context = {}
    context['msg'] = "Deleted Successfully"
    context['color'] = "green"
    books = Book.objects.all()
    context['books'] = books
    return render(req, 'allBooks.html', context)


def borrowBook(req, bookID):
    context = {}
    context['title'] = "Borrow Book"
    if req.session['username']:
        book = Book.objects.filter(id=bookID)[0]
        context = {}
        if req.method == 'GET':
            form = BorrowBookForm(instance=book)
            context['form'] = form
            return render(req, 'borrowBook.html', context)
        elif req.method == 'POST':
            form = BorrowBookForm(instance=book, data=req.POST)
            if form.is_valid():
                form.save()
                Book.objects.filter(id=bookID).update(
                    is_borrowed=True, borrowed_by_id=req.session['id'])
                context['msg'] = "Borrowed Successfully"
                context['color'] = "green"
                return render(req, 'borrowBook.html', context)
            else:
                context['msg'] = "Invalid Data"
                context['color'] = "red"
                context['form'] = BorrowBookForm(instance=book)
                return render(req, 'borrowBook.html', context)
        return HttpResponseNotAllowed()
    # else:
    #     context['msg'] = "You Must Be Logged In to Borrow A Book."
    #     context['color'] = "red"
    #     context['form'] = BorrowBookForm()
    #     return render(req, 'borrowBook.html', context)


def studentBook(req):
    context = {}
    context['title'] = "Student Books"
    books = Book.objects.filter(borrowed_by_id=req.session['id'])
    context = {}
    context['books'] = books
    return render(req, 'viewbooks.html', context)


def returnback(req, bookID):
    context = {}
    context['title'] = "Return to Shelf"
    Book.objects.filter(id=bookID).update(
        borrowed_by_id=None, returnTime=None, is_borrowed=False)
    book = Book.objects.filter(borrowed_by_id=req.session['id'])
    context = {}
    context['book'] = book
    context['msg'] = "Returned to Shelf"
    context['color'] = "green"
    return render(req, 'viewbooks.html', context)


def studentProfile(req):
    user = User.objects.filter(id = req.session['id'])[0]
    form = StudentProfileForm(instance=user)
    context = {'form': form}
    if req.method == 'POST':
        form = StudentProfileForm(instance=user, data=req.POST)
        if form.is_valid():
            form.save()
            context['form'] = form
            context['msg'] = "Updated Successfully."
            context['color'] = "green"
            return render(req, 'studentProfile.html', context)
        else:
            context['form'] = form
            context['msg'] = "Invalid Data."
            context['color'] = "red"
            return render(req, 'studentProfile.html', context)
    elif req.method == 'GET':
        return render(req, 'studentProfile.html', context)
