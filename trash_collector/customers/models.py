from django.db import models

class Customer(models.Model):
    MONDAY = 'MON'
    TUESDAY = 'TUES'
    WEDNESDAY = 'WED'
    THURSDAY = 'THURs'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'  
    DAY_CHOICES = (
        (MONDAY, 'MONDAY'),
        (TUESDAY, 'TUESDAY'),
        (WEDNESDAY, 'WEDNESDAY'),
        (THURSDAY, 'THURSDAY'),
        (FRIDAY, 'FRIDAY'),
        (SATURDAY, 'SATURDAY'),
        (SUNDAY, 'SUNDAY')
    )
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
    weekly_pickup = models.CharField(max_length=10)
    one_time_pickup = models.DateField(null=True, blank=True)
    suspend_start = models.DateField(null=True, blank=True)
    suspend_end = models.DateField(null=True, blank=True)
    date_of_last_pickup = models.DateField(null=True, blank=True)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name