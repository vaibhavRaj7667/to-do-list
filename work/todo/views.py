from django.shortcuts import render,redirect
from .forms import Task_form
from .models import Todo
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


def create_user(request):
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
    all_data = Todo.objects.all()
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