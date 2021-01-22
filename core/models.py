from django.db import models
from django.conf import settings
from django.shortcuts import reverse


CATEGORY_CHOICES = (('S', 'Salon'),
                    ('SW', 'Cuisine'),
                    ('OW', 'Chambre'),
                    ('AU', 'Autre'))

COLOR_CHOICES = (('P', 'primary'),
                 ('S', 'secondary'),
                 ('D', 'danger'))


class Home(models.Model):
    title = models.CharField(max_length=100)
    slider_image = models.ImageField(
        blank=True, upload_to='static/images/')

    def __str__(self):
        return self.title


class Item(models.Model):
    """
    individual item data
    """
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    color = models.CharField(choices=COLOR_CHOICES, max_length=3, default="P")
    slug = models.SlugField()
    description = models.TextField()
    image = models.FileField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse('core:add_to_cart', kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse('core:remove_from_cart', kwargs={"slug": self.slug})


class ItemImage(models.Model):
    item = models.ForeignKey(Item, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to='images/')
    number = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title


class OrderItem(models.Model):
    """
    item list to be in Order
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return (self.quantity * self.item.price)

    def get_total_item_discountPrice(self):
        return (self.quantity * self.item.discount_price)


class Order(models.Model):
    """
    user Order
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
