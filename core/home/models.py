from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.transaction_type} - {self.description}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    month = models.DateField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'category', 'month']
    
    def __str__(self):
        return f"{self.category.name} - {self.month.strftime('%B %Y')}"
    
    def get_spent_amount(self):
        start_date = self.month.replace(day=1)
        if self.month.month == 12:
            end_date = self.month.replace(year=self.month.year + 1, month=1, day=1)
        else:
            end_date = self.month.replace(month=self.month.month + 1, day=1)
        
        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type='EXPENSE',
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        return spent
    
    def get_remaining_amount(self):
        return self.amount - self.get_spent_amount()

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default='something')
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name
