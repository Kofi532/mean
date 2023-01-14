
# Create your views here.
from django.shortcuts import render
import openpyxl
from uploading.models import fees_update
import pandas as pd
from django.utils import timezone
from datetime import date
from users.models import use, sch_reg, act, class_fee, classn
from operator import add
from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel
from itertools import islice
import os
from django.core.files.storage import FileSystemStorage
import numpy as np 
import itertools
import math
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request,'logout.html', {})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

def delete_std(request):
    username = None
    usernamed = request.user.username
    df = pd.DataFrame(sch_reg.objects.all().values())
    if usernamed in list(df['username']):
        #df = pd.DataFrame(use.objects.all().values())
        df = pd.DataFrame(sch_reg.objects.all().values())
        df = df.drop('id', axis=1)
        df = df[df['username'] == usernamed]
        ffs = list(df['full_sch'])
        schf = ffs[0]
        ff = list(df['school'])
        sch = ff[0]
        ffc = list(df['contact_details'])
        schc = ffc[0] 
        active = use.objects.all().values().filter(school = sch) 
        cfees = class_fee.objects.all().values().filter(school = sch) 
        skuul =  pd.DataFrame(fees_update.objects.all().values().filter(school = sch))
        z= list(skuul['stu_id'])
        if request.method == 'POST':
            student = request.POST.get('student')
            fees_update.objects.filter(stu_id=student).delete()
            return render(request, 'thanks.html', {'z': z})
    return render(request, 'deletestd.html', {'z': z})



@login_required(login_url='/login/')
def index(request):
    username = None
    usernamed = request.user.username 
    dfs = pd.DataFrame(use.objects.all().values())
    dkb = dfs.copy()
    if list(dkb) == []:
        lis1 = ['nil']
    else:
        lis1 = list(dkb['username'])
    dfs = pd.DataFrame(sch_reg.objects.all().values())
    if list(dfs) == []:
        lis2 = ['nil']
    else:
        lis2 = list(dfs['username'])
    lil = lis1 + lis2
    if usernamed in lil:       
        if "GET" == request.method:
            username = None
            usernamed = request.user.username 
            dfs = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
            dkb = dfs.copy()
            if list(dfs) == []:
                dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
            full_sch = list(dfs['full_sch'])
            full_sch = full_sch[0]
            code = list(dfs['school'])
            code = code[0]
            df_act = pd.DataFrame(act.objects.all().values().filter(school = code))
            if list(df_act) == []:
                term = ''
            else:
                term = list(df_act['active_term']) 
                term = term[0]
            return render(request, 'upload.html', {'full_sch': full_sch, 'term': term})
        else:
            excel_file = request.FILES["excel_file"]

            # you may put validations here to check extension or file size

            wb = openpyxl.load_workbook(excel_file)
            username = None
            usernamed = request.user.username 
            dfs = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
            dkb = dfs.copy()
            if list(dfs) == []:
                dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
            code = list(dfs['school'])
            code = code[0]
            df_act = pd.DataFrame(act.objects.all().values().filter(school = code))
            term = list(df_act['active_term']) 
            term = term[0]
            skuul =  pd.DataFrame(classn.objects.all().values().filter(school = code))
            com = ['classA', 'classB', 'classC', 'classD', 'classE', 'classF', 'classG', 'classH','classI','classJ', 'classK', 'classL', 'classM', 'classN', 'classO']
            skuul = skuul[com]
            ree = list(skuul.iloc[0])
            ree = [x for x in ree if x != '0']
            ree = [x for x in ree if x != None]

            #ree = ['Nursery2']
            for i in ree:
            #"Class 1NewAdm"
                
                worksheet = wb[i+'NewAdm']
                data = worksheet.values
                cols = next(data)[1:]
                data = list(data)
                idx = [r[0] for r in data]
                data = (islice(r, 1, None) for r in data)
                df = pd.DataFrame(data, index=idx, columns=cols)
                username = None
                username = request.user.username 
                dfs = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
                if list(dfs) == []:
                    dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
                dfsr = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
                ffr = list(dfsr['school'])
                ffs = list(dfsr['full_sch'])
                fullsch = ffs[0]
                schr = ffr[0]
                ff = list(dfs['school'])
                sch = ff[0]
                claz_df = pd.DataFrame(class_fee.objects.all().values().filter(school = sch).filter(classes =i))
                if list(claz_df) == []:
                    clazfee = 0
                else:
                    claz_df = list(claz_df['fee'])
                    clazfee = claz_df[0]
                df['middlename'] = df['middlename'].fillna('None')
                df['mother_name'] = df['mother_name'].fillna('None')
                df['father_name'] = df['father_name'].fillna('None')
                df['mother_contact'] = df['mother_contact'].fillna('None')
                df['father_contact'] = df['father_contact'].fillna('None')
                df['datey'] = date.today()
                #df['school'] = sch
                df['school_name'] = fullsch
                df['school'] = schr
                df['level'] = i
                df['numbering'] = np.arange(len(df))
                df['number'] = df['numbering']
                df['fee'] = clazfee
                dfp = pd.DataFrame(fees_update.objects.all().values().filter(school = schr).filter(level = i))
                if list(dfp) == []:
                    dfp = pd.DataFrame({'stu_id': pd.Series(dtype='str'),
                        'firstname': pd.Series(dtype='str'),
                        'lastname': pd.Series(dtype='str'),
                        'level': pd.Series(dtype='str'),
                        'amount': pd.Series(dtype='float'),
                        'fee': pd.Series(dtype='float'),
                        'balance': pd.Series(dtype='float'),
                        'school': pd.Series(dtype='str'),
                        'school_name': pd.Series(dtype='str'),
                        'datey': pd.Series(dtype='str')})
    #['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount','amountpaid_term1', 'amountpaid_term2', 'amountpaid_term3','fee', 'balance', 'school', 'datey', 'school_full', 'mother_name', 'mother_contact', 'father_name', 'father_contact']
                else:
                    dfp = dfp.copy()
                    dfp = dfp.drop('id', axis=1)
                if len(dfp['stu_id']) == 0:
                    leng = 1
                else:
                    dfp['new'] = dfp["stu_id"].str.split("-", n = 1, expand = False)
                    leng = list(dfp['new'])
                    leng = [item[1] for item in leng]
                    leng = [float(i) for i in leng]
                    leng = max(leng)+1
                    leng = math.trunc(leng)
            # leng = len(list(dfp['stu_id']))+ 1
                df['numbering'] = df['numbering']+leng
                my_list = list(df['numbering'])
                my_list = [str(x) for x in my_list]
                inn = i
                df['stu_id'] = [inn+'S'+schr+'-' +x  for x in my_list]
                df['amount'] = 0
                df['balance'] = df['fee'] - df['amount']
                df['level'] = i
                df['school_full'] = fullsch
    #['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount','amountpaid_term1', 'amountpaid_term2', 'amountpaid_term3','fee', 'balance', 'school', 'datey', 'school_full', 'mother_name', 'mother_contact', 'father_name', 'father_contact']
                com = ['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school','school_name', 'datey', 'school_full', 'mother_name', 'mother_contact', 'father_name', 'father_contact']
                df = df[com]
                df = df.dropna()
                for index, row in df.iterrows():
                    model = fees_update()
                    model.stu_id = row['stu_id']
                    model.firstname = row['firstname']
                    model.middlename = row['middlename']
                    model.lastname = row['lastname']
                    model.level = row['level']
                    model.amount = row['amount']
                    model.fee = row['fee']
                    model.balance = row['balance']
                    model.school = row['school']
                    model.school_full = row['school_name']
                    model.datey = row['datey']
                    model.mother_name = row['mother_name']
                    model.father_name = row['father_name']
                    model.mother_contact = row['mother_contact']
                    model.father_contact = row['father_contact']
                    model.save()
    #        return render(request, 'upload.html', {})
        
            for ii in ree:
                worksheet = wb[ii]
                data = worksheet.values
                cols = next(data)[1:]
                data = list(data)
                idx = [r[0] for r in data]
                data = (islice(r, 1, None) for r in data)
                df = pd.DataFrame(data, index=idx, columns=cols)
                username = None
                username = request.user.username 
                dfs = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
                if list(dfs) == []:
                    dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
                ff = list(dfs['school'])
                sch = ff[0]
                claz_df = pd.DataFrame(class_fee.objects.all().values().filter(school = sch).filter(classes =ii))
                if list(claz_df) == []:
                    clazfee = 0
                else:
                    claz_df = list(claz_df['fee'])
                    clazfee = claz_df[0]
                df['middlename'] = df['middlename'].fillna('None')
                df['datey'] = date.today()
                df['school'] = schr
                df['level'] = ii
                df['fee'] = clazfee
        #['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school', 'datey']
            # com = ['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school', 'amount', 'datey']
            # df.columns = com
                #df = df[com]
                df = df.dropna()
                liss = list(df['stu_id'])
                lis = list(set(liss))
                dfp = pd.DataFrame(fees_update.objects.all().values().filter(school = schr))
                if list(dfp) == []:
                    dfp = pd.DataFrame({'stu_id': pd.Series(dtype='str'),
                        'firstname': pd.Series(dtype='str'),
                        'lastname': pd.Series(dtype='str'),
                        'level': pd.Series(dtype='str'),
                        'amount': pd.Series(dtype='float'),
                        'fee': pd.Series(dtype='float'),
                        'balance': pd.Series(dtype='float'),
                        'school': pd.Series(dtype='str'),
                        'datey': pd.Series(dtype='str'),
                        'amountpaid_term1': pd.Series(dtype='float'),
                        'amountpaid_term2': pd.Series(dtype='float'),
                        'amountpaid_term3': pd.Series(dtype='float'),
                        })
                else:
                    dfp = dfp.copy()
                    dfp = dfp.drop('id', axis=1)
                dff = dfp.loc[dfp['stu_id'].isin(lis)]
                dff_list = list(dff['amountpaid_'+term]) #amountpaid-term1
                df_list = list(df['amount'])
                wix = list(df['stu_id'])
                df['newamount'] = list(map(add, dff_list, df_list))
                if term == 'term1':
                    df['balance'] = df['fee'] - df['newamount']
                if term == 'term2':
                    df['balance'] = 2*(df['fee']) - df['newamount'] - df['amountpaid_term1']
                if term == 'term3':
                    df['balance'] = 3*(df['fee']) - df['newamount'] - df['amountpaid_term1'] - df['amountpaid_term2']
        #       df['balance'] = df['fee'] - df['newamount']
                df['middlename'] = df['middlename'].fillna('None')
                df['datey'] = date.today()
                df['school'] = schr   
                df['level'] = ii
                df['fee'] = clazfee
                if term == 'term1':
                    df['amountpaid_term1'] = list(df['newamount'])
                    df['amountpaid_term2'] = list(dff['amountpaid_term2'])
                    df['amountpaid_term3'] = list(dff['amountpaid_term3'])
                if term == 'term2':               
                    df['amountpaid_term1'] = list(dff['amountpaid_term1'])
                    df['amountpaid_term2'] = list(df['newamount'])
                    df['amountpaid_term3'] = list(dff['amountpaid_term3'])
                if term == 'term3':
                    df['amountpaid_term1'] = list(dff['amountpaid_term1'])
                    df['amountpaid_term2'] = list(df['amountpaid_term2'])
                    df['amountpaid_term3'] = list(df['newamount'])
                list2 = list(df['stu_id'])
                newamn = list(df['newamount'])##
                bal = list(df['balance'])
                dat = list(df['datey'])
                am1 = list(df['amountpaid_term1'])
                am2 = list(df['amountpaid_term2'])
                am3 = list(df['amountpaid_term3'])
                fee = list(df['fee'])
                for a,b,c,d,e,f,g,h in zip(list2, newamn, bal, dat, am1, am2, am3, fee):
                    fees_update.objects.filter(stu_id=a).update(amount=b, balance=c, datey=d, amountpaid_term1=e, amountpaid_term2=f, amountpaid_term3=g, fee=h)
            return render(request, 'thanks.html', {})
    else:
        return render(request, 'registersch.html', {})
    #return render(request, 'upload.html', {})

            # for i in list2:
            #     fees_update.objects.all().filter(school = schr).filter(stu_id = i).delete()
            # for index, row in df.iterrows():
            #     model = fees_update()
            #     if term == 'term1':
            #         model.amountpaid_term1 = row['newamount']
            #         model.amountpaid_term2 = row['amountpaid_term2']
            #         model.amountpaid_term3 = row['amountpaid_term3']
            #     if term == 'term2':
            #         model.amountpaid_term2 = row['newamount']
            #         model.amountpaid_term1 = row['amountpaid_term1']
            #         model.amountpaid_term3 = row['amountpaid_term3']
            #     if term == 'term3':
            #         model.amountpaid_term3 = row['newamount']
            #         model.amountpaid_term1 = row['amountpaid_term2']
            #         model.amountpaid_term3 = row['amountpaid_term3']                    
            #     model.stu_id = row['stu_id']
            #     model.firstname = row['firstname']
            #     model.middlename = row['middlename']
            #     model.lastname = row['lastname']
            #     model.level = row['level']
            #     model.fee = row['fee']
            #     model.balance = row['balance']
            #     model.school = row['school']
            #     model.datey = row['datey']
            #     model.save()

def fetch(request):
    username = None
    usernamed = request.user.username 
    dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed ))
    if usernamed in list(dfs['username']):
        ff = list(dfs['school'])
        sch = ff[0]
        df = pd.DataFrame(fees_update.objects.all().values().filter(school = sch))
        skuul =  pd.DataFrame(classn.objects.all().values().filter(school = sch))
        com = ['classA', 'classB', 'classC', 'classD', 'classE', 'classF', 'classG', 'classH','classI','classJ', 'classK', 'classL', 'classM', 'classN', 'classO']
        skuul = skuul[com]
        ree = list(skuul.iloc[0])
        ree = [x for x in ree if x != '0']
        ree = [x for x in ree if x != None]

        #ree = ['Creche','K.G1', 'K.G2', 'Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']
        #ree = ['Creche', 'K.G1']
        for z in ree:
            dft = pd.DataFrame(fees_update.objects.all().values().filter(school = sch).filter(level = z).filter(promote = 1))
            if list(dft) == []:
                move = 1
            else:
                filt = list(dft['stu_id'])
                prom_id = list(dft['stu_id'])
                position = ree.index(z)
                pos1 = ree[position]
                if pos1 == ree[-1]:
                    #pos2 = ree[0]
                    pos2 = 'graduate'
                else:
                    pos2 = ree[position+1]
                prom_id = [(x.replace(z ,pos2)) for x in prom_id]
                dft['stu_id'] = prom_id
                dft['level'] = pos2
                dft['promote'] = 0
                dft.dropna()
                schz = list(dft['school_full'])
                first = list(dft['firstname'])
                middle = list(dft['middlename'])
                last = list(dft['lastname'])
                skuul = list(dft['school'])
                levv = list(dft['level'])
                ppp = list(dft['promote'])
                
                for a,b,c,d,e,f,g,h,j in zip(schz,first,middle,last, prom_id, filt, skuul, levv, ppp):##       
                # fees_update.objects.filter(stu_id=f).update(school = g, school_full = a , stu_id = e, firstname = c, middlename = c, lastname = d, level = h, promote = j)
                    new_entry = fees_update(school = g, school_full = a , stu_id = e, firstname = b, middlename = c, lastname = d, level = h, promote = j)
                    new_entry.save()
        fees_update.objects.filter(school = sch).filter(promote = 1).delete()
        dfb = pd.DataFrame(fees_update.objects.all().values().filter(school = sch))
        stu_ring = list(dfb['stu_id'])
        dfb['promote'] = 1
        pr_ring = list(dfb['promote'])
        for a,b in zip(stu_ring, pr_ring):
            fees_update.objects.filter(school = sch).filter(stu_id = a).update(promote = b)
        return render(request, 'fetch.html')
    else:
        return render(request, 'unauth.html')
#['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount','amountpaid_term1', 'amountpaid_term2', 'amountpaid_term3','fee', 'balance', 'school', 'datey']
