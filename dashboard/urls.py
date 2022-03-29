from django.contrib import admin
from django.urls import path
from dashboard import views

urlpatterns = [
    path("",views.dashboard, name = 'dashboard'),
    path("chartofaccounts",views.chartofaccounts, name = 'chartofaccounts'),
    path("createchartaccount",views.createchartaccount, name = "createchartaccount"),
    path("generaljournal",views.generaljournal, name = 'generaljournal'),
    path("ledger",views.ledger, name = "ledger"),
    path("trialbalance",views.trialbalance, name = "trialbalance"),
    path("financialstatements",views.financialstatements, name = "financialstatements"),
    path("balancesheet",views.balancesheet, name = "balancesheet"),
    path("incomestatement",views.incomestatement, name = "incomestatement")
]
