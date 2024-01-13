from django import forms
from django.db.models import Q
from .models import Expense, Spent, User, ShareRequest
from django.core.exceptions import ValidationError

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name']

class SpentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SpentForm, self).__init__(*args, **kwargs)

        if self.user and hasattr(self.instance, 'id') and self.instance.id:
            # Verifica se o objeto instance tem um atributo id válido
            self.fields['users_shared'].queryset = User.objects.exclude(id=self.user.id)
            self.fields['expense'].queryset = Expense.objects.filter(
                Q(user_create=self.user) |
                Q(spent__users_shared=self.user)
            ).distinct()

    def clean_users_shared(self):
        users_shared = self.cleaned_data.get('users_shared')
        if self.user in users_shared:
            raise ValidationError("Você não pode compartilhar com você mesmo.")
        return users_shared

    class Meta:
        model = Spent
        fields = ['value', 'description', 'date', 'expense', 'users_shared']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class ShareRequestForm(forms.ModelForm):
    class Meta:
        model = ShareRequest
        fields = '__all__'

class UserFilterForm(forms.Form):
    recebidas = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    enviadas = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, user, *args, **kwargs):
        super(UserFilterForm, self).__init__(*args, **kwargs)

        # Preenche a queryset do campo recebidas com os usuários apropriados
        spent_users_shared = Spent.objects.filter(users_shared=user, sharerequest__status='A')
        approved_users = ShareRequest.objects.filter(spent__in=spent_users_shared, user_approving=user, status='A', spent__users_shared=user)
        self.fields['recebidas'].queryset = User.objects.filter(Q(pk__in=approved_users.values('spent__user')))

        # Preenche a queryset do campo enviadas com os usuários apropriados
        my_spents_shared = Spent.objects.filter(user=user, sharerequest__status='A')
        approved_users = ShareRequest.objects.filter(spent__in=my_spents_shared, user_requesting=user, status='A', spent__users_shared__in=my_spents_shared.values('users_shared'))
        self.fields['enviadas'].queryset = User.objects.filter(Q(pk__in=approved_users.values('user_approving')))
