"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event 

        Returns:
            Response -- JSON serialized event 
        """
        event = Event.objects.get(pk=pk)
        serializer = eventSerializer(event)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all event 

        Returns:
            Response -- JSON serialized list of event 
        """
        events = events = Event.objects.all()
        if "game" in request.query_params:
            events = events.filter(game = request.query_params["game"])

        print(events)

        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)


class eventSerializer(serializers.ModelSerializer):
    """JSON serializer for event 
    """
    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'game', 'organizer', 'attendees')