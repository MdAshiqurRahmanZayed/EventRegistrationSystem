from django.shortcuts import render
from Accounts.models import *
from Events.models import *
from rest_framework.generics import *
from .serializers import *
from rest_framework import status,permissions,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes


class EventListCreateAPIView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

     
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = EventCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=request.user)
        
        event = EventModelSerializer(instance)
        headers = self.get_success_headers(serializer.data)          
        return Response(event.data, status=status.HTTP_201_CREATED, headers=headers)
    

class EventRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EventModelSerializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(instance.user)
        if instance.user != request.user:
             return Response({'message':'you are not allow to edit.'})
        serializer = EventCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        instance = serializer.save()
        post_serializer = EventModelSerializer(instance)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(post_serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
             return Response({'message':'you are not allow to destroy.'})
        self.perform_destroy(instance)
        return Response({'message':'Event deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
   
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def registration_or_unregistration_for_events(request, pk):
    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
    user = request.user

    if RegistrationForEvent.objects.filter(user=user, event=event).exists():
        RegistrationForEvent.objects.filter(user=user, event=event).delete()
        event.slots_available += 1
        event.save()
        return Response({'detail': 'Unregistered successfully.'}, status=status.HTTP_200_OK)

    else:
        if event.slots_available > 0:
            RegistrationForEvent.objects.create(user=user, event=event)
            event.slots_available -= 1
            event.save()
            return Response({'detail': 'Registered successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Sorry, no available slots.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def created_events(request):
     events = Event.objects.filter(user=request.user).order_by('-created_at')
     serializer = EventModelSerializer(events,many=True)
     response_data = {
            'created_events_count': events.count(),
            'created_events': serializer.data,
        }
     return Response(response_data, status=status.HTTP_200_OK)

class RegisteredEventsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        registered_events = RegistrationForEvent.objects.filter(user=request.user).order_by('-created_at')
        registered_events_count = registered_events.count()
        serializer = RegistrationForEventSerializer(registered_events, many=True)
        
        response_data = {
            'registered_events_count': registered_events_count,
            'registered_events': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class CreatedEventsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        registered_events = RegistrationForEvent.objects.filter(user=request.user).order_by('-created_at')
        registered_events_count = registered_events.count()
        serializer = RegistrationForEventSerializer(registered_events, many=True)
        
        response_data = {
            'registered_events_count': registered_events_count,
            'registered_events': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


# all CRUD operation
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Adjust permissions as needed

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return EventCreateSerializer
        return EventModelSerializer