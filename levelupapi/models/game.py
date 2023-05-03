from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=75)
    num_of_players = models.CharField(max_length=15)
    skill_level = models.CharField(max_length=50)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name="Games")
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="OwnedGames")


