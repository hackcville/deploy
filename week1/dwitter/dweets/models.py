from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Dweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.message} - {self.user} - {str(self.date)}"
