from django.shortcuts import render,redirect,get_object_or_404
from Accounts.models import Account 
from .forms import *
from django.contrib import auth
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView  
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.decorators  import login_required
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view 
from django.contrib import messages,auth
from Events.models import *

def register(request):
     if request.method == "POST":
          try:
               form = RegistrationForm(request.POST)
               if form.is_valid():
                         email = form.cleaned_data['email']
                         password = form.cleaned_data['password']
                         username = email.split('@')[0] + '_' + email.split('@')[1].split('.')[0]
                         user = Account.objects.create_user( email=email, username=username, password=password)
                         user.is_active = True
                         user.save()
                        
                         return redirect('login')
          except:
                         return redirect('register')
     else:
          form =  RegistrationForm()
     context = {
          'form':form
     }
     return render(request,'Accounts/register.html',context)


def login(request):
     
     if request.method == "POST":
          
          email = request.POST['email']
          password = request.POST['password']
          print(email,password)
          user = auth.authenticate( email=email, password=password)
          if user is not None:
               auth.login(request,user)
               return redirect('dashboard')
          else:
               return redirect('login')
          
     return render(request,'Accounts/login.html')


@api_view(['POST'])
def register_view(request):
     if request.method == 'POST':
          serializers = RegisterSerializer(data = request.data)
          data = {}
          
          if serializers.is_valid(raise_exception=True):
               user = serializers.save()
               data['response'] = "Registration completed successfully.please login."
               data['username'] = f'{user.username}'
               data['email'] = serializers.data['email']
          else:
               data = serializers.errors
          return Response(data) 
  


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
     # def validate(self,attrs):
    def validate(self, attrs):

     #    username_field = get_user_model().USERNAME_FIELD
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['type'] = 'Bearer'
        data['lifetime'] = str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days) + ' days'
        
        data['user_id'] = self.user.id
        data['user_email'] = self.user.email
        data['user_username'] = self.user.username
        
        return data 
        
 

class MyTokenObtainPairView(TokenObtainPairView):
     serializer_class = MyTokenObtainPairSerializer
     
@login_required(login_url='login')
def dashboard(request):
     userProfile = get_object_or_404(Account,email = request.user)
     events = Event.objects.filter(user= request.user)
     register_events= RegistrationForEvent.objects.filter(user=request.user).order_by('-created_at')
     form = UserForm(instance = userProfile)
     if request.method == "POST":
          form = UserForm(request.POST,instance = userProfile)
          if form.is_valid():
               form.save()
               return redirect('dashboard')
          else:
               return redirect('dashboard')
     context = {
          'form':form,
          'events':events.count,
          'register_events':register_events.count,
     }
     return render(request,'Accounts/dashboard.html',context)

@login_required(login_url = 'login')
def logout(request):
     auth.logout(request)
     return redirect('login')

@login_required(login_url = 'login')
def created_events(request):
     events = Event.objects.filter(user=request.user).order_by('-created_at')
     context= {
          'events':events
     }
     return render(request,'Accounts/created_events.html',context)


@login_required(login_url = 'login')
def registered_events(request):
     registered_events = RegistrationForEvent.objects.filter(user=request.user).order_by('-created_at')
     context= {
          'registered_events':registered_events
     }
     return render(request,'Accounts/registered_events.html',context)



# api
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status,permissions

class UserProfileAPI(APIView):
    serializer_class = UserSerializer
    def get(self, request, pk):
        try:
            profile = Account.objects.get(pk=pk)
            serializer = UserSerializer(profile)
            return Response(serializer.data)
        except:
            return Response("User profile does not exist", status=status.HTTP_404_NOT_FOUND)
    
  