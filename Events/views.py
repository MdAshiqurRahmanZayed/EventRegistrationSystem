from django.shortcuts import render,redirect,get_object_or_404
from .forms import eventForm
from django.contrib.auth.decorators import login_required
from .models import Event,RegistrationForEvent
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages,auth
from django.db.models import Q

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
    try:
          registration_check = RegistrationForEvent.objects.filter(user=request.user,event=event).exists()    
    except:
         registration_check = False
    context = {
         'event':event,
         'registration_check':registration_check,
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
     
@login_required(login_url='login')
def registrationOrUnregistrationForEvents(request,pk):
     event = Event.objects.get(id = pk)
     if RegistrationForEvent.objects.filter(user=request.user,event=event).exists():
          RegistrationForEvent.objects.filter(user=request.user,event=event).delete()
          messages.warning(request,"Unregistered successfully.")
          event.slots_available +=1
          event.save()
          return redirect('event_detail',pk)
          
     else:
          if event.slots_available>0:
               RegistrationForEvent.objects.create(user=request.user,event=event)
               messages.success(request,"Registered successfully.")
               event.slots_available -=1
               event.save()
          else:
               messages.warning(request,"Sorry no availabel slot.")
               return redirect('event_detail',pk)
     return redirect('event_detail',pk)
     
     
def searchEvent(request):
    if 'keyword' in request.GET:
          keyword = request.GET['keyword']

    if keyword:
               events = Event.objects.order_by('-created_at').filter(Q(title__icontains=keyword) |
                                                                   Q(description__icontains=keyword) |
                                                                   Q(location__icontains=keyword))
               event_count = events.count()
               paginator = Paginator(events, 3)  

               page = request.GET.get('page')
               try:
                    events = paginator.page(page)
               except PageNotAnInteger:
                    events = paginator.page(1)
               except EmptyPage:
                    events = paginator.page(paginator.num_pages)
    context = {
          "events": events,
          "event_count": event_count,
          "keyword": keyword,
     }
    return render(request, "Events/event_list.html",context)

