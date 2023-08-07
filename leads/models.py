from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


# Create your models here.
        #USER MODEL TO REGISTER AGENTS
        ## - HERE  WE USE A PREDEFINED MODEL BY DJANGO TO REGISTER USER HAVING ALL NECESSARY FIELDS

class User(AbstractUser):
    # To limit the views for agent and organizers
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class lead(models.Model):
    #LEADS
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default = 0)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    agent = models.ForeignKey("Agent",null=True,blank=True, on_delete=models.SET_NULL)   #SHOWS THAT EVERY LEAD HAS A AGENT
                                                                   #CASCADE means if the agent related to that lead is deleted thn also delete the lead.
    category = models.ForeignKey("Category", related_name="leads" ,null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    'FOREIGN KEY CREATES A CONNECTIVITY BETWEEN TABLES'

        #AGENTS
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
class Category(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
#test user password = admin_user
def post_save_create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(post_save_create_userprofile, sender=User)
