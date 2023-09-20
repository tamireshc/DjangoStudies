from django.db import models


class Topic(models.Model):
    """Table topic"""

    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Devolve uma representa'ão em string do modelo"""
        return self.text
