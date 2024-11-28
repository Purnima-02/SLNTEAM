from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, franchisesales

@receiver(post_save, sender=Employee)
def create_franchisesales_entry(sender, instance, created, **kwargs):
    # This function runs whenever an Employee entry is created
    if created:
        # Check if the employee meets the specified conditions
        if instance.franchisecode == 'SLNBR001' and instance.employee_type == 'sales':
            # Automatically create a new franchisesales entry
            franchisesales.objects.create(
                Employe=instance,
                registerid=instance.employee_id,
                franchiseCode=instance.franchisecode,  
                name=instance.username,  
                email=instance.email,
                phone=instance.phone_number,
            )
