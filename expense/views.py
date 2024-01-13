from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm, SpentForm, ShareRequest
from django.contrib.auth.decorators import login_required
from .models import Expense, Spent
from django.db.models import Q, Sum
from django.http import HttpResponseForbidden
from expense.forms import UserFilterForm

@login_required
def create_expense(request):

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user_create = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'expense/create_expense.html', {'form': form})

@login_required
def create_spent(request):

    if request.method == 'POST':
        form = SpentForm(request.POST, user=request.user)
        if form.is_valid():
            spent = form.save(commit=False)
            spent.user = request.user
            spent.save()
            form.save_m2m()

            users_shared = spent.users_shared.all()
            for user_shared in users_shared:
                if user_shared != request.user:
                    ShareRequest.objects.create(
                        spent=spent,
                        user_requesting=request.user,
                        user_approving=user_shared,
                        status='P', 
                        date_create=spent.date_create,
                        date_modified=spent.date_modified,
                    )
            spent.users_shared.clear()
            spent.users_shared.add(*users_shared)
            spent.save()
            form.save_m2m()

            return redirect('home')
    else:
        form = SpentForm(user=request.user)

    return render(request, 'expense/create_spent.html', {'form': form})

@login_required
def list_spents(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.user != expense.user_create and request.user not in expense.spent_set.filter(users_shared=request.user):
        shared_spents = Spent.objects.filter(users_shared=request.user, expense=expense, sharerequest__status='A')
        
        if not shared_spents.exists():
            return HttpResponseForbidden("Você não tem permissão.")

    spents = Spent.objects.filter(
        Q(expense=expense, user=request.user) | 
        Q(expense=expense, users_shared=request.user, sharerequest__status='A')
    ).distinct()

    user_totals = {}
    for spent in spents:
        if spent.user.username not in user_totals:
            user_totals[spent.user.username] = 0
        user_totals[spent.user.username] += spent.value

    total_spent = sum(user_totals.values())

    return render(request, 'expense/list_spents.html', {'spents': spents, 'expense': expense, 'user_totals': user_totals, 'total_spent': total_spent})

@login_required
def view_spent(request, expense_id, spent_id):

    expense = get_object_or_404(Expense, id=expense_id)
    spent = get_object_or_404(Spent, id=spent_id, expense=expense)

    if request.user != expense.user_create and request.user not in expense.spent_set.filter(users_shared=request.user):
        shared_spents = Spent.objects.filter(users_shared=request.user, expense=expense, sharerequest__status='A')
        if not shared_spents.exists():
            return HttpResponseForbidden("Você não tem permissão.")

    return render(request, 'expense/spent.html', {'spent': spent, 'expense': expense})

@login_required
def dashboard_spents(request):
    user = request.user

    if request.method == 'POST':
        form = UserFilterForm(user, request.POST)
        if form.is_valid():
            recebidas = form.cleaned_data.get('recebidas', [])
            enviadas = form.cleaned_data.get('enviadas', [])
        else:
            recebidas = []
            enviadas = []
    else:
        form = UserFilterForm(user)
        recebidas = []
        enviadas = []

    expenses = Expense.objects.filter(Q(user_create=user) | Q(spent__users_shared=user)).distinct()

    # Filtra os gastos de acordo com os usuários selecionados no formulário
    if recebidas or enviadas:
        spents = Spent.objects.filter(
            Q(expense__in=expenses, user__in=recebidas) |
            Q(expense__in=expenses, users_shared__in=enviadas, sharerequest__status='A')
        ).distinct()
    else:
        spents = Spent.objects.filter(
            Q(expense__in=expenses, user=user) |
            Q(expense__in=expenses, users_shared=user, sharerequest__status='A')
        ).distinct()

    # Agrupa os gastos por despesa e calcula o total gasto por despesa
    expenses_with_spents = []
    for expense in expenses:
        expense_spents = spents.filter(expense=expense)
        total_spent = expense_spents.aggregate(Sum('value'))['value__sum']
        expenses_with_spents.append({
            'expense': expense,
            'spents': expense_spents,
            'total_spent': total_spent,
        })

    return render(request, 'expense/dashboard_spents.html', {'form': form, 'expenses_with_spents': expenses_with_spents})

@login_required
def edit_spent(request, spent_id):

    spent = get_object_or_404(Spent, id=spent_id)

    if request.user != spent.user:
        return HttpResponseForbidden("Você não tem permissão")
    
    if request.method == 'POST':
        form = SpentForm(request.POST, instance=spent)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SpentForm(instance=spent)

    return render(request, 'expense/edit_spent.html', {'form': form})
