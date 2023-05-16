"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game
from rest_framework.decorators import action
from django.db.models import Count


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event 

        Returns:
            Response -- JSON serialized event 
        """
        try: 
            event = Event.objects.annotate(attendee_count=Count('attendees')).get(pk=pk)
            serializer = eventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex: 
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all event 

        Returns:
            Response -- JSON serialized list of event 
        """
        events = Event.objects.annotate(attendee_count=Count('attendees'))

        gamer = Gamer.objects.get(user=request.auth.user)

        if "game" in request.query_params:
            events = events.filter(game = request.query_params["game"])

        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()

        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request): 
        """Handle POST operations 
        Returns 
            Response -- JSON serialized event instance
        """

        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game'])

        event = Event.objects.create(
            description = request.data['description'], 
            date = request.data['date'], 
            organizer = organizer, 
            game = game, 
        )
        event.attendees.set([request.auth.user.id])
        serializer = eventSerializer(event)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
        Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]

        event_game = Game.objects.get(pk=request.data['game'])
        event.game = event_game

        event_organizer = Gamer.objects.get(user=request.auth.user)
        event.organizer = event_organizer

        event.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk): 

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    



class eventSerializer(serializers.ModelSerializer):
    attendee_count = serializers.IntegerField(default=None)
    """JSON serializer for event 
    """
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'game', 'organizer', 'attendees', 'joined', 'attendee_count')
        depth = 1