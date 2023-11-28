from django.shortcuts import render,redirect,get_object_or_404
from .forms import eventForm
from django.contrib.auth.decorators import login_required
from .models import Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages,auth


def home(request):
     events = Event.objects.all().order_by('-created_at')[:6]
     context = {
          'events':events
     }
     return render(request,'Events/home.html',context)


@login_required(login_url='login')
def createEvent(request):
     if request.method == 'POST':
          # print(request.POST)
          form = eventForm(request.POST)
          try:
               if form.is_valid():
                    form = form.save(commit=False)
                    form.user = request.user
                    form.save()
                    messages.success(request,"Created Event successfully.")
                    return redirect('event_detail',form.id)
                    
          except:
               messages.warning(request,"Does not Created Event.")
               return redirect('createEvent')
     
     event_form = eventForm()
     context= {
          'form':event_form
     }
     return render(request,'Events/event_form.html',context)

def event_list(request):
    event_list = Event.objects.all().order_by('-created_at')
    paginator = Paginator(event_list, 3)  

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'Events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {
         'event':event
    }
    return render(request, 'Events/event_detail.html',context)


@login_required(login_url='login')
def update_event(request, pk):
     event = get_object_or_404(Event, id=pk)
     form = eventForm(instance=event)
     if event.user != request.user:
               return redirect('home')
     if request.method == 'POST':
          form = eventForm(request.POST, instance=event)
          if form.is_valid():
               form.save()
               messages.success(request,"Updated Event successfully.")
               return redirect('event_detail',pk)
          else:
               messages.success(request,"Does not Updated Event successfully.")
               return redirect('event_detail',pk)
     context = {
          'form':form
     }
     return render(request, 'Events/event_form.html',context)


@login_required(login_url='login')
def delete_event(request, pk):
     event = get_object_or_404(Event, id=pk)
     event.delete()
     messages.warning(request,"Event deleted successfully.")
     return redirect('dashboard')
     