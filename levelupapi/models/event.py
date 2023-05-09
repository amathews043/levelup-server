from django.db import models
from .gamer import Gamer

class Event(models.Model):
    description = models.CharField(max_length=250)
    date = models.DateTimeField()
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="EventsPlayed")
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name="EventsHosted")
    attendees = models.ManyToManyField(Gamer, related_name="events")

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value

