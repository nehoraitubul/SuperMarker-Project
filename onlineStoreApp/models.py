import uuid
import time

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField

# Create your models here.

def current_timestamp():
    return int(time.time())

class Product(models.Model):

    class Meta:
        db_table = 'products'
        ordering = ['id']


    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    catalog_number = models.BigIntegerField(db_column='catalog_number', null=False, blank=False, unique=True)
    manufacturer_id = models.ForeignKey('Manufacturer', on_delete=models.RESTRICT, db_column='manufacturer_id', null=True, blank=True)
    units = models.CharField(max_length=128, db_column='units', null=False, blank=False)
    category_id = models.ForeignKey('SubSubSubCategory', on_delete=models.RESTRICT, db_column='category_id', null=True, blank=True)
    quantity = models.IntegerField(db_column='quantity', null=False, blank=False)
    discount_status = models.BooleanField( db_column='discount_status', null=False, blank=False, default=False)
    product_status = models.BooleanField( db_column='product_status', null=False, blank=False, default=True)
    unit_of_measure = models.CharField(max_length=256, db_column='unit_of_measure', null=False, blank=False)
    unit_of_measure_price = models.IntegerField(db_column='unit_of_measure_price', null=False, blank=False)
    product_info_id = models.ForeignKey('ProductInfo', on_delete=models.SET_NULL, db_column='product_info_id', null=True, blank=True)
    image = models.URLField(db_column='image', null=True, blank=True)
    sold_qty = models.IntegerField(db_column='sold_qty', null=False, blank=False, default=0)
    rating = models.IntegerField(db_column='rating', null=False, blank=False, default=0)
    checked = models.IntegerField(db_column='checked', null=False, blank=False, default=0)
    search_vector = SearchVectorField(null=True, blank=True)


class Price(models.Model):

    class Meta:
        db_table = 'prices'
        ordering = ['id']
        unique_together = ('product_id', 'retailer_id',)

    product_id = models.ForeignKey('Product', on_delete=models.RESTRICT, db_column='product_id', null=False, blank=False)
    retailer_id = models.ForeignKey('Retailer', on_delete=models.RESTRICT, db_column='retailer_id', null=False, blank=False)
    price = models.DecimalField(db_column='price', null=False, blank=False, max_digits=10, decimal_places=2)



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

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False, unique=True)



class SubCategory(models.Model):

    class Meta:
        db_table = 'sub_categories'
        ordering = ['id']

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    category_id = models.ForeignKey('Category', on_delete=models.RESTRICT, db_column='category_id', null=True, blank=True)



class SubSubCategory(models.Model):

    class Meta:
        db_table = 'sub_sub_categories'
        ordering = ['id']

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    sub_category_id = models.ForeignKey('SubCategory', on_delete=models.RESTRICT, db_column='sub_category_id', null=True, blank=True)



class SubSubSubCategory(models.Model):

    class Meta:
        db_table = 'sub_sub_sub_categories'
        ordering = ['id']

    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    sub_sub_category_id = models.ForeignKey('SubSubCategory', on_delete=models.RESTRICT, db_column='sub_sub_category_id', null=True, blank=True)



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
        unique_together = ('cart_id', 'product_id')

    product_id = models.ForeignKey('Product', on_delete=models.RESTRICT, db_column='product_id', null=False, blank=False)
    quantity = models.SmallIntegerField(db_column='quantity', null=False, blank=False)
    cart_id = models.ForeignKey('Cart', on_delete=models.RESTRICT, db_column='cart_id', null=False, blank=False)



class Cart(models.Model):

    class Meta:
        db_table = 'carts'
        ordering = ['id']

    user_id = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='user_id', null=True, blank=True)
    date = models.BigIntegerField(db_column='date', null=False, blank=False, default=current_timestamp)
    price = models.DecimalField(db_column='price', null=False, blank=False, default=0, max_digits=10, decimal_places=2)
    # retailer_id = models.ForeignKey('Retailer', on_delete=models.RESTRICT, db_column='retailer_id', null=False, blank=False)
    cart_status = models.BooleanField(db_column='cart_status', null=False, blank=False, default=True)
    cart_key = models.UUIDField(db_column='cart_key', default=uuid.uuid4, unique=True)

    products = models.ManyToManyField('Product', related_name='cart', through='CartProduct')


class ProductInfo(models.Model):

    class Meta:
        db_table = 'products_info'
        ordering = ['id']

    dietary_fiber = models.CharField(max_length=128, db_column='dietary_fiber', null=True, blank=True)       # סיבים תזונתיים
    sugars_from_carbohydrates = models.CharField(max_length=128, db_column='sugars_from_carbohydrates', null=True, blank=True)       # סוכרים מפחמימות
    energy = models.CharField(max_length=128, db_column='energy', null=True, blank=True)       # אנרגיה
    proteins = models.CharField(max_length=128, db_column='proteins', null=True, blank=True)       # חלבונים
    carbohydrates = models.CharField(max_length=128, db_column='carbohydrates', null=True, blank=True)       # פחמימות
    fats = models.CharField(max_length=128, db_column='fats', null=True, blank=True)        # שומנים
    sodium = models.CharField(max_length=128, db_column='sodium', null=True, blank=True)      # נתרן
    salt = models.CharField(max_length=128, db_column='salt', null=True, blank=True)        #מלח
    cholesterol = models.CharField(max_length=128, db_column='cholesterol', null=True, blank=True)     # כולסטרול
    saturated_fat = models.CharField(max_length=128, db_column='saturated_fat', null=True, blank=True)       # שומן רווי
    trans_fatty_acids = models.CharField(max_length=128, db_column='trans_fatty_acids', null=True, blank=True)       # חומצות שומן טראנס
    sugar = models.CharField(max_length=128, db_column='sugar', null=True, blank=True)       # סוכר
    iron = models.CharField(max_length=128, db_column='iron', null=True, blank=True)  # ברזל
    calcium = models.CharField(max_length=128, db_column='calcium', null=True, blank=True)  # סידן
    local_rabbinate = models.CharField(max_length=128, db_column='local_rabbinate', null=True, blank=True)     # רבנות מקומית
    kosher_type = models.CharField(max_length=128, db_column='kosher_type', null=True, blank=True)     #פרווה - חלבי - בשרי
    kosher = models.CharField(max_length=128, db_column='kosher', null=True, blank=True)      # כשרות
    passover = models.CharField(max_length=128, db_column='passover', null=True, blank=True)         # פסח
    component = models.TextField(db_column='component', null=True, blank=True)        # רכיבים
    allergies_properties = models.CharField(max_length=768, db_column='allergies_properties', null=True, blank=True)        # מכיל לאלרגנים
    allergies_traces = models.CharField(max_length=768, db_column='allergies_traces', null=True, blank=True)         # עלול להכיל לאלרגנים
    no_preserv = models.BooleanField(db_column='no_preserv', null=False, blank=False, default=False) # סימון בריאותי - מכיל גלוטן
    lactose_free = models.BooleanField(db_column='lactose_free', null=False, blank=False, default=False) #   סימון בריאותי - מכיל לקטוז
    gluten_free =  models.BooleanField(db_column='gluten_free', null=False, blank=False, default=False) # סימון בריאותי - מכיל גלוטן
    organic =  models.BooleanField(db_column='organic', null=False, blank=False, default=False) # סימון בריאותי - אורגני
    description = models.TextField(db_column='description', null=True, blank=True)  # על המוצר