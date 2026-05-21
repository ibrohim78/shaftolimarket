from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Buyurtma #{self.id} — {self.customer_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'
