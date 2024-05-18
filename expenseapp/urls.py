from django.urls import path
from expenseapp import views

urlpatterns = [
    
path('HOME/',views.HOME,name='home'),
path('LOGIN/',views.LOGIN,name='loginpage'),
path('AddingExpense/',views.Addexpensefunction,name='AddingExpensepage'),
path('ExpenseData/',views.Expensedata,name='Expensedata'),
path('ExpenseDisplay/',views.ExpenseDisplay,name='ExpenseDisplay'),
path('ExpenseEdit/<int:dataid>/',views.ExpenseEdit,name='ExpenseEdit'),
path('UpdateExpense/<int:dataid>/',views.Update_Expense,name='UpdateExpense'),
path('DeleteExpense/<int:dataid>/',views.DeleteExpense,name='DeleteExpense'),
path('expense_history/', views.expense_history, name='expense_history'),
path('expense_report/', views.expense_report, name='expense_report'),
path('generate_report/', views.generate_report, name='generate_report'),


 
    
]