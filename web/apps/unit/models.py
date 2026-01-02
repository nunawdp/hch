from django.db import models

# Create your models here.
class Unit(models.Model):
    NAME_CHOICES = [
        ("KPN", "KPN"),
        ("MBLE", "MBLE"),
        ("WWPI", "WWPI"),
        ("BBS", "BBS"),
        ("MJR", "MJR"),
    ]
    
    BRAND_CHOICES = [
        ("HINO", "HINO"),
        ("MERCEDEZ BANZ", "MERCEDEZ BANZ"),
        ("SCANIA", "SCANIA"),
        ("DONGFENG", "DONGFENG"),
        ("FOTON", "FOTON"),
    ]
    
    PREFIX_CHOICES = [
        ("KPNDT", "KPNDT"),
        ("DTMB", "DTMB"),
        ("DTWG", "DTWG"),
        ("BSDT", "BSDT"),
        ("MJRDT", "MJRDT"),
    ]
    name = models.CharField(max_length=25, choices=NAME_CHOICES, default=NAME_CHOICES[0][0])
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default=BRAND_CHOICES[0][0])
    prefix = models.CharField(max_length=10, choices=PREFIX_CHOICES, default=PREFIX_CHOICES[0][0])
    code = models.CharField(max_length=10, null=True)
    tara = models.PositiveIntegerField(null=True, blank=True)
    operator = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ("name", "code")
    
    def __str__(self):
        return f'{self.prefix}-{self.code}'