from django.db import models


class Spreadsheet(models.Model):
    name = models.TextField(max_length=300)
    url = models.TextField()
    iat = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    date = models.DateField(null=True)

    def __str__(self):
        aux = 'ok' if self.processed else 'pendente'
        return f'{self.name} - {aux}'


class Schedule(models.Model):
    name = models.CharField(max_length=300)
    birth_date = models.DateField()
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.DO_NOTHING)
    spreadsheet_page = models.IntegerField(null=True)
    spreadsheet_line = models.IntegerField(null=True)
    place = models.CharField(max_length=300)
    date = models.DateTimeField()
    dose = models.IntegerField()
    iat = models.DateTimeField(auto_now_add=True)


class EmailNotification(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    second_dose_sent = models.BooleanField(null=True, default=False)
    sent_at = models.DateTimeField(null=True)
    iat = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'email']
