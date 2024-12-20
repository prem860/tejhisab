from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Transaction
from django.db.models import Sum
from nepali_datetime import date as nepali_date

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid username or password'})
    return render(request, 'tracker/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    transactions = Transaction.objects.all().order_by('-id')  # Sorting S.N. in descending order

    # Filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    transaction_type = request.GET.get('type')
    description = request.GET.get('description')

    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)
    if transaction_type and transaction_type != "All":
        transactions = transactions.filter(type=transaction_type)
    if description:
        transactions = transactions.filter(description__icontains=description)

    # Calculate totals
    total_income = Transaction.objects.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # Add serial numbers and Nepali dates
    for i, transaction in enumerate(transactions, start=1):
        transaction.sn = i
        transaction.nepali_date = nepali_date.from_datetime_date(transaction.date)

    context = {
        'transactions': transactions,
        'total_income': round(total_income, 2),  # Ensure 2 decimal places
        'total_expense': round(total_expense, 2),  # Ensure 2 decimal places
        'balance': round(balance, 2),  # Ensure 2 decimal places
    }
    return render(request, 'tracker/index.html', context)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        remarks = request.POST.get('remarks')

        Transaction.objects.create(
            type=type,
            amount=amount,
            description=description,
            date=date,
            remarks=remarks,
            added_by=request.user  # Automatically set the current user as 'added_by'
        )
        return redirect('index')
    return render(request, 'tracker/add_transaction.html')

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.type = request.POST.get('type')
        transaction.amount = request.POST.get('amount')
        transaction.description = request.POST.get('description')
        transaction.date = request.POST.get('date')
        transaction.remarks = request.POST.get('remarks')
        transaction.save()  # Save the updated transaction
        return redirect('index')
    return render(request, 'tracker/edit_transaction.html', {'transaction': transaction})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('index')
