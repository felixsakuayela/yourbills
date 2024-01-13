from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from expense.models import Expense, ShareRequest, Spent
from expense.forms import ExpenseForm, SpentForm
from django.contrib.auth.decorators import login_required
from reversion.models import Version

@login_required
def home(request):
    
    expenses_created = Expense.objects.filter(user_create=request.user, active=True)
   
    expenses_shared = Expense.objects.filter(
        spent__users_shared=request.user,
        spent__sharerequest__status='A',
        active=True
    ).distinct()

    expenses_with_user_spents = Expense.objects.filter(spent__user=request.user, active=True).distinct()
    expenses = expenses_created.union(expenses_shared, expenses_with_user_spents)

    return render(request, 'home.html', {'expenses': expenses})

@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(Expense, id=expense_id)

    if request.user != expense.user_create:
        return HttpResponseForbidden("Você não tem permissão")
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expense/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(Expense, id=expense_id)

    if request.user != expense.user_create:
        return HttpResponseForbidden("Você não tem permissão")
    
    expense = get_object_or_404(Expense, id=expense_id)
    expense.active = False
    expense.save()

    return redirect('home')

@login_required
def view_history(request, expense_id):

    expense = get_object_or_404(Expense, id=expense_id)

    if request.user != expense.user_create:
        return HttpResponseForbidden("Você não tem permissão")
    
    versions = Version.objects.get_for_object(expense)

    return render(request, 'expense/history_expense.html', {'expense': expense, 'versions': versions})

@login_required
def pending_spents(request):
    
    received_pending_share_requests = ShareRequest.objects.filter(user_approving=request.user, status='P')
    received_pending_spents = [share_request.spent for share_request in received_pending_share_requests]

    sent_pending_share_requests = ShareRequest.objects.filter(user_requesting=request.user, status='P')
    sent_pending_spents = [share_request.spent for share_request in sent_pending_share_requests]

    reproved_pending_share_requests = ShareRequest.objects.filter(user_requesting=request.user, status='R')
    reproved_pending_spents = [share_request.spent for share_request in reproved_pending_share_requests]

    return render(request, 'expense/pending_spents.html', {'received_pending_spents': received_pending_spents, 'sent_pending_spents': sent_pending_spents, 'reproved_pending_spents': reproved_pending_spents})

@login_required
def resubmit_spent(request, spent_id):
    
    spent = get_object_or_404(Spent, id=spent_id)

    share_request = get_object_or_404(ShareRequest, spent=spent, user_requesting=request.user)
    share_request.status = 'P'
    share_request.save()
    
    return redirect('pending_spents')

@login_required
def approve_spent(request, spent_id):

    spent = get_object_or_404(Spent, id=spent_id)

    share_request = get_object_or_404(ShareRequest, spent=spent, user_approving=request.user)
    share_request.status = 'A'
    share_request.save()

    return redirect('pending_spents')

@login_required
def reject_spent(request, spent_id):

    spent = get_object_or_404(Spent, id=spent_id)

    share_request = get_object_or_404(ShareRequest, spent=spent, user_approving=request.user)
    share_request.status = 'R'
    share_request.save()

    return redirect('pending_spents')

