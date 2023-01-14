from django.db import models
from datetime import date

# Create your models here.
class use(models.Model):       
    username = models.CharField(max_length=10, default='')
    school = models.CharField(max_length=150,null=True)
    date = models.DateField(default=date.today())
    full_sch = models.CharField(max_length=30, default='0')
    contact_details = models.CharField(max_length=10, default='0')
    def __str__(self):
        return self.username


class sch_reg(models.Model):       
    username = models.CharField(max_length=10, default='')
    school = models.CharField(max_length=150,null=True)
    date = models.DateField(default=date.today())
    full_sch = models.CharField(max_length=30, default='0')
    contact_details = models.CharField(max_length=10, default='0')
    def __str__(self):
        return self.username

class act(models.Model):       
    username = models.CharField(max_length=10, default='')
    full_sch = models.CharField(max_length=150,null=True)
    active_term = models.CharField(max_length=30, default='0')
    school = models.CharField(max_length=30, default='0')
    def __str__(self):
        return self.username

claz = (
    ('Creche', 'Creche'),
    ('Nursery1', 'Nursery1'),
    ('Nursery2', 'Nursery2'),
    ('K.G1', 'K.G1'),
    ('K.G2', 'K.G2'),
    ('Class1', 'Class1'),
    ('Class2', 'Class2'),
    ('Class3', 'Class3'),
    ('Class4', 'Class4'),
    ('Class5', 'Class5'),
    ('Class6', 'Class6'),
    ('J.H.S1', 'J.H.S1'),
    ('J.H.S2', 'J.H.S2'),
    ('J.H.S3', 'J.H.S3'),
)

class class_fee(models.Model):
    school = models.CharField(max_length=15, default='', null=True)
    classes = models.CharField(max_length=15, default=0, null=True)
    fee = models.FloatField(max_length=15 ,default=0, null=True)
    datey = models.CharField(max_length=15, default=date.today(), null=True)
    def __str__(self):
        return self.school

#['creche','nursery1', 'nursery2', 'kg1', 'kg2', 'class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'jhs1', 'jhs2', 'jhs3']
#['Creche', 'Nursery1', 'Nursery2', 'K.G1', 'K.G2', 'Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']

class classn(models.Model): 
    stu_id = models.CharField(max_length=30,null=True, default=0)
    number = models.CharField(max_length=30,null=True, default=0)
    classA = models.CharField(max_length=30,null=True, default=0)
    classB = models.CharField(max_length=30,null=True, default=0)
    classC = models.CharField(max_length=30,null=True, default=0)
    classD = models.CharField(max_length=30,null=True, default=0)
    classE = models.CharField(max_length=30,null=True, default=0)
    classF = models.CharField(max_length=30,null=True, default=0)
    classG = models.CharField(max_length=30,null=True, default=0)
    classH = models.CharField(max_length=30,null=True, default=0)
    classI = models.CharField(max_length=30,null=True, default=0)
    classJ = models.CharField(max_length=30,null=True, default=0)
    classK = models.CharField(max_length=30,null=True, default=0)
    classL = models.CharField(max_length=30,null=True, default=0)
    classM = models.CharField(max_length=30,null=True, default=0)
    classN = models.CharField(max_length=30,null=True, default=0)
    classO = models.CharField(max_length=30,null=True, default=0)
    school = models.CharField(max_length=30,null=True, default=0)

    def __str__(self):
        return self.classA