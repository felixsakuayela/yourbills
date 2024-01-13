from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import Expense, Spent, ShareRequest

@admin.register(Expense)
class ExpenseAdmin(VersionAdmin):
    pass

@admin.register(Spent)
class SpentAdmin(VersionAdmin):
    pass

@admin.register(ShareRequest)
class ShareRequestAdmin(VersionAdmin):
    pass
