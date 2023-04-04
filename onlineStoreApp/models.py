from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):

    class Meta:
        db_table = 'products'
        ordering = ['id']


    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    catalog_number = models.BigIntegerField(db_column='catalog_number', null=False, blank=False, unique=True)
    manufacturer_id = models.ForeignKey('Manufacturer', on_delete=models.RESTRICT, db_column='manufacturer_id', null=True, blank=True)
    units = models.CharField(max_length=128, db_column='units', null=False, blank=False)
    quantity = models.IntegerField(db_column='quantity', null=False, blank=False)
    category_id = models.ForeignKey('SubCategory', on_delete=models.RESTRICT, db_column='category_id', null=True, blank=True)
    discount_status = models.BooleanField( db_column='discount_status', null=False, blank=False, default=False)
    product_status = models.BooleanField( db_column='product_status', null=False, blank=False, default=True)
    unit_of_measure = models.CharField(max_length=256, db_column='unit_of_measure', null=False, blank=False)
    unit_of_measure_price = models.IntegerField(db_column='unit_of_measure_price', null=False, blank=False)



class Price(models.Model):

    class Meta:
        db_table = 'prices'
        ordering = ['id']
        unique_together = ('product_id', 'retailer_id',)

    product_id = models.ForeignKey('Product', on_delete=models.RESTRICT, db_column='product_id', null=False, blank=False)
    retailer_id = models.ForeignKey('Retailer', on_delete=models.RESTRICT, db_column='retailer_id', null=False, blank=False)
    price = models.SmallIntegerField(db_column='price', null=False, blank=False)



class Retailer(models.Model):

    class Meta:
        db_table = 'retailers'
        ordering = ['id']

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    last_scan = models.BigIntegerField(db_column='last_scan', null=False, blank=False)



class Manufacturer(models.Model):

    class Meta:
        db_table = 'manufacturers'
        ordering = ['id']

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    country = models.CharField(max_length=256, db_column='country', null=True, blank=True)



class Category(models.Model):

    class Meta:
        db_table = 'categories'
        ordering = ['id']

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)



class SubCategory(models.Model):

    class Meta:
        db_table = 'sub_categories'
        ordering = ['id']

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    category_id = models.ForeignKey('Category', on_delete=models.RESTRICT, db_column='category_id', null=True, blank=True)



class Promo(models.Model):

    class Meta:
        db_table = 'promos'
        ordering = ['id']

    type = models.CharField(max_length=256, db_column='type', null=False, blank=False)
    percent =  models.SmallIntegerField(max_length=128, db_column='percent', null=True, blank=True)
    fixed = models.SmallIntegerField(max_length=128, db_column='fixed', null=True, blank=True)
    x = models.SmallIntegerField(max_length=128, db_column='x', null=True, blank=True)
    y = models.SmallIntegerField(max_length=128, db_column='y', null=True, blank=True)
    retailer_id = models.ForeignKey('Retailer', on_delete=models.RESTRICT, db_column='retailer_id', null=False, blank=False)



class PromoProduct(models.Model):

    class Meta:
        db_table = 'promos_products'
        ordering = ['id']

    promo_id = models.ForeignKey('Promo', on_delete=models.RESTRICT, db_column='promo_id', null=False, blank=False)
    product_id = models.ForeignKey('Product', on_delete=models.RESTRICT, db_column='product_id', null=False, blank=False)



class CartProduct(models.Model):

    class Meta:
        db_table = 'cart_products'
        ordering = ['id']

    product_id = models.ForeignKey('Product', on_delete=models.RESTRICT, db_column='product_id', null=False, blank=False)
    quantity = models.SmallIntegerField(db_column='quantity', null=False, blank=False)
    cart_id = models.ForeignKey('Cart', on_delete=models.RESTRICT, db_column='cart_id', null=False, blank=False)



class Cart(models.Model):

    class Meta:
        db_table = 'carts'
        ordering = ['id']

    user_id = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='user_id', null=False, blank=False)
    date = models.BigIntegerField(db_column='date', null=False, blank=False)
    price = models.IntegerField(db_column='price', null=False, blank=False)
    retailer_id = models.ForeignKey('Retailer', on_delete=models.RESTRICT, db_column='retailer_id', null=False, blank=False)
    cart_status = models.BooleanField( db_column='cart_status', null=False, blank=False, default=True)