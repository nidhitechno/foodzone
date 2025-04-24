from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message= models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contact Table'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='Profile/%y/%m/%d', null=True, blank=True)
    address = models.TextField()
    update_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
         verbose_name_plural = 'Profile Table'

class Profile(models.Model):  # ✅ Make sure this exists
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/%Y/%m/%d")
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Category Table'

class Team(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team")
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # facebook_url = models.CharField(blank=True,max_length=200)
    # twitter_url = models.CharField(blank=True,max_length=200)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural = 'Team Table'

# models.py
class Dish(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='dishes/%Y/%m/%d')
    ingredients = models.TextField()
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    discount_percent = models.PositiveIntegerField(default=0)
    discount_price_display = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    def discount_price(self):
        return round(self.price - (self.price * self.discount_percent / 100), 2)
    
    def save(self, *args, **kwargs):
        # Automatically update discount_price_display before saving
        self.discount_price_display = self.discount_price()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Dish Table"

class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    invoice_id = models.CharField(max_length=100, blank=True)
    # payer_id = models.CharField(max_length=100, blank=True)
    payer_id = models.CharField(max_length=255, null=True, blank=True)
    ordered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.first_name

    class Meta:
        verbose_name_plural = "Order Table"

class TableBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time} for {self.guests} guests"
    
class Newslettersubmit(models.Model):
    email = models.EmailField(unique=True)
    submit_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
