from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import redirect, render

import requests
from django.contrib.humanize.templatetags.humanize import intcomma

from .models import *
from django.http import HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.paginator import *
from django.views.decorators.csrf import csrf_exempt
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Create your views here.
@csrf_exempt
def superadminLogin(request):
   errorMessage=''
   if request.method=="POST":

      id=request.POST.get('applicationid')
      passw=request.POST.get('password')
     
      if passw==settings.SUPERADMIN_PASSWORD and id==settings.SUPERADMIN_USERNAME:
         
         request.session['LoginAccess']=True
         if request.session.get('indexPage'): return redirect('dashBoardIndexpage')
         

         return redirect(request.session.get('responseUrl'))
      else:
        errorMessage="Wrong Credentials"

   return render(request,'Login.html',{'errorMessage':errorMessage})

def logOut(request):
   request.session.clear()
   return redirect('Login')
def dsaDashBoard(request):
    return render(request,"Dashboard.html")

def dsamanualId(request):

    request.session['franchCode']=settings.SUPERADMIN_FRANCHISECODE
    request.session['refCode']=settings.SUPERADMIN_REFCODE
    return request.session.get('refCode')


# ApplyForms.................................................................

def apply_business(request):
    return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/bl/demo",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})
def apply_Education(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/el/apply-educationalLoan",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})
def home_loan(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/home/",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})
def credit_card(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cc/credit/",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})
def car_loan(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cl/car-loan-application/",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})
def lap(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/lapapply/",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})
def apply_personal(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/personal/",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})
def apply_gold(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/goldloan/",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})
def apply_otherLoan(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/otherloan/",'dsaId':dsamanualId(request),'currentUrl':f'{settings.FRANCHISE_URL}','sourceUrl':f"{settings.SOURCE_PROJECT_URL}"})


# Insurance..........................................
def lifeInsurance(request):
   return render(request,"Lifeinsurance.html",{'url':f"{settings.SOURCE_PROJECT_URL}"})

def generalInsurance(request):
   return render(request,"GeneralInsurance.html",{'url':f"{settings.SOURCE_PROJECT_URL}"})

def healthInsurance(request):
   return render(request,"HealthInsurance.html",{'url':f"{settings.SOURCE_PROJECT_URL}"})

def allInsurance(request):
   return render(request,"AllInsurance.html",{'url':f"{settings.SOURCE_PROJECT_URL}"})

# Insurance............................................



# CheckEligibility.....................
def educheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/el/edubasicdetail/"})

def busicheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/bl/busbasicdetail/"})

def lapcheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/basicdetail/"})

def homecheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/homebasicdetail/"})

def personalcheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/perbasicdetail/"})

def carcheckEligible(request):

   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cl/carbasic-details/"})

def creditcheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cc/crebasicdetail/"})

def goldcheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/goldbasicdetail/"})

def othercheckEligible(request):
   return render(request,"checkEligible.html",{'url':f"{settings.SOURCE_PROJECT_URL}/otherbasicdetail/"})




# CheckEligibility.....................


def AllLoansCount(refCode,date=None):

  if not date:

   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_Frloan_refCode_LoansCount/')
  else:

   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_Frloan_refCode_LoansCount/?date={date}')
  if response.status_code==200:

      return response.json()

def AllApprovedLoansCount(refCode,date=None):
  if not date:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_Frloan_refCode_ApprovedCount/')
  else:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_Frloan_refCode_ApprovedCount/?date={date}')
  if response.status_code==200:
      return response.json()

def AllRejectedLoansCount(refCode,date=None):
  if not date:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_Frloan_refCode_RejectedCount/')
  else:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_Frloan_refCode_RejectedCount/?date={date}')

  if response.status_code==200:
     
      return response.json()
   
   
# All DSA & Loans Count Loans Count.........................
def AllDsaSalesLoansCount(refCode,date=None):

  if not date:

   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_LoansCount/')
  else:

   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_LoansCount/?date={date}')
  if response.status_code==200:

      return response.json()

def AllDsaSalesApprovedLoansCount(refCode,date=None):
  if not date:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_ApprovedCount/')
  else:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_ApprovedCount/?date={date}')
  if response.status_code==200:
      return response.json()

def AllDsaSalesRejectedLoansCount(refCode,date=None):
  if not date:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_RejectedCount/')
  else:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_RejectedCount/?date={date}')

  if response.status_code==200:
     
      return response.json()
   
   
   

  

# Credit Card........................
def credit_Loans_Count(request,refCode):

   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/credit_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   

def credit_FranLoans_Count(request,refCode):

   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/credit_loan_FranCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}

 
def allTotalDSADisbursedAmountCalculator(request,date=None,ids=None):
   if ids:
    resu=[i.get('dsa_registerid') for i in ids]
    if not date:
     response=requests.post(f'{settings.ACCOUNTS_SOURCE_URL}/DisburseViewsets/calculateAllDisbursementAmountUsingIds/',json={'ids':resu})
    else:
       response=requests.post(f'{settings.ACCOUNTS_SOURCE_URL}/DisburseViewsets/calculateAllDisbursementAmountUsingIds/',json={'ids':resu,'date':date})
    
   #  if request.session.get('strtSum'):
    request.session['sumofAllTotalDisbursamountdsa']=intcomma(sum(response.json()))
    return response.json()
   return []


def allTotalFranchiseDisbursedAmountCalculator(request,date=None,ids=None):
   # ids=getAllDsaIds(request,franchCode)

   if ids:
    resu=[i.get('franchise_id') for i in ids]
    if not date:
     response=requests.post(f'{settings.ACCOUNTS_SOURCE_URL}/DisburseViewsets/calculateAllFranchiseDisbursementAmountUsingIds/',json={'ids':resu})
    else:
       response=requests.post(f'{settings.ACCOUNTS_SOURCE_URL}/DisburseViewsets/calculateAllFranchiseDisbursementAmountUsingIds/',json={'ids':resu,'date':date})
    
   #  if request.session.get('strtSum'):
    request.session['sumofAllTotalDisbursamountdsa']=intcomma(sum(response.json()))
    return response.json()
   return []


def allTotalFranchiseAmountCalculator(request,date=None,ids=None):
   if ids:
    resu=[i.get('franchise_id') for i in ids]
    if not date:
      
     response=requests.post(f'{settings.ACCOUNTS_SOURCE_URL}/DisburseViewsets/calculateAllFranchiseClosedAmountUsingIds/',json={'ids':resu})
    else:
       response=requests.post(f'{settings.ACCOUNTS_SOURCE_URL}/DisburseViewsets/calculateAllFranchiseClosedAmountUsingIds/',json={'ids':resu,'date':date})
    
   #  if request.session.get('strtSum'):
    request.session['sumofAllAmount']=intcomma(sum(response.json()))

    return response.json()
   return []



#Dsa IDS......................................
def getAllDsaIds(request,franchiseCode=None):

   res=requests.get(f'{settings.HR_SOURCE_URL}/api/mymodel/giveAllDSAIds/')
   if res.status_code==200:


      return res.json()
   else:return []
   
#    return res.json() if res.status_code==200 else return None
#Dsa IDS.................................... 





#Sales IDS......................................
def getAllSalesIDS(request,franchiseCode=None):

   res=requests.get(f'{settings.HR_SOURCE_URL}/api/mymodel/giveAllSALESIds/')
   if res.status_code==200:


      return res.json()
   else:return []
#Sales IDS.................................... 
 


#Frachise IDS......................................
def getAllFranchiseIDS(request,franchiseCode=None):

   res=requests.get(f'{settings.HR_SOURCE_URL}/api/mymodel/giveAllFranchiseIds/')
   if res.status_code==200:


      return res.json()
   else:return []
#Frachise IDS.................................... 



#All DSA History Data...............................
def franchiseTotalLoansCount(request,franchiseCode=None,date=None,franchiseTotalAmountDate=None):


   dsaIds=getAllFranchiseIDS(request,franchiseCode)
   if not dsaIds:

      return []
   listData=[]

   with ThreadPoolExecutor() as executor:
       thread1=executor.submit(allTotalFranchiseDisbursedAmountCalculator,request,date,dsaIds)
      #  Calculating total franchises amounts including sales,dsa's.........
       thread2=executor.submit(allTotalFranchiseAmountCalculator,request,franchiseTotalAmountDate,dsaIds)
       
   disbursedAmount=thread1.result()
   franchiseAmounts=thread2.result()


   
   
   with ThreadPoolExecutor() as executor:
      franchiseFunctionResult=executor.submit(franchiseTotalAmountCalculateFunction,request,dsaIds,franchiseAmounts)
      
      
      for i,j in zip(dsaIds,disbursedAmount):
     
        totalLoansCountedVal=executor.submit(AllLoansCount,i.get('franchise_id'),date)
        totalresult=totalLoansCountedVal.result()
        
        totalAppreovedLoans=executor.submit(AllApprovedLoansCount,i.get('franchise_id'),date)
        totalApprovedresult=totalAppreovedLoans.result()
        
        totalRejectedLoans=executor.submit(AllRejectedLoansCount,i.get('franchise_id'),date)
        totalRejectedresult=totalRejectedLoans.result()
        
      
         
         # Credit Card...............
      #   creditTotalLoansThread1 = executor.submit(credit_FranLoans_Count, request,i.get('franchise_id'))
      #   ccCount=creditTotalLoansThread1.result()
        
        
      #   Note otherLoans,GoldLoans No pending Loans Calculated..................
        totalPendingLoans=totalresult.get('totalcount')-(totalApprovedresult.get('totalApprovedcount')+totalRejectedresult.get('totrejectedcount'))
        totalPendingLoans=totalPendingLoans-(totalresult.get('goldcount')+totalresult.get('othercount'))
        
        
        
        data={
           'registerId':i.get('franchise_id'),
        #    'franchiseId':i.get('franchiseCode'),
           'totalLoans':totalresult.get('totalcount'),
           'businesscount':totalresult.get('buscount'),
           'educationcount':totalresult.get('educount'),
           'lapcount':totalresult.get('lapcount'),
           'personalcount':totalresult.get('percount'),
           'homecount':totalresult.get('homecount'),
           'carcount':totalresult.get('carcount'),
           'goldcount':totalresult.get('goldcount'),
           'othercount':totalresult.get('othercount'),
           
           
           
           'approvedloans':totalApprovedresult.get('totalApprovedcount'),
           'businessapprovedcount':totalApprovedresult.get('busapprovedcount'),
           'educationapprovedcount':totalApprovedresult.get('eduapprovedcount'),
           'lapapprovedcount':totalApprovedresult.get('lapapprovedcount'),
            'personalapprovedcount':totalApprovedresult.get('perapprovedcount'),
             'homeapprovedcount':totalApprovedresult.get('homeapprovedcount'),
              'carapprovedcount':totalApprovedresult.get('carapprovedcount'),
           
           'rejectedLoans':totalRejectedresult.get('totrejectedcount'),
           'businessrejectedcount':totalRejectedresult.get('busrejectedcount'),
           'educationrejectedcount':totalRejectedresult.get('edurejectedcount'),
           'laprejectedcount':totalRejectedresult.get('laprejectedcount'),
           'personalrejectedcount':totalRejectedresult.get('perrejectedcount'),
           'homerejectedcount':totalRejectedresult.get('homerejectedcount'),
           'carrejectedcount':totalRejectedresult.get('carrejectedcount'),
           
           'pendingLoans':totalPendingLoans,
           'creditcardtotalloans':totalresult.get('creditcount'),
           
           'totalinsurance':totalresult.get('totalInsurances'),
           'allinsurance':totalresult.get('allinsurance'),
           'lifeinsurance':totalresult.get('lifeinsurance'),
           'generalinsurance':totalresult.get('generalinsurance'),
           'healthinsurance':totalresult.get('healthinsurance'),
           'TotaldisbursedAmount':intcomma(j),
           
        }
        listData.append(data)
           # a=[1,2,3]
         
   return [listData,franchiseFunctionResult.result()]

def franchiseTotalAmountCalculateFunction(request,dsaIds,franchiseAmounts):
   franchiseAmount=[]
   for i,j in zip(dsaIds,franchiseAmounts):
      

         res=requests.get(f"{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{i.get('franchise_id')}/All_TotlDSA_SalesFrloan_refCode_LoansCount/")
         if res.status_code==200:
            result=res.json()
            data={
            'registerId':i.get('franchise_id'),
            'TotalFranchiseAmount':intcomma(j),
            'TotalLoans':result.get('totalcount'),
            'TotalCC':result.get('creditcount'),
            'TotalInsurances':result.get('totalInsurances'),
          }
            franchiseAmount.append(data)   
   return franchiseAmount   


@csrf_exempt
def franchiseTrack(request):
   
   if request.GET.get('date'):
      request.session['date']=request.GET.get('date')
      
      
   if request.GET.get('fradate'):
      request.session['fradate']=request.GET.get('fradate')
   
   # when personal franchise date serach clicks removing entire franchise total amount sessions to give response fast
   if request.GET.get('applicationid'):
      if request.session.get('fradate'):
         del request.session['fradate']
   if request.GET.get('fraapplicationid'):
      if request.session.get('date'):
         del request.session['date']
         
   # when personal franchise pagination clicks removing entire franchise total amount session to give response fast
   if request.GET.get('page'):
      if request.session.get('fradate'):
         del request.session['fradate']
         
   if request.GET.get('pagecopy'):
      if request.session.get('date'):
         del request.session['date']
      
   
   if request.GET.get('showall'):
      if request.session.get('date'):
         del request.session['date']
   if request.GET.get('showfranchiseall'):
      if request.session.get('fradate'):
         del request.session['fradate']
      
      
   normalData,franchiseamountData=[],[]
   data=franchiseTotalLoansCount(request,request.session.get('franchCode'),request.session.get('date'))
   
   
   if not data:

      data=[[],[]]
   else:
      normalData=data[0]
      franchiseamountData=data[1]
         
   if request.session.get('date'):

      # allTotalDSADisbursedAmountCalculator(request,request.session.get('franchCode'),request.session.get('date'))
      # res=requests.get(f'{settings.FRANCHISE_URL}/franchise/api/totalLoansCount?franchiseCode={request.session.get('franchCode')}&date={request.session.get('date')}')
      data=franchiseTotalLoansCount(request,request.session.get('franchCode'),request.session.get('date'))
      # normalData=data[0]
      normalData=data[0] if data else [[],[]]
      # franchiseamountData=data[1]
      # if not data:
      #    data=[]
         
   if request.session.get('fradate'):

      data=franchiseTotalLoansCount(request,request.session.get('franchCode'),request.session.get('date'),request.session.get('fradate'))
      # franchiseamountData=data[1]
      # if not data:
      #    data = [[], []]
      franchiseamountData=data[1] if data else [[],[]]
         
   if request.GET.get('applicationid'):
      
      normalData=[i for i in data[0] if i['registerId'] == request.GET.get('applicationid')]
         
   
   if request.GET.get('fraapplicationid'):

         
      franchiseamountData=[i for i in data[1] if i['registerId'] == request.GET.get('fraapplicationid')]

   paginator = Paginator(normalData, 10)  
   page = request.GET.get('page') 
         
   try:
        objects = paginator.page(page)

   except PageNotAnInteger:
        objects = paginator.page(1)
   except EmptyPage:
        objects = paginator.page(1)
  
   start_index = (objects.number - 1) * paginator.per_page + 1
   

   paginatorCopy = Paginator(franchiseamountData, 10)
   pageCopy = request.GET.get('pagecopy')
         
   try:
        objectsCopy = paginatorCopy.page(pageCopy)

   except PageNotAnInteger:
        objectsCopy = paginatorCopy.page(1)
   except EmptyPage:
        objectsCopy = paginatorCopy.page(1)
  
   start_indexCopy = (objectsCopy.number - 1) * paginatorCopy.per_page + 1
   
   


   return render(request,'dsaTrack.html',{'objects':objects,'start_index':start_index,'sumofAllTotalDisbursamountdsa':request.session.get('sumofAllTotalDisbursamountdsa'),'fromFranchise':True,'sumofAllTotalAmount':request.session.get('sumofAllAmount'),'objectsCopy':objectsCopy,'start_indexCopy':start_indexCopy})

   




 #All DSA History Data...............................
def totalLoansCount(request,franchiseCode=None,date=None):
   dsaIds=getAllDsaIds(request,franchiseCode)
   if not dsaIds:

      return []
   listData=[]



   disbursedAmount=allTotalDSADisbursedAmountCalculator(request,date,dsaIds)

   
   with ThreadPoolExecutor() as executor:
      for i,j in zip(dsaIds,disbursedAmount):
     
        totalLoansCountedVal=executor.submit(AllDsaSalesLoansCount,i.get('dsa_registerid'),date)
        totalresult=totalLoansCountedVal.result()
        
        totalAppreovedLoans=executor.submit(AllDsaSalesApprovedLoansCount,i.get('dsa_registerid'),date)
        totalApprovedresult=totalAppreovedLoans.result()
        
        totalRejectedLoans=executor.submit(AllDsaSalesRejectedLoansCount,i.get('dsa_registerid'),date)
        totalRejectedresult=totalRejectedLoans.result()
        
      
         
         # Credit Card...............
      #   creditTotalLoansThread1 = executor.submit(credit_Loans_Count, request,i.get('dsa_registerid'))
      #   ccCount=creditTotalLoansThread1.result()

        
      
        #Calculation..............................
     
      #   Note otherLoans,GoldLoans No pending Loans Calculated..................
        totalPendingLoans=totalresult.get('totalcount')-(totalApprovedresult.get('totalApprovedcount')+totalRejectedresult.get('totrejectedcount'))
        totalPendingLoans=totalPendingLoans-(totalresult.get('goldcount')+totalresult.get('othercount'))
        
        
        
        data={
           'registerId':i.get('dsa_registerid'),
           'franchiseId':i.get('franchiseCode'),
           'totalLoans':totalresult.get('totalcount'),
           'businesscount':totalresult.get('buscount'),
           'educationcount':totalresult.get('educount'),
           'lapcount':totalresult.get('lapcount'),
           'personalcount':totalresult.get('percount'),
           'homecount':totalresult.get('homecount'),
           'carcount':totalresult.get('carcount'),
           'goldcount':totalresult.get('goldcount'),
           'othercount':totalresult.get('othercount'),
           
           
           
           'approvedloans':totalApprovedresult.get('totalApprovedcount'),
           'businessapprovedcount':totalApprovedresult.get('busapprovedcount'),
           'educationapprovedcount':totalApprovedresult.get('eduapprovedcount'),
           'lapapprovedcount':totalApprovedresult.get('lapapprovedcount'),
            'personalapprovedcount':totalApprovedresult.get('perapprovedcount'),
             'homeapprovedcount':totalApprovedresult.get('homeapprovedcount'),
              'carapprovedcount':totalApprovedresult.get('carapprovedcount'),
           
           'rejectedLoans':totalRejectedresult.get('totrejectedcount'),
           'businessrejectedcount':totalRejectedresult.get('busrejectedcount'),
           'educationrejectedcount':totalRejectedresult.get('edurejectedcount'),
           'laprejectedcount':totalRejectedresult.get('laprejectedcount'),
           'personalrejectedcount':totalRejectedresult.get('perrejectedcount'),
           'homerejectedcount':totalRejectedresult.get('homerejectedcount'),
           'carrejectedcount':totalRejectedresult.get('carrejectedcount'),
           
           'pendingLoans':totalPendingLoans,
           'creditcardtotalloans':totalresult.get('creditcount'),
           
           'totalinsurance':totalresult.get('totalInsurances'),
           'allinsurance':totalresult.get('allinsurance'),
           'lifeinsurance':totalresult.get('lifeinsurance'),
           'generalinsurance':totalresult.get('generalinsurance'),
           'healthinsurance':totalresult.get('healthinsurance'),
           'TotaldisbursedAmount':intcomma(j),
        }
        listData.append(data)
        
   
   
   # totalSumdisbursedAmount=sum(disbursedAmount)
   
   return listData
      #   future_education = executor.submit(educationLoanApi, request)



#DSA Tracking
@csrf_exempt
def dsaTrack(request):
  
   # showAll=None
   
   if request.GET.get('date'):
      request.session['date']=request.GET.get('date')
      if request.session.get('DSAApplicationID'):
         del request.session['DSAApplicationID']
      
   if request.GET.get('showall'):
      # showAll=True
      if request.session.get('date'):
         del request.session['date']
      
      if request.session.get('DSAApplicationID'):
         del request.session['DSAApplicationID']
      
      
#    if request.GET.get('page'):pagenum=request.GET.get('page')
#    else: pagenum=1
   
#    pagenum=request.GET.get('page',1)
   
      

   # res=requests.get(f'{settings.FRANCHISE_URL}/franchise/api/totalLoansCount?franchiseCode={request.session.get('franchCode')}')
   data=totalLoansCount(request,request.session.get('franchCode'),request.session.get('date'))
   # allTotalDSADisbursedAmountCalculator(request,request.session.get('franchCode'))

   if not data:
      data=[]
   # paginator = Paginator(res.json(), 1)

   
   
   
   
         
   

   storeFranchRecords=[]
   
   if request.GET.get('applicationid'):
      request.session['DSAApplicationID']=request.GET.get('applicationid')
      if request.session.get('date'):
         del request.session['date']
      
      
   if request.session.get('DSAApplicationID'):

      # data=res.json()

      if request.session.get('DSAApplicationID').startswith("SLNDSA"):
       for i in data:
         if i['registerId']==request.session.get('DSAApplicationID'):
            data=[i]
            break;
      else:

        for i in data:
         if i['franchiseId']==request.session.get('DSAApplicationID'):
            storeFranchRecords.append(i)
        data=storeFranchRecords
            
   if request.session.get('date'):
      

      data=totalLoansCount(request,request.session.get('franchCode'),request.session.get('date'))
      if not data:
         data=[]
         
      
   # if data:
   paginator = Paginator(data, 10)  
   page = request.GET.get('page') 
         
   try:
        objects = paginator.page(page)

   except PageNotAnInteger:
        objects = paginator.page(1)
   except EmptyPage:
        objects = paginator.page(1)
  
   start_index = (objects.number - 1) * paginator.per_page + 1


   # if not request.session.get('sumofAllTotalDisbursamountdsa'):
   # request.session['strtSum']=True
  
   # del request.session['strtSum']
   
   
   return render(request,'dsaTrack.html',{'objects':objects,'start_index':start_index,'sumofAllTotalDisbursamountdsa':request.session.get('sumofAllTotalDisbursamountdsa')})





def allTotalSALESDisbursedAmountCalculator(request,date=None,ids=None):
   # ids=getAllSalesIDS(request,franchCode)

   if ids:
    resu=[i.get('registerid') for i in ids]
    if not date:
     response=requests.post(f'{settings.ACCOUNTS_SOURCE_URL}/DisburseViewsets/calculateAllDisbursementAmountUsingIds/',json={'ids':resu})
    else:
       response=requests.post(f'{settings.ACCOUNTS_SOURCE_URL}/DisburseViewsets/calculateAllDisbursementAmountUsingIds/',json={'ids':resu,'date':date})
    
   #  if request.session.get('strtSum'):
    request.session['sumofAllTotalDisbursamountdsa']=intcomma(sum(response.json()))
    return response.json()
   return []

 
 #All Sales History Data...............................
def SalestotalLoansCount(request,franchise=None,date=None):


   dsaIds=getAllSalesIDS(request,franchise)

   if not dsaIds: return []
   listData=[]
   
   dsaIds=[sale for sale in dsaIds if sale.get('registerid')!=None]
   disbursedAmount=allTotalSALESDisbursedAmountCalculator(request,date,dsaIds)
   
   
   with ThreadPoolExecutor() as executor:
      for i,j in zip(dsaIds,disbursedAmount):

         
      
        totalLoansCountedVal=executor.submit(AllDsaSalesLoansCount,i.get('registerid'),date)
        totalresult=totalLoansCountedVal.result()
        
        totalAppreovedLoans=executor.submit(AllDsaSalesApprovedLoansCount,i.get('registerid'),date)
        totalApprovedresult=totalAppreovedLoans.result()
        
        totalRejectedLoans=executor.submit(AllDsaSalesRejectedLoansCount,i.get('registerid'),date)
        totalRejectedresult=totalRejectedLoans.result()
        
      
         
         # Credit Card...............
      #   creditTotalLoansThread1 = executor.submit(credit_Loans_Count, request,i.get('registerid'))
      #   ccCount=creditTotalLoansThread1.result()
        
      #   Note otherLoans,GoldLoans No pending Loans Calculated..................
        totalPendingLoans=totalresult.get('totalcount')-(totalApprovedresult.get('totalApprovedcount')+totalRejectedresult.get('totrejectedcount'))
        totalPendingLoans=totalPendingLoans-(totalresult.get('goldcount')+totalresult.get('othercount'))
       
        
        
        
        data={
           'registerId':i.get('registerid'),
           'franchiseId':i.get('franchiseCode'),
           'totalLoans':totalresult.get('totalcount'),
           'businesscount':totalresult.get('buscount'),
           'educationcount':totalresult.get('educount'),
           'lapcount':totalresult.get('lapcount'),
           'personalcount':totalresult.get('percount'),
           'homecount':totalresult.get('homecount'),
           'carcount':totalresult.get('carcount'),
           'goldcount':totalresult.get('goldcount'),
           'othercount':totalresult.get('othercount'),
           
           
           
           'approvedloans':totalApprovedresult.get('totalApprovedcount'),
           'businessapprovedcount':totalApprovedresult.get('busapprovedcount'),
           'educationapprovedcount':totalApprovedresult.get('eduapprovedcount'),
           'lapapprovedcount':totalApprovedresult.get('lapapprovedcount'),
            'personalapprovedcount':totalApprovedresult.get('perapprovedcount'),
             'homeapprovedcount':totalApprovedresult.get('homeapprovedcount'),
              'carapprovedcount':totalApprovedresult.get('carapprovedcount'),
           
           'rejectedLoans':totalRejectedresult.get('totrejectedcount'),
           'businessrejectedcount':totalRejectedresult.get('busrejectedcount'),
           'educationrejectedcount':totalRejectedresult.get('edurejectedcount'),
           'laprejectedcount':totalRejectedresult.get('laprejectedcount'),
           'personalrejectedcount':totalRejectedresult.get('perrejectedcount'),
           'homerejectedcount':totalRejectedresult.get('homerejectedcount'),
           'carrejectedcount':totalRejectedresult.get('carrejectedcount'),
           
           'pendingLoans':totalPendingLoans,
           'creditcardtotalloans':totalresult.get('creditcount'),
           
           'totalinsurance':totalresult.get('totalInsurances'),
           'allinsurance':totalresult.get('allinsurance'),
           'lifeinsurance':totalresult.get('lifeinsurance'),
           'generalinsurance':totalresult.get('generalinsurance'),
           'healthinsurance':totalresult.get('healthinsurance'),
           'TotaldisbursedAmount':intcomma(j),
        }
        listData.append(data)
   return listData
      



#DSA Tracking
@csrf_exempt
def salesTrack(request):
   # showAll=None
   
   if request.GET.get('date'):
      request.session['date4']=request.GET.get('date')
      if request.session.get('salesapplicationid'):
         del request.session['salesapplicationid']
      
   if request.GET.get('showall'):
      # showAll=True
      if request.session.get('date4'):
         del request.session['date4']
         
      if request.session.get('salesapplicationid'):
         del request.session['salesapplicationid']
      
      

   # res=requests.get(f'{settings.FRANCHISE_URL}/franchise/api/SalestotalLoansCount?franchiseCode={request.session.get('franchCode')}')

   # data=request.session.get('franchCode')
   data=SalestotalLoansCount(request,request.session.get('franchCode'))
   if not data:
      data=[]
   # paginator = Paginator(res.json(), 1)

   
   
      
   storeFranchRecords=[]
   if request.GET.get('applicationid'):
      request.session['salesapplicationid']=request.GET.get('applicationid')
      if request.session.get('date4'):
         del request.session['date4']
   
   if request.session.get('salesapplicationid'):

      if request.session.get('salesapplicationid').startswith("SLNEMP"):
       for i in data:
         if i['registerId']==request.session.get('salesapplicationid'):
            data=[i]
            break;
      else:

        for i in data:


         if i['franchiseId']==request.session.get('salesapplicationid'):
            storeFranchRecords.append(i)
        data=storeFranchRecords
        
   
   if request.session.get('date4'):
      if request.session.get('salesapplicationid'):
         del request.session['salesapplicationid']

      data=SalestotalLoansCount(request,request.session.get('franchCode'),request.session.get('date4'))
      if not data:
         data=[]
      
         
      
   # if data:
   paginator = Paginator(data, 10)
   page = request.GET.get('page') 
         
   try:
        objects = paginator.page(page)

   except PageNotAnInteger:
        objects = paginator.page(1)
   except EmptyPage:
        objects = paginator.page(1)
  
   start_index = (objects.number - 1) * paginator.per_page + 1
   
   return render(request,'dsaTrack.html',{'objects':objects,'start_index':start_index,'sumofAllTotalDisbursamountdsa':request.session.get('sumofAllTotalDisbursamountdsa')})


def getAllFranchiseTotalLoans():

   requests.get()
   
def allFranchiseAmounts(request):
    if request.GET.get('date'):
        request.session['franchDatefilter']=request.GET.get('date')
        
    ids=getAllFranchiseIDS(request,request.session.get('franchCode'))
    
    franchiseAmounts=allTotalFranchiseDisbursedAmountCalculator(request,request.GET.get('date'),ids)
    result=[]
   #  franchiseAmounts=thread1.result()
    for i,j in zip(ids,franchiseAmounts):
        
        context={
            'franchiseId':i.get('franchise_id'),
            'Amount':intcomma(j),
        }
        result.append(context)
    return result
    
    # paginator = Paginator(result, 10)  
    # page = request.GET.get('page')
         
    # try:
    #     objects = paginator.page(page)
    #   #   print(objects)
    # except PageNotAnInteger:
    #     objects = paginator.page(1)
    # except EmptyPage:
    #     objects = paginator.page(1)
  
    # start_index = (objects.number - 1) * paginator.per_page + 1
   
    # return render(request,'FranchiseClosedAmount.html',{'objects':objects,'start_index':start_index,'sumofAllTotalDisbursamountdsa':request.session.get('sumofAllTotalDisbursamountdsa')})
 

#Main Branch Sales IDS......................................
def getMainBranchAllSalesIDS(request,franchiseCode=None):

   res=requests.get(f'{settings.HR_SOURCE_URL}/api/mymodel/{franchiseCode}/giveFranchiseSalesIds/')
   if res.status_code==200:


      return res.json()
   else:return []
#Main Branch Sales IDS.................................... 



#Main Branch Dsa IDS......................................
def getMainBranchAllDsaIds(request,franchiseCode=None):

   res=requests.get(f'{settings.HR_SOURCE_URL}/api/mymodel/{franchiseCode}/giveFranchiseDSAIds/')
   if res.status_code==200:


      return res.json()
   else:return []
#Main Branch Dsa IDS.................................... 

        
    
# DashBoardIndexpage Data Process Supporter......................................
def dashboardAmountCountsLogic(request,date1=None,date2=None):


   
   # if request.GET.get('date1'): date1=request.GET.get('date1')
   # else: date1=None
   
   # date1= request.GET.get('date1') if request.GET.get('date1') else None

   
   franchiseIds=getAllFranchiseIDS(request,request.session.get('franchCode'))
   slnTotalbusiness=allTotalFranchiseAmountCalculator(request,date1,franchiseIds)
   

   

  
#   DSA And SAles IDS MAin Branch.......
   mainBranchDsaIds=getMainBranchAllDsaIds(request,request.session.get('franchCode'))
   mainBranchSalesIds=getMainBranchAllSalesIDS(request,request.session.get('franchCode'))
#   DSA And SAles IDS MAin Branch......

   
   # Main Branch Total Amount By DSA and Sales..........................
   mainBranchdsaAmount=allTotalDSADisbursedAmountCalculator(request,date1,mainBranchDsaIds)
   mainBranchSalesAmount=allTotalSALESDisbursedAmountCalculator(request,date1,mainBranchSalesIds)

   
   
   franchiseIdswithoutMainBranch=[i for i in franchiseIds if i.get('franchise_id')!=settings.MAIN_BRANCHID]
   allFranchiseAmountexceptMainBranch=allTotalFranchiseAmountCalculator(request,date1,franchiseIdswithoutMainBranch)

   
   onlyMainOfficeAmount=sum(slnTotalbusiness)-sum(allFranchiseAmountexceptMainBranch)
   
   
   onlyMainbranchAmount=sum(slnTotalbusiness)-sum(allFranchiseAmountexceptMainBranch)

   
   dsaIds=getAllDsaIds(request,request.session.get('franchCode'))
   dsaTotalAmount=allTotalDSADisbursedAmountCalculator(request,date1,dsaIds)
   
   
   salesIds=getAllSalesIDS(request,request.session.get('franchCode'))

   salesTotalAmount=allTotalSALESDisbursedAmountCalculator(request,date1,salesIds)
   
   
 
  
   # For Total Loans Closed By All Franchises,dsa's,Sales......................
   
   if not date2:
    result=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/All_OverAll_LoansCount/')
   else:
      result=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/All_OverAll_LoansCount/?date={date2}')
   result=result.json()

   context={
      'slnTotalbusiness':intcomma(sum(slnTotalbusiness)),
      'onlyMainOfficeAmount':onlyMainOfficeAmount,
      'allFranchiseAmountexceptMainBranch':intcomma(sum(allFranchiseAmountexceptMainBranch)),
      'dsaTotalAmount':intcomma(sum(dsaTotalAmount)),
      'salesTotalAmount':intcomma(sum(salesTotalAmount)),
      'totalFranchisesCount':len(franchiseIds),
      'totalDSACount':len(dsaIds),
      'totalSalesCount':len(salesIds),
      'onlyMainbranchAmount':intcomma(onlyMainbranchAmount),
      'mainBranchDsaIds':len(mainBranchDsaIds),
      'mainBranchSalesIds':len(mainBranchSalesIds),
      'mainBranchdsaAmount':intcomma(sum(mainBranchdsaAmount)),
      'mainBranchSalesAmount':intcomma(sum(mainBranchSalesAmount)),
      
      'totalApplications':result.get('totalcount'),
       'creditCard':result.get('creditcount'),
       'businessLength':result.get('buscount'),
       'EducationLength':result.get('educount'),
       'personalLength':result.get('percount'),
       'homeLength':result.get('homecount'),
       'carLength':result.get('carcount'),
       'lapLength':result.get('lapcount'),
       'otherLength':result.get('othercount'),
       'goldLength':result.get('goldcount'),
       'TotalInsurances':result.get('totalInsurances'),
       'AllInsurance':result.get('allinsurance'),
       'LifeInsurance':result.get('lifeinsurance'),
       'HealthInsurance':result.get('healthinsurance'),
       'GeneralInsurnace':result.get('generalinsurance'),
      
   }
   return context

   
   

def allHOBranchLoansCount(request,refCode,date):
    
   #  salesIds=getAllSalesIDS(request,request.session.get('franchCode'))
   #  dsaIds=getAllDsaIds(request,request.session.get('franchCode'))
    result,busines,education,personal,home,lap,car,other,gold=[],[],[],[],[],[],[],[],[]
    response2=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_TotlDSA_SalesFrloan_refCode_LoansCount/')
    if response2.status_code==200:
       result=response2.json()
    else:return []
    context={
       'totalApplications':result.get('totalcount'),
       'creditCard':result.get('creditcount'),
       'businessLength':result.get('buscount'),
       'EducationLength':result.get('educount'),
       'personalLength':result.get('percount'),
       'homeLength':result.get('homecount'),
       'carLength':result.get('carcount'),
       'lapLength':result.get('lapcount'),
       'otherLength':result.get('othercount'),
       'goldLength':result.get('goldcount'),
       'TotalInsurances':result.get('totalInsurances'),
       'AllInsurance':result.get('allinsurance'),
       'LifeInsurance':result.get('lifeinsurance'),
       'HealthInsurance':result.get('healthinsurance'),
       'GeneralInsurnace':result.get('generalinsurance'),
    }
    return context
 
 
 
def slnHoBranchTotalLoansIncludingDSASales(request):

   return render(request,"SLNHOBranchTotalLoans.html",allHOBranchLoansCount(request,request.session.get('franchCode'),None))
   
   
   
# Superadmin closed Forms Data.............................

def allSuperAdminLoansCount(request,refCode,date):
    
   #  salesIds=getAllSalesIDS(request,request.session.get('franchCode'))
   #  dsaIds=getAllDsaIds(request,request.session.get('franchCode'))
    result,busines,education,personal,home,lap,car,other,gold=[],[],[],[],[],[],[],[],[]
    response2=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_LoansCount/')
    if response2.status_code==200:
       result=response2.json()
    else:return []
    ccResponse=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/credit_loan_refCode_LoansCount/')
    if ccResponse.status_code==200: 
      ccResult=ccResponse.json()
    else:
       return []
    
   
    
    context={
       'totalApplications':result.get('totalcount'),
       'creditCard':ccResult.get('count'),
       'businessLength':result.get('buscount'),
       'EducationLength':result.get('educount'),
       'personalLength':result.get('percount'),
       'homeLength':result.get('homecount'),
       'carLength':result.get('carcount'),
       'lapLength':result.get('lapcount'),
       'otherLength':result.get('othercount'),
       'goldLength':result.get('goldcount'),
       'TotalInsurances':result.get('totalInsurances'),
       'AllInsurance':result.get('allinsurance'),
       'LifeInsurance':result.get('lifeinsurance'),
       'HealthInsurance':result.get('healthinsurance'),
       'GeneralInsurnace':result.get('generalinsurance'),
    }
    return context
 
 
def slnSuperAdminTotalLoans(request):
   return render(request,"SLNHOBranchTotalLoans.html",allSuperAdminLoansCount(request,dsamanualId(request),None))
   


def dashBoardIndexpage(request):
   date1=request.POST.get('date1') if request.POST.get('date1') else None
   date2=request.POST.get('date2') if request.POST.get('date2') else None

   context=dashboardAmountCountsLogic(request,date1,date2)
   # context.update(allCount(request,request.session.get('franchCode'),None))
   return render(request,"Index.html",context)
   



def dsaMasterData(request):
    if request.GET.get('deleteId'):
       try:
        instance = DSAMasterData.objects.get(id=request.GET.get('deleteId'))
        instance.delete() 
       except:
          pass
   #  if request
   
    
    if request.method=="POST":
       if 'dateFilter' in request.POST:

          date=request.POST.get('dateFilter')
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()

          data=DSAMasterData.objects.filter(created_at__range=(date_obj1,date_obj2))
          return render(request,"MasterData.html",{'data':data,'title':"DSA Master Data",'url':'DsaMasterData'})
       elif 'MasterDataFile' in request.FILES:

         MasterDatafile=request.FILES.get('MasterDataFile')
         DSAMasterData.objects.create(MasterDataImage=MasterDatafile)
       
    data=DSAMasterData.objects.all()
    return render(request,"MasterData.html",{'data':data,'title':"DSA Master Data",'url':'DsaMasterData'})
 
 
def franchiseMasterData(request):
   #  if request.GET.get('deleteId'):FranchiseMasterData.objects.filter(id=request.GET.get('deleteId')).delete()
    if request.GET.get('deleteId'):
       try:
        instance = FranchiseMasterData.objects.get(id=request.GET.get('deleteId'))
        instance.delete() 
       except:
          pass
       
    if request.method=="POST":
       if 'dateFilter' in request.POST:

          date=request.POST.get('dateFilter')
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()

          data=FranchiseMasterData.objects.filter(created_at__range=(date_obj1,date_obj2))
          return render(request,"MasterData.html",{'data':data,'title':"Franchise Master Data",'url':'FranchiseMasterData'})
       elif 'MasterDataFile' in request.FILES:
        MasterDatafile=request.FILES.get('MasterDataFile')
        FranchiseMasterData.objects.create(MasterDataImage=MasterDatafile)
    data=FranchiseMasterData.objects.all()
    return render(request,"MasterData.html",{'data':data,'title':"Franchise Master Data",'url':'FranchiseMasterData'})
 
 
def accountsMasterData(request):
    if request.GET.get('deleteId'):
       try:
        instance = AccountsMasterData.objects.get(id=request.GET.get('deleteId'))
        instance.delete() 
       except:
          pass
   #  if request.GET.get('deleteId'):AccountsMasterData.objects.filter(id=request.GET.get('deleteId')).delete()
    if request.method=="POST":
       if 'dateFilter' in request.POST:

          date=request.POST.get('dateFilter')
          strtDate=date.split(' to ')[0]
          endDate=date.split(' to ')[1]
          date_obj1 = datetime.strptime(strtDate, '%Y-%m-%d').date()
          date_obj2 = datetime.strptime(endDate, '%Y-%m-%d').date()

          data=AccountsMasterData.objects.filter(created_at__range=(date_obj1,date_obj2))
          return render(request,"MasterData.html",{'data':data,'title':"Accounts Master Data",'url':'AccountsMasterData'})
       elif 'MasterDataFile' in request.FILES:
        MasterDatafile=request.FILES.get('MasterDataFile')
        AccountsMasterData.objects.create(MasterDataImage=MasterDatafile)
    data=AccountsMasterData.objects.all()
    return render(request,"MasterData.html",{'data':data,'title':"Accounts Master Data",'url':'AccountsMasterData'})
 
 
 
import time   

def demo(request):
    time.sleep(2)
    return render(request,"demo.html")





    


