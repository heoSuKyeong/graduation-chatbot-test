from django.db import models

class MainCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'main_categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'


class Product(models.Model):
    name = models.CharField(max_length=255)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products")
    photo = models.URLField(blank=True, null=True)  # Photo URL
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    energy_efficiency = models.CharField(max_length=50, blank=True, null=True)
    power_consumption = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'products'


class Aspect(models.Model):
    aspect = models.CharField(max_length=255)

    class Meta:
        db_table = 'aspects'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    raw_text = models.TextField()
    source = models.CharField(max_length=255, blank=True, null=True)
    review_score = models.IntegerField(blank=True, null=True)
    syllable_count = models.IntegerField(blank=True, null=True)
    word_count = models.IntegerField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    general_polarity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'reviews'


class ReviewAspect(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review_aspects")
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE, related_name="review_aspects")
    sentiment_text = models.TextField(blank=True, null=True)
    sentiment_word_count = models.IntegerField(blank=True, null=True)
    sentiment_polarity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'review_aspects'
