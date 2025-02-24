from django.db import models
from django.urls import reverse

class Category(models.Model):
  name = models.CharField(max_length=250, unique= True)
  slug = models.SlugField(max_length=250, unique=True)
  description = models.TextField(blank=True, null=True)
  image = models.ImageField(upload_to='category',blank = True,null = True)
  class Meta :
    ordering = ('name',)
    verbose_name = 'CATEGORY'
    verbose_name_plural = "categories"
  def __str__(self):
    return self.name
  def get_url(self):
    return reverse('category_page',args = [self.slug])


class Product(models.Model):
  name = models.CharField(max_length=250, unique= True)
  slug = models.SlugField(max_length=250, unique=True)
  description = models.TextField(blank=True, null=True)
  Category = models.ForeignKey(Category,on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=10,decimal_places=2)
  image = models.ImageField(upload_to='product',blank = True,null = True)
  stock = models.IntegerField()
  avilable = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  update = models.DateTimeField(auto_now=True)
  
  class Meta :
    ordering = ('name',)
    verbose_name = 'Product'
    verbose_name_plural = "Products"
  def get_url(self):
    return reverse('product_page',args = [self.Category.slug, self.slug])
  def __str__(self):
    return self.name
  
class Cart(models.Model) :
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
      db_table = 'Cart'
      ordering = ['date_added']

    def __str__(self):
      return self.cart_id
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
   
    class Meta:
      db_table = 'CartItem'

    def __str__(self):
      return self.product
      db_table = 'Cart'
    def sub_total(self):
      return self.product.price * self.quantity
class Order(models.Model):
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Order Total')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=250, blank=True)
    billingCountry = models.CharField(max_length=250, blank=True)
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=250, blank=True)
    shippingCountry = models.CharField(max_length=250, blank=True)
    
    class Meta:
      db_table = "order"
      ordering = ['-created']

    def __str__(self):
      return str(self.id)

class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product