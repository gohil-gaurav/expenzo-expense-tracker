from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
from .forms import CustomSignupForm
from datetime import datetime
from django.db.models.functions import TruncMonth


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'expenses/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomSignupForm()

    return render(request, 'expenses/auth/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'expenses/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@login_required
def dashboard(request):
    qs = Expense.objects.filter(user=request.user)

    # Date range from query params
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        qs = qs.filter(date__range=[start_date, end_date])

    # Totals
    total_income = qs.filter(transaction_type='INCOME').aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expense = qs.filter(transaction_type='EXPENSE').aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance = total_income - total_expense

    # Pie chart (category-wise)
    category_data = (
        qs.filter(transaction_type='EXPENSE')
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Bar chart (monthly)
    monthly_data = (
        qs.filter(transaction_type='EXPENSE')
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,

        'category_labels': [c['category'] for c in category_data],
        'category_totals': [float(c['total']) for c in category_data],

        'month_labels': [
            m['month'].strftime('%b %Y') for m in monthly_data
        ],
        'month_totals': [float(m['total']) for m in monthly_data],

        # keep dates selected
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'expenses/dashboard.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)

    month = request.GET.get('month')
    year = request.GET.get('year')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if month:
        expenses = expenses.filter(date__month=int(month))
    if year:
        expenses = expenses.filter(date__year=int(year))

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    months = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December')
    ]

    current_year = datetime.now().year
    years = range(current_year - 3, current_year + 1)

    context = {
        'expenses': expenses.order_by('-date'),
        'months': months,
        'years': years,
        'selected_month': month,
        'selected_year': year,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'expenses/expense_list.html', context)



@login_required
def edit_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)

    if(request.method == 'POST'):
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)

    if(request.method == 'POST'):
        expense.delete()
        return redirect('expense_list')
    
    return render(request, 'expenses/delete_expense.html', {'expense': expense})