from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User  
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from .models import Expense, Category, Transaction, Budget
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required(login_url='/login/')
def expenses(request):
    salary = 0 
    if request.method == 'POST':
        data = request.POST
        salary = int(data.get('salary', 0))
        name = data.get('name')
        price = int(data.get('price', 0))

        Expense.objects.create(
            salary=salary,
            name=name,
            price=price,
        )
        return redirect('/')

    queryset = Expense.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(
            name__icontains=request.GET.get('search'))

    total_sum = sum(expense.price for expense in queryset)
    
    context = {'expenses': queryset, 'total_sum': total_sum}
    return render(request, 'expenses.html', context)

@login_required(login_url='/login/')
def update_expense(request, id):
    queryset = Expense.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        price = int(data.get('price', 0))

        queryset.name = name
        queryset.price = price
        queryset.save()
        return redirect('/')

    context = {'expense': queryset}
    return render(request, 'update_expense.html', context)

@login_required(login_url='/login/')
def delete_expense(request, id):
    queryset = Expense.objects.get(id=id)
    queryset.delete()
    return redirect('/')

def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                messages.error(request, "Username not found")
                return redirect('/login/')
            user_auth = authenticate(username=username, password=password)
            if user_auth:
                login(request, user_auth)
                return redirect('/')
            messages.error(request, "Wrong Password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
    return render(request, "login.html")

def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, "register.html")

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def pdf(request):
    if request.method == 'POST':
        data = request.POST
        salary = int(data.get('salary'))
        name = data.get('name')
        price = int(data.get('price', 0))

        Expense.objects.create(
            salary=salary,
            name=name,
            price=price,
        )
        return redirect('pdf')

    queryset = Expense.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(
            name__icontains=request.GET.get('search'))

    total_sum = sum(expense.price for expense in queryset)
    username = request.user.username

    context = {'expenses': queryset, 'total_sum': total_sum, 'username':username}
    return render(request, 'pdf.html', context)

@login_required(login_url='/login/')
def dashboard(request):
    today = timezone.now()
    start_date = today.replace(day=1)
    if today.month == 12:
        end_date = today.replace(year=today.year + 1, month=1, day=1)
    else:
        end_date = today.replace(month=today.month + 1, day=1)
    
    transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lt=end_date
    ).order_by('-date')
    
   
    total_income = transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expenses
    
   
    budgets = Budget.objects.filter(user=request.user, month__year=today.year, month__month=today.month)
    budget_status = []
    for budget in budgets:
        spent = budget.get_spent_amount()
        remaining = budget.get_remaining_amount()
        budget_status.append({
            'category': budget.category.name,
            'budget': budget.amount,
            'spent': spent,
            'remaining': remaining,
            'percentage': (spent / budget.amount * 100) if budget.amount > 0 else 0
        })
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'budget_status': budget_status,
        'categories': Category.objects.filter(user=request.user)
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/')
def add_transaction(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        transaction_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        
        try:
            category = Category.objects.get(id=category_id, user=request.user)
            Transaction.objects.create(
                user=request.user,
                category=category,
                transaction_type=transaction_type,
                amount=amount,
                description=description,
                date=date
            )
            messages.success(request, 'Transaction added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding transaction: {str(e)}')
        
        return redirect('dashboard')
    
    context = {
        'categories': Category.objects.filter(user=request.user)
    }
    return render(request, 'add_transaction.html', context)

@login_required(login_url='/login/')
def manage_categories(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        try:
            Category.objects.create(
                user=request.user,
                name=name,
                description=description
            )
            messages.success(request, 'Category added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding category: {str(e)}')
        
        return redirect('manage_categories')
    
    categories = Category.objects.filter(user=request.user)
    return render(request, 'manage_categories.html', {'categories': categories})

@login_required(login_url='/login/')
def set_budget(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        month = request.POST.get('month')
        
        try:
            category = Category.objects.get(id=category_id, user=request.user)
            Budget.objects.update_or_create(
                user=request.user,
                category=category,
                month=month,
                defaults={'amount': amount}
            )
            messages.success(request, 'Budget set successfully!')
        except Exception as e:
            messages.error(request, f'Error setting budget: {str(e)}')
        
        return redirect('dashboard')
    
    context = {
        'categories': Category.objects.filter(user=request.user)
    }
    return render(request, 'set_budget.html', context)

@login_required(login_url='/login/')
def budget_overview(request):
    # Get the selected month from request or default to current month
    selected_month = request.GET.get('month')
    if selected_month:
        try:
            selected_month = datetime.strptime(selected_month, '%Y-%m').date()
        except ValueError:
            selected_month = timezone.now().replace(day=1)
    else:
        selected_month = timezone.now().replace(day=1)
    
    # Calculate start and end dates for the selected month
    start_date = selected_month
    if selected_month.month == 12:
        end_date = selected_month.replace(year=selected_month.year + 1, month=1, day=1)
    else:
        end_date = selected_month.replace(month=selected_month.month + 1, day=1)
    
    # Get all budgets for the selected month
    budgets = Budget.objects.filter(
        user=request.user,
        month__year=selected_month.year,
        month__month=selected_month.month
    ).select_related('category')
    
    
    total_budget = sum(budget.amount for budget in budgets)
    total_spent = sum(budget.get_spent_amount() for budget in budgets)
    total_remaining = total_budget - total_spent
    
    
    chart_data = []
    for budget in budgets:
        spent = budget.get_spent_amount()
        chart_data.append({
            'category': budget.category.name,
            'budget': float(budget.amount),
            'spent': float(spent),
            'remaining': float(budget.get_remaining_amount()),
            'percentage': (spent / budget.amount * 100) if budget.amount > 0 else 0
        })
    
    context = {
        'selected_month': selected_month,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'total_remaining': total_remaining,
        'chart_data': chart_data,
        'budgets': budgets,
        'categories': Category.objects.filter(user=request.user)
    }
    
    return render(request, 'budget.html', context)

@login_required(login_url='/login/')
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id, user=request.user)
    transaction.delete()
    messages.success(request, 'Transaction deleted successfully!')
    return redirect('dashboard')

@login_required(login_url='/login/')
def update_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id, user=request.user)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        transaction_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        
        try:
            category = Category.objects.get(id=category_id, user=request.user)
            transaction.category = category
            transaction.transaction_type = transaction_type
            transaction.amount = amount
            transaction.description = description
            transaction.date = date
            transaction.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error updating transaction: {str(e)}')
    
    context = {
        'transaction': transaction,
        'categories': Category.objects.filter(user=request.user)
    }
    return render(request, 'update_transaction.html', context)

@login_required(login_url='/login/')
def transactions(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    
    transactions = Transaction.objects.filter(user=request.user)
    
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if min_amount:
        transactions = transactions.filter(amount__gte=min_amount)
    if max_amount:
        transactions = transactions.filter(amount__lte=max_amount)
    
    transactions = transactions.order_by('-date')
    
    
    page = request.GET.get('page', 1)
    paginator = Paginator(transactions, 10)  
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)
    
    context = {
        'transactions': transactions,
        'categories': Category.objects.filter(user=request.user),
    }
    return render(request, 'transactions.html', context)