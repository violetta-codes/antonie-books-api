from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class Office(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the office.")
    location = models.CharField(max_length=255, help_text="Location of the office.")

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    # TODO: implement methods for generating reports once the rest of the models are defined
    phone_number = models.CharField(max_length=15)
    office = models.ForeignKey(Office,
                               on_delete=models.CASCADE,
                               related_name='employees',
                               null=True)

    @property
    def employee(self):
        return self.groups.filter(name="Employees").exists() or self.is_superuser

    def __str__(self):
        return self.username

class Package(models.Model):
    DELIVERY_TYPE_CHOICES = [
        ('office', 'Office'),
        ('address', 'Address'),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('lost', 'Lost'),
    ]
    content = models.CharField(max_length=255,
                               help_text='What the package contains.')
    sender = models.ForeignKey(CustomUser,
                               related_name='sent_packages',
                               on_delete=models.CASCADE,
                               help_text="The user who sent the package.")
    receiver = models.ForeignKey(CustomUser,
                                 related_name='received_packages',
                                 on_delete=models.CASCADE,
                                 help_text="The user who receives the package."
    )
    delivery_address = models.CharField(max_length=255,
                                        blank=True,
                                        null=True,
                                        help_text="Address for delivery (if applicable)."
    )
    office = models.ForeignKey(Office,
                               related_name='packages',
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               help_text="Office location for delivery/pickup (if applicable)."
    )
    weight = models.DecimalField(max_digits=5,
                                 decimal_places=2,
                                 help_text="Weight of the package in kilograms.")
    delivery_type = models.CharField(max_length=10,
                                     choices=DELIVERY_TYPE_CHOICES,
                                     help_text="Type of delivery: to office or address."
    )
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='submitted',
                              help_text="Current status of the package."
    )
    price = models.DecimalField(max_digits=7,
                                decimal_places=2,
                                help_text="Price of the delivery."
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, help_text="Time when the package was registered.")

    def clean(self):
        super().clean()

        # Custom validation to ensure at least one field is filled out
        if not self.office and not self.delivery_address:
            raise ValidationError('Either office or location must be provided.')

    def calculate_price(self):
        """Calculate the price based on weight and delivery type."""
        base_price = Decimal(5)
        weight_factor = Decimal(2)

        # Deliveries to offices are cheaper
        if self.delivery_type == 'office':
            return base_price + self.weight * weight_factor * Decimal(0.8)
        return base_price + self.weight * weight_factor

    def save(self, *args, **kwargs):
        self.price = self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Package from {self.sender} to {self.receiver} ({self.delivery_type}, {self.status})"

class Company(models.Model):
    pass
