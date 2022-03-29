from django.shortcuts import render, HttpResponse
from datetime import datetime
from dashboard.models import AccountDetail
from dashboard.models import AccountDetailEnding
from django.contrib.messages import constants as messages

"""
General Account Detail Database = GADD
Account Ending Details Database = AEDD
"""

# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def chartofaccounts(request):
    print("Hello CoA's")
    dbitems = AccountDetahttpsilEnding.objects.all()
    context = {'dbnames':dbitems}
    return render(request,"chart.html",context)

def createchartaccount(request):
    print("Hello CCoA's")
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        typeA = request.POST.get('typeA')
        balance = request.POST.get('balance')
        debit = 0
        credit = 0
        
        #Code to check if the balance provided should be a debit or a credit.
        if((typeA == "fixed_asset") or (typeA == "current_asset") or (typeA == "expense")):
            debit = balance
        
        else:
            credit = balance

        #This saves the instance into the General Account Detail Database.
        account_details = AccountDetail(name = name, desc = desc, typeA = typeA, debit = debit, credit = credit, date = datetime.today(),balance = balance)
        account_details.save()
        
        #This creates a list of all Account Names in the GADD.
        accountsFinal = AccountDetailEnding.objects.all()
        names = []
        
        for account in accountsFinal:
            names.append(account.name)
        
        #If a given Account is being added for the first time, only then will it be inserted into the Account Ending Details Database.
        if account_details.name not in names:
            accountdetailsending = AccountDetailEnding(name = name, desc = desc, typeA = typeA, debit = debit, credit = credit, date = datetime.today(),balance = balance, transmade = False)
            accountdetailsending.save()
        
    return render(request,"chart_create.html")


def generaljournal(request):
    
    dbitems = AccountDetailEnding.objects.all()
    dbnames = []
        
    for account in dbitems:
        dbnames.append(account.name)
            
    print(dbitems)
    
    context = {'dbnames':dbnames}
    
    if request.method == "POST":
        
        count = 0
        isTrue = True
        
        try:
            while(isTrue):  
                name  = request.POST.get('name' + str(count))
                desc = request.POST.get('desc' + str(count))
                
                print(name, "is the account name with length ",len(name))
                
                # Searching for the Account in the AEDD so that we can retreive it's type, since the account being entered is already in the AEDD, and while making the entries from the general journal, you are not taking the type so you have to retrieve it.

                print("PRINTING")
                
                Obj = AccountDetailEnding.objects.filter(name = name)[0]
                if(Obj.transmade != 1):
                    AccountDetailEnding.objects.filter(name = name).update(transmade = 1)
                    
                print(Obj)
                #Retrieving the Account Type
                typeA = Obj.typeA
                print(name)
                balance = 0
                
                debit = request.POST.get('debit' + str(count))
                credit = request.POST.get('credit' + str(count))
                
                
                if(credit == ''):
                    credit = 0
                else:
                    debit = 0

                # Uploading the Account details to the GADD
                account_details = AccountDetail(name = name, desc = desc, typeA = typeA, debit = debit, credit = credit, date = datetime.today(),balance = balance)
                account_details.save()
                
                ObjBalance = Obj.balance
                
                if((typeA == "fixed_asset") or (typeA == "current_asset") or (typeA == "expense")):
                    if(credit != 0):
                        print("Executed 1.0")
                        ObjBalance = ObjBalance - int(credit)
                        print("Executed 1.1")
                        AccountDetailEnding.objects.filter(name = name).update(balance = ObjBalance)
                        print("Executed 1.2")
                    else:
                        print("Executed 2.0")
                        ObjBalance = ObjBalance + int(debit)
                        print("Executed 2.1")
                        AccountDetailEnding.objects.filter(name = name).update(balance = ObjBalance)
                        print("Executed 2.2")
                        
                else:
                    if(credit != 0):
                        print("Executed 3.0")
                        ObjBalance = ObjBalance + int(credit)
                        print("Executed 3.1")
                        AccountDetailEnding.objects.filter(name = name).update(balance = ObjBalance)
                        print("Executed 3.2")
                    else:
                        print("Executed 4.0")
                        ObjBalance = ObjBalance - int(debit)
                        print("Executed 4.1")
                        AccountDetailEnding.objects.filter(name = name).update(balance = ObjBalance)
                        print("Executed 4.2")
                    
                count = count + 1
        
        # Sets the isTrue to false so that the while loop stops when the number of entries end. Helps to avoid the DoesNotExist error which occurs when you let the count go out of range.
        except:
            isTrue = False
            
            
    return render(request,"general_j.html",context)

def ledger(request):
    dbnamesending = AccountDetailEnding.objects.all()
    dbnames = AccountDetail.objects.all()
         
    context = {'dbnamesending':dbnamesending,
                'dbnames':dbnames}
    
    return render(request,"ledgers.html",context)

def trialbalance(request):
    
    current_assets = AccountDetailEnding.objects.filter(typeA = "current_asset")
    fixed_assets = AccountDetailEnding.objects.filter(typeA = "fixed_asset")
    current_liabilities = AccountDetailEnding.objects.filter(typeA = "current_liability")
    noncurrent_liabilities = AccountDetailEnding.objects.filter(typeA = "noncurrent_liability")
    earned_revenues = AccountDetailEnding.objects.filter(typeA = "earned_revenue")
    unearned_revenues = AccountDetailEnding.objects.filter(typeA = "unearned_revenue")
    equitys = AccountDetailEnding.objects.filter(typeA = "equity")
    expenses = AccountDetailEnding.objects.filter(typeA = "expense")
    
    date = datetime.today()
    
    emptiness = False
    
    if((len(current_assets) == 0) and (len(fixed_assets) == 0) and (len(current_liabilities) == 0) and (len(noncurrent_liabilities) == 0) and (len(earned_revenues) == 0) and (len(unearned_revenues) == 0) and (len(equitys) == 0) and (len(expenses) == 0)):
        emptiness = True
        
    debitEndingBalance = 0
    creditEndingBalance = 0
    
    for account in AccountDetailEnding.objects.all():
        
        if ((account.typeA == "fixed_asset") or (account.typeA == "current_asset") or (account.typeA == "expense")):
            debitEndingBalance = debitEndingBalance + account.balance
        else:
            creditEndingBalance = creditEndingBalance + account.balance
            
        
    context = {
        'currentAssets':current_assets,
        'fixedAssets':fixed_assets,
        'currentLiabilities':current_liabilities,
        'noncurrentLiabilities':noncurrent_liabilities,
        'earnedRevenues':earned_revenues,
        'unearnedRevenues':unearned_revenues,
        'equitys': equitys,
        'expenses': expenses,
        'date':date,
        'emptiness':emptiness,
        'debitEnding':debitEndingBalance,
        'creditEnding':creditEndingBalance
    }
    
    return render(request,"trial_b.html",context)

def financialstatements(request):
    return render(request,"financial_s.html")

def balancesheet(request):
    return render(request,"balance_sheet.html")

def incomestatement(request):
    return render(request,"income_statement.html")
