from django import forms
from .models import AddExpensedb

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = AddExpensedb
        fields = ['NAME', 'ExpenseName', 'Amount', 'Date', 'ExpenseCategory']
