from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models


# Review for promotion
class Review(models.Model):
    author = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True, null=True)
    STARS = (
        ('Rating:(1-5)', (
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        )
         ),
    )
    rating = models.IntegerField(choices=STARS, default=1, editable=True)

    def __str__(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def set_description(self, desc):
        self.description = desc

    def get_rating(self):
        return self.rating


# Create your models here.
class Promotion(models.Model):
    #title = models.CharField(max_length=25, unique=True)  # specify the models fields (data type) based on what django provides
    #description = models.TextField(blank=True, null=True)
    STARS = (
        ('Rating:(1-5)', (
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        )
         ),
    )
    rating = models.IntegerField(choices=STARS, default=1, editable=True)
    review = models.ManyToManyField(Review)
    reviewNum = Review.objects.count()

    owner_id = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField()
    picture = models.TextField()
    # rating = models.CharField(max_length=5)
    num_ratings = models.IntegerField(default=0)
    promotion_type = models.TextField()

    def __str__(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def set_description(self, desc):
        self.description = desc

    def set_picture(self, pic):
        self.picture = pic

    def set_rating(self, rating):
        self.rating = rating

    def set_num_ratings(self, num_ratings):
        self.num_ratings = num_ratings

    def set_promotion_type(self, prom):
        self.promotion_type = prom

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_picture(self):
        return self.picture

    def get_rating(self):
        return self.rating

    def get_num_ratings(self):
        return self.num_ratings

    def addReview(self, review):
        self.review.add(review)

    def getNumReviews(self):
        return self.reviewNum

    def getReviews(self):
        lst = []
        for i in range(0, self.review.count()):
            lst.append(self.review.all()[i])
        return lst


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

    proms = models.ManyToManyField(Promotion)
    promos = []
    is_filtered = True

    google_id = models.IntegerField()
    owner_number = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.TextField()
    phone_number = models.CharField(max_length=25)
    email_address = models.CharField(max_length=30)
    website= models.CharField(max_length=75)
    picture = models.CharField(max_length=50)
    category = models.TextField()
    rating = models.CharField(max_length=5)
    yelp = models.TextField()

    def set_owner_number(self, owner_number):
        self.owner_number = owner_number

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def set_email_address(self, email_address):
        self.email_address = email_address

    def set_website(self, website):
        self.website = website

    def set_picture(self, picture):
        self.picture = picture

    def set_category(self, category):
        self.category = category

    def set_rating(self, rating):
        self.rating = rating

    def set_yelp(self, yelp):
        self.yelp = yelp

    def get_owner_number(self):
        return self.owner_number

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_phone_number(self):
        return self.phone_number

    def get_email_address(self):
        return self.email_address

    def get_website(self):
        return self.website

    def get_picture(self):
        return self.picture

    def get_category(self):
        return self.category

    def get_rating(self):
        return self.rating

    def get_yelp(self):
        return self.yelp

    def get_absolute_url(self):
        return reverse('promotions', args=(self.id,))

    def set_filter_status(self, status):
        self.is_filtered = status

    def __str__(self):
        return self.name

    def addPromo(self, promo):
        self.proms.add(promo)

    def fillPromoList(self):
        self.promos.clear()
        for i in range(0, self.proms.count()):
            self.promos.append(self.proms.all()[i])

    def getPromotions(self):
        if len(self.promos) is 0:
            self.fillPromoList()
        return self.promos

    def mostPop(self):
        self.fillPromoList()
        finished = False

        while not finished:
            finished = True
            for i in range(0, len(self.promos)):
                if i + 1 < len(self.promos):
                    if self.promos[i].rating > self.promos[i + 1].rating:
                        self.promos[i], self.promos[i + 1] = self.promos[i + 1], self.promos[i]
                        finished = False

    def leastPop(self):
        self.fillPromoList()
        finished = False
        while not finished:
            finished = True
            for i in range(0, len(self.promos)):
                if i + 1 > len(self.promos):
                    if self.promos[i].rating < self.promos[i+1].rating:
                        self.promos[i], self.promos[i+1] = self.promos[i+1], self.promos[i]
                        finished = False




class Owner(models.Model):
    restaurants = models.ManyToManyField(Restaurant)
    owner_id = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.owner_id
