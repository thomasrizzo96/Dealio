from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
class Promotion(models.Model):
    title = models.CharField(max_length=25, unique=True)  # specify the models fields (data type) based on what django provides
    description = models.TextField(blank=True, null=True)
    STARS = (
        ('Rating:(1-5)', (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        )
         ),
    )
    rating = models.CharField(max_length=1, choices=STARS, default=1)

    def __str__(self):
        return self.title
    def set_title(self, title):
        self.title = title
    def set_description(self, desc):
        self.description = desc
    def set_rating(self, rating):
        self.rating = rating


class Restaurant(models.Model):
    categoryOptions = (
        ('Food Choice',(
                ('American', 'American'),
                ('Chinese', 'Chinese'),
                ('Indian', 'Indian'),
                ('Mexican', 'Mexican'),
                ('Italian', 'Italian'),
            )
         ),
    )
    name = models.CharField(max_length=25, unique=True)
    proms = models.ManyToManyField(Promotion)
    category = models.CharField(max_length=10, choices=categoryOptions)
    review_link = models.CharField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('promotions', args=(self.id,))


    def __str__(self):
        return self.name

    def get_review_link(self):
        return self.review_link

    def getCategory(self):
        return self.category

    def addPromo(self, promo):
        self.proms.add(promo)

    def getPromotions(self):
        promos = []
        for i in range(0,self.proms.count()):
            promos.append(self.proms.all()[i])
        finished = False
        while not finished:
            finished = True
            for i in range(0,len(promos)):
                if i + 1 < len(promos):
                    if promos[i].rating < promos[i+1].rating:
                        promos[i], promos[i+1] = promos[i+1], promos[i]
                        finished = False
        return promos


class Owner(models.Model):
    restaurants = models.ManyToManyField(Restaurant)
    owner_id = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.owner_id
