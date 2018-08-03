from django.db import models
from astroquery.utils import TableList

# Create your models here.


class Catalog(models.Model):
    tables = models.TextField()
