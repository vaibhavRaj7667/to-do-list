from django.shortcuts import render,redirect
from .forms import Task_form
from .models import Todo
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User


def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect('home')


def create_user(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,"user alredy in DB")
            elif User.objects.filter(email=email).exists():
                messages.error(request,"email alredy in DB")
            else:
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                messages.success(request,"user created succesfully")
                return redirect('home')
            
        else:
             messages.error(request, 'Passwords do not match.')

    return render(request,'create_user.html')


def home(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('create_task')
        else:
            messages.warning(request, "invalid data")
            return redirect('home')
    else:
        return render(request,'login_page.html')


@login_required
def create_task(request):
    all_data = Todo.objects.filter(user=request.user)
    if request.method=='POST':
        form = Task_form(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  
            task.user = request.user        
            task.save()  
            return redirect('create_task')
    else:
        form=Task_form()


    return render(request,'home_page.html',{'form':form,'all_data':all_data})



def delete_task(request,task_id):
    task = get_object_or_404(Todo, id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('create_task')  