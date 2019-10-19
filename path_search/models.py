from django.db import models

# Create your models here.

# class User(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     email = models.EmailField()


from django.db import models
import pickle
# Create your models here.
class CompoundsName(models.Model):
    name = models.CharField(max_length=60)
    cnum = models.CharField(max_length=30)

# name_cnum_data=pickle.load(open('/Users/xubo/Desktop/work/0927 软件测试/TEST/input_complete/name_cnum.pkl','rb'))
# for name in name_cnum_data:
#     CN = CompoundsName()
#     CN.name = name
#     CN.cnum = name_cnum_data[name]
#     CN.save() 