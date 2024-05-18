from django.shortcuts import render,redirect
from expenseapp.models import AddExpensedb
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum, Count, F, Min
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay
from django.http import HttpResponse ,JsonResponse
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncDay





# Create your views here.
@login_required
def HOME(request):
    current_user = request.user
    today = datetime.today()
    current_month = today.month
    current_year = today.year
    expenses = AddExpensedb.objects.filter(user=current_user,Date__month=current_month, Date__year=current_year)
    total_expense = expenses.aggregate(Sum('Amount'))['Amount__sum']
    recent_transactions = AddExpensedb.objects.filter(user=request.user).order_by('-Date')[:5]
    # Query expenses by categories
    categories = [
        "Health Care",
        "Entertainment",
        "Insurance",
        "Food",
        "Education",
        "Transportation",
        "Housing",
        "Utilities",
        "PersonalCare",
        "ChildCare",
        "Taxes",
        "DebtPayments",
        "Gifts and Donations",
        "Travel",
        "Home and Office",
        "Emergency Fund",
        "Others",
    ]
    
    category_expenses = []

    
    for category in categories:
        category_total = expenses.filter(ExpenseCategory=category).aggregate(Sum('Amount'))['Amount__sum']
        category_expenses.append(category_total or 0)
        
    categories_json = json.dumps(categories)
    category_expenses_json = json.dumps([float(value) for value in category_expenses])


    # Create a context dictionary to pass data to the template
    context = {
        'total_expense': total_expense,
        'recent_transactions': recent_transactions,
        'categories': categories_json,
        'category_expenses': category_expenses_json,
    }

    return render(request, "home.html", context)
    
    
    
def LOGIN(request):
    return render(request,"login.html")

def Addexpensefunction(request):
    return render(request,"addexpense.html")

def Expensedata(request):
    if request.method == "POST":
        user = request.user
        na = request.POST.get('userName')
        en = request.POST.get('expenseName')
        am = request.POST.get('amountSpent')
        if not am:
            messages.error(request,'Please enter the amount spent!')
            return render(request,"addexpense.html")
        dt = request.POST.get('currentDate')
        ec = request.POST.get('expenseCategory')
        obj = AddExpensedb(user=user,NAME=na,ExpenseName=en,Amount=am,Date=dt,ExpenseCategory=ec)
        obj.save()
        messages.success(request,"Expense Added Successfully")
        return redirect(Addexpensefunction)
    
def ExpenseDisplay(request):
    data = AddExpensedb.objects.filter(user=request.user)
    return render(request,'displayexpense.html',{'data':data})


def ExpenseEdit(request,dataid):
    data = AddExpensedb.objects.get(id=dataid)
    return render(request,"editexpense.html",{'data':data})


def Update_Expense(request,dataid):
    if request.method=="POST":
        na = request.POST.get('userName')
        en = request.POST.get('expenseName')
        am = request.POST.get('amountSpent')
        dt = request.POST.get('currentDate')
        ec = request.POST.get('expenseCategory')
        AddExpensedb.objects.filter(id=dataid).update(NAME=na,ExpenseName=en,Amount=am,Date=dt,ExpenseCategory=ec)
        messages.success(request,"Updated Successfully")
        return redirect(expense_history)
    
def DeleteExpense(request,dataid):
    data = AddExpensedb.objects.filter(id=dataid)
    data.delete()
    messages.success(request, "Expense deleted Successfully")
    return redirect(expense_history)


def expense_history(request):
    # Get the user from the request
    user = request.user

    # Initialize filter variables
    category_filter = request.GET.get('category', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    search_filter = request.GET.get('search', '')

    # Fetch all expenses for the user
    expenses = AddExpensedb.objects.filter(user=user)

    # Apply filters
    if category_filter:
        expenses = expenses.filter(ExpenseCategory=category_filter)

    if start_date_filter:
        expenses = expenses.filter(Date__gte=start_date_filter)

    if end_date_filter:
        expenses = expenses.filter(Date__lte=end_date_filter)

    if search_filter:
        expenses = expenses.filter(
            Q(NAME__icontains=search_filter) |  # Search by expense name
            Q(ExpenseName__icontains=search_filter)  # Search by expense description
        )

    # Paginate the expenses
    page = request.GET.get('page', 1)
    items_per_page = 10  # Number of items per page
    paginator = Paginator(expenses, items_per_page)
    try:
        expense_page = paginator.page(page)
    except PageNotAnInteger:
        expense_page = paginator.page(1)
    except EmptyPage:
        expense_page = paginator.page(paginator.num_pages)

    context = {
        'expense_page': expense_page,
        'category_filter': category_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
        'search_filter': search_filter,
    }

    return render(request, 'expensehistory.html', context)


def expense_report(request):
    report_type = request.GET.get('report-type', 'monthly')
    
    if report_type == 'monthly':
        # Get monthly expenses
        monthly_expenses = AddExpensedb.objects.filter(user=request.user).annotate(
            month=TruncMonth('Date')
        ).values('month').annotate(total_amount=Sum('Amount'))

        context = {
            'report_type': report_type,
            'monthly_expenses': monthly_expenses,
        }
    elif report_type == 'yearly':
        # Get a list of distinct years for the yearly report
        distinct_years = AddExpensedb.objects.filter(user=request.user).dates('Date', 'year', order='DESC').distinct()
        
        context = {
            'report_type': report_type,
            'distinct_years': distinct_years,
        }

    return render(request, 'expensereport.html', context)







def generate_report(request):
    current_user = request.user

    if request.method == 'POST':
        selected_month = request.POST.get('selected_month')
        selected_year = request.POST.get('selected_year', datetime.now().year)

        try:
            selected_month = int(selected_month) if selected_month and selected_month != 'Select month' else None
        except ValueError:
            selected_month = None

        # Handle the case where 'Select year' is selected in the form
        if selected_year == 'Select year':
            selected_year = None
        else:
            selected_year = int(selected_year)

        # If only month is selected without a year, provide a message
        if selected_month and not selected_year:
            error_message = "Please select a year along with the month."
            context = {'error_message': error_message}
            return render(request, 'expensereport.html', context)
        
        

        # If both month and year are selected, display daily expenses
        if selected_month and selected_year:
            expenses = AddExpensedb.objects.filter(user=current_user, Date__month=selected_month, Date__year=selected_year)
            report_type = f"Daily Report for {selected_month}, {selected_year}"
        # If only year is selected, display monthly expenses
        elif selected_year:
            expenses = AddExpensedb.objects.filter(user=current_user, Date__year=selected_year)
            report_type = f"Monthly Report for {selected_year}"
        else:
            # Handle other cases or provide a default behavior
            return HttpResponse("Invalid selection")

        total_expense = expenses.aggregate(Sum('Amount'))['Amount__sum']

        categories_data = (
            expenses.values('ExpenseCategory')
            .annotate(total_expense=Sum('Amount'))
            .order_by('ExpenseCategory')
        )

        # Total Expense by Category
        total_expense_by_category = (
            expenses.values('ExpenseCategory')
            .annotate(total_expense=Sum('Amount'))
            .order_by('ExpenseCategory')
        )

        # Adjust the date filtering based on the selected_month and selected_year
        if selected_month and selected_year:
            daily_expenses = expenses.values(day=ExtractDay('Date')) \
                .annotate(total_expense=Sum('Amount'))

            chart_labels = [f"{selected_month}-{expense['day']}-{selected_year}" for expense in daily_expenses]
            chart_data = [expense['total_expense'] for expense in daily_expenses]
        else:
            monthly_expenses = expenses.values(month=ExtractMonth('Date')) \
                .annotate(total_expense=Sum('Amount'))

            chart_labels = [f"{expense['month']}-{selected_year}" for expense in monthly_expenses]
            chart_data = [expense['total_expense'] for expense in monthly_expenses]

        context = {
            'report_type': report_type,
            'selected_month': selected_month,
            'selected_year': selected_year,
            'expenses': expenses,
            'total_expense': total_expense or 0,
            'categories_data': categories_data,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
            'total_expense_by_category': total_expense_by_category,
        }

        return render(request, 'expensereport.html', context)
    else:
        current_date = datetime.now()
        context = {
            'selected_month': None,
            'selected_year': current_date.year,
        }
        return render(request, 'expensereport.html', context)


    


