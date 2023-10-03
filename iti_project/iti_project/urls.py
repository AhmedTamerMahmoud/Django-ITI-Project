
from django.contrib import admin
from django.urls import path
from myapp.views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',home, name='home'),
    
    path('signup',signup,name='signup'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),

    path('addBook', addBook, name='addBook'),
    path('allBooks', allBooks, name='allBooks'),
    path('updateBook/<int:ID>', updateBook, name='updateBook'),
    path('deleteBook/<int:ID>', deleteBook, name='deleteBook'),
    path('borrowBook/<int:bookID>', borrowBook, name='borrowBook'),

    path('studentBook',studentBook,name='studentBook'),
    path('studentProfile', studentProfile,name='studentProfile'),
    path('returnback/<int:bookID>',returnback,name='returnback'),


    path('list_users',list_users, name='list_users'),
    path('studentDetails/<int:ID>', studentDetails, name='studentDetails'),
    path('changePass', changePass, name="changePass")
]
