from django.db import models

# Create your models here.
class AccountDetail(models.Model):
    date = models.DateField()
    name = models.CharField(max_length = 120, null = True, blank = True)
    typeA = models.CharField(max_length = 120, null = True, blank = True)
    debit = models.PositiveIntegerField(default = 0, null = True, blank = True)
    credit = models.PositiveIntegerField(default = 0, null = True, blank = True)
    balance = models.PositiveIntegerField(default = 0, null = True, blank = True)
    desc = models.TextField()    
    
    
    def __str__(self):
        return self.name
    
class AccountDetailEnding(models.Model):
    date = models.DateField()
    name = models.CharField(max_length = 120, null = True, blank = True)
    typeA = models.CharField(max_length = 120, null = True, blank = True)
    debit = models.PositiveIntegerField(default = 00000, null = True, blank = True)
    credit = models.PositiveIntegerField(default = 00000, null = True, blank = True)
    balance = models.PositiveIntegerField(default = 00000, null = True, blank = True)
    desc = models.TextField() 
    transmade = models.IntegerField(default = 00000)
    
    def __str__(self):
        return self.name
    
    