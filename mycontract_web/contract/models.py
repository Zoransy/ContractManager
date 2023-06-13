from django.db import models

# Create your models here.

# this class is user table
class User(models.Model):
    # user'name less than 40
    # can't be null
    name = models.CharField(max_length=40, blank=False, null=False) 

    # password less than 20 
    # can't be null
    password = models.CharField(max_length=20, blank=False, null=False) 

    # eamil is used to send the information that counter ...
    email = models.CharField(max_length=50, null=True)
    # operator is 1 and administrator is 2
    # could be 0 when it is 0, it is the new one
    roleID = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class Authority(models.Model):
    # the right name 1 is admin, 2 is the manager, 3 is draft, 4 is counter, 5 is approve, 6 is sign
    
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

class HaveAuthority(models.Model):
    # reference the User table's id
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.PROTECT)

    # reference the Authority table's id
    right = models.ForeignKey(to='Authority', to_field='id', on_delete=models.PROTECT)

class Customer(models.Model):
    # the customer's name 
    # can't be null
    name = models.CharField(max_length=10, blank=False, null=False)

    # the customer's address
    # address can be null
    address = models.CharField(max_length=100)

    # the customer's telephone the length must be fixed 
    telephone = models.CharField(max_length=11)
    
    # postcode 
    postcode = models.CharField(max_length=10)

    # bank 
    bank = models.CharField(max_length=50)

    # bank account
    account = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Contract(models.Model):
    # contract name 
    name = models.CharField(max_length=50)

    # the contract' start time
    start_time = models.DateTimeField()

    # the contract' end time
    end_time = models.DateTimeField()

    # the contract' content 
    content = models.TextField()

    # customer foreign key mean that the person sign the contract 
    customer = models.ForeignKey(to='Customer', to_field='id', on_delete=models.PROTECT) 

    # fileName
    file = models.ForeignKey(to='File', to_field='id', on_delete=models.PROTECT)

    # distribute == 0 mean that the contract is not distributed
    distribute = models.IntegerField(default=0)

    # state 0 is the not countersign, 1 is not dinggao, 2 is not approve , 3 is not sign, 4 is meaning that the contract is finished
    state = models.IntegerField(default=0)

    # the contract is drafted by the user
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name


class File(models.Model):
    # the file name is not repeatable
    fileName = models.CharField(max_length=50, blank=False, null=False)

    content = models.TextField()

class CounterSign(models.Model):
    # foreign key User table id
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.PROTECT)

    # foreign key contract table id
    contract = models.ForeignKey(to='Contract', to_field='id', on_delete=models.PROTECT)

    content = models.TextField(null=True)

class Approve(models.Model):
    # foreign key User table id
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.PROTECT)

    # foreign key contract table id
    contract = models.ForeignKey(to='Contract', to_field='id', on_delete=models.PROTECT)

    content = models.TextField(null=True)

    # refuse or accept, 0 is refuse, 1 is accept
    judge = models.IntegerField(default=0)

class Sign(models.Model):
    # foreign key User table id
    user = models.ForeignKey(to='User', to_field='id', on_delete=models.PROTECT)

    # foreign key contract table id
    contract = models.ForeignKey(to='Contract', to_field='id', on_delete=models.PROTECT)

    content = models.TextField(null=True)


# first insert into user values('admin', '123456', 0)

# User.objects.create(name='admin', password='123456', roleID=2)