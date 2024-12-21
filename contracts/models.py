from django.contrib.auth.models import User
from django.db import models

class Contract(models.Model):    
    STATUS_CHOICES = [
        ('created', 'created'),
        ('sent', 'sent'),
        ('completed', 'completed'),
        ('signed', 'signed'),
        ('failed', 'failed'),
    ]

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    envelope_id = models.CharField(max_length=255, unique=True)  
    recipient_email = models.EmailField()  
    recipient_name = models.CharField(max_length=255)  
    contract_text = models.TextField(
        default = """
        It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. 
        The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, 
        making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, 
        and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, 
        sometimes by accident, sometimes on purpose. Please sign the contract here: ~signature~
        """
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')  
    created_at = models.DateTimeField(auto_now_add = True)  
    signed_by_user = models.BooleanField(default = False) 
    signed_by_recipient = models.BooleanField(default = False) 
    signed_at_user = models.DateTimeField(null=True, blank = True)  
    signed_at_recipient = models.DateTimeField(null = True, blank = True)  
    contract_name = models.CharField(max_length = 255, null = True, blank = True) 
    start_date = models.DateField(null = True, blank = True)  
    end_date = models.DateField(null = True, blank = True)  
    
    def __str__(self):
        return f'Contract {self.envelope_id} for {self.recipient_email}'
    
    def is_complete(self):
        return self.status == 'completed'and self.signed_by_user and self.signed_by_recipient

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'contract'
        verbose_name_plural = 'contracts'