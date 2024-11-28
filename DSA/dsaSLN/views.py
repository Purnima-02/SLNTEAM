import json
from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
import requests


from .models import *
from django.http import HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.paginator import *
from django.views.decorators.csrf import csrf_exempt
from concurrent.futures import ThreadPoolExecutor
# from Comisiions.views import viewComissions


# Create your views here.
@csrf_exempt
def dsaLogin(request):
   errorMessage=None
   if request.method=="POST":
      # print(request.POST.get('applicationid'))
      id=request.POST.get('applicationid')
      passw=request.POST.get('password')
      response=requests.get(f"{settings.HR_SOURCE_URL}/api/mymodel/{id}/{passw}/dsaLoginCheck/")
      if response.status_code==200:
         res=response.json()
         
         # print(res)
         DSA.objects.get_or_create(dsa_registerid=id,defaults={'dsa_registerid':id})
         request.session['verified']=True
         request.session['dsaLoginId']=request.POST.get('applicationid')
         franchise_code = res[0].get('franchiseCode')  
         request.session['franchCode'] = franchise_code
        

         
         if request.session.get('indexPage'): return redirect('dsa-index')
         
         return redirect(request.session.get('pageurl'))
      else:
        errorMessage="Wrong Credentials"

   return render(request,'dsaLogin.html',{'errorMessage':errorMessage})

def dsaLogout(request):
   # if  request.session.get('verified'):
   #  del request.session['verified']
   # if request.session.get('indexPage'):
   #   del request.session['indexPage']
   # return render(request,'dsaLogin.html')
   request.session.clear()
   return redirect('dsalogin')


# DSA ManualId
def dsamanualId(request):

   return request.session.get('dsaLoginId')
# DSA ManualId

@csrf_exempt
def dsaProfile(request):
    resp=requests.get(f'http://13.51.23.145:999/api/mymodel/{dsamanualId(request)}/custom_get/')
    if resp.status_code==200:


       data=resp.json()
             
       if request.method=='POST':
          
          request.POST.get('dsa_registerid')
          
          data={
             
             'dsa_name':request.POST.get('dsa_name'),
             'email':request.POST.get('email'),
             'phone':request.POST.get('mobilenumber'),
             'profession':request.POST.get('profession'),
            #  'dsa_password':request.POST.get('dsa_password'),
             'city':request.POST.get('city'),
             
             
          }


          response=requests.post(f'{settings.HR_SOURCE_URL}/api/mymodel/{dsamanualId(request)}/custom_update/',json=data)
          if response.status_code==201 or response.status_code==200:
            data=response.json()

            listData=[data]

            return render(request,'DSAProfile.html',{'data':listData,'edited':True})
          else:
             return HttpResponse("No data..")
          
          
       return render(request,'DSAProfile.html',{'data':data})
    else: return None
    

def dsaDashboard(request):
   response=requests.get(f'{settings.SUPERADMIN_URL}/superadmin/app1/DSAMasterData_AppliViewsets/')
   result = response.json() if response.status_code in [200, 201] else None 
   result=result[0] if result else None
   return render(request,"DsaDashboard.html",{'result': result})


def disbursedTotalAmount(request):
   request.session['disbursedTotalAmount']=True
   from Comisiions.views import commonComissions
   total=commonComissions(request)
   if total:
      loans= total
      request.session['disbursedTotalAmount']=None
      del request.session['disbursedTotalAmount']
      return loans
   else:
      return None
   
def disbursedTotalLoans(request):
   request.session['disbursedTotalLoans']=True
   from Comisiions.views import commonComissions
   total=commonComissions(request)
   if total:
      loans= total
      request.session['disbursedTotalLoans']=None
      del request.session['disbursedTotalLoans']
      return loans
   else:
      return None
   
def disbursedTotalLoanIds(request):
  response=requests.get(f"{settings.ACCOUNTS_SOURCE_URL}/getDisburseIds/{dsamanualId(request)}")
  if response.status_code==200:
     res=response.json()
     finlres=[res]

     return res
  else:
     return None
  
def demo4(request):
     return HttpResponse(f"{settings.ACCOUNTS_SOURCE_URL}")

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


def dsaTotalAllApplications(request):
    dsaObj = DSA.objects.prefetch_related('dsa').get(dsa_registerid=dsamanualId(request))
    dsaApp=dsaObj.dsa.all()
    return dsaApp
   
# def chat(request):
#     return render(request,"chat.html") 

# Business LOan API......................................................
def businessLoanApi(request):
    #  print(f'{settings.SOURCE_PROJECT_URL}/bl/getByRefCode/SLNDSA1002')
     records=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/getByRefCode/{dsamanualId(request)}')
     if records.status_code==200:
      res=records.json()
      # loans=[]
      # allLoans=[]
      if request.session.get('approved') == "Approved":
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/getApprovedRecords/{dsamanualId(request)}')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:

            return []
         
         # Old Approach
      #  print("Apprved method..")
      #  for result in res:
      #     if result.get('applicationverification') is not None:
      #        a=result.get('applicationverification')
      #        if a.get('verification_status')=="Approved":
      #           loans.append(result)
      #  return loans

      
      if request.session.get('rejected') == "Rejected":
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/getRejectedRecords/{dsamanualId(request)}')
         if responseData.status_code==200:
            res=responseData.json()           
         else:
           
            return []
         
      
      
   
      return res
     else:
         return []
     
     
# Education LOan API......................................................
def educationLoanApi(request):

    records=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/getByRefCode/{dsamanualId(request)}')
    if records.status_code==200:

      res=records.json()
     
      loans=[]
      allLoans=[]
     
      if request.session.get('approved') == "Approved":
      
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/EduViewsets/{dsamanualId(request)}/getApprovedRecords/')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
           
            return []
    
      if request.session.get('rejected') == "Rejected":
      #   del request.session['approved']
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/EduViewsets/{dsamanualId(request)}/getRejectedRecords/')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
           
            return []
      
    
      return res
    else:
         return []
      
def lapApi(request):
    records=requests.get(f'{settings.SOURCE_PROJECT_URL}/getByRefCode/{dsamanualId(request)}')
    if records.status_code==200:
      # print("edu../")
      res=records.json()
     
      loans=[]
      allLoans=[]
     
      if request.session.get('approved') == "Approved":
      
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/lapapi/{dsamanualId(request)}/getApprovedRecords/')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
            return []
    
      if request.session.get('rejected') == "Rejected":
              
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/lapapi/{dsamanualId(request)}/getRejectedRecords/')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
            return []
      
    
      # print(res)
      return res
    else:
         return []
      

def homeApi(request):
    records=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/getHomeByRefCode/{dsamanualId(request)}')
    if records.status_code==200:
      # print("edu../")
      res=records.json()
     
      loans=[]
      allLoans=[]
     
      if request.session.get('approved') == "Approved":
      
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/getHomeApprovedRecords/{dsamanualId(request)}')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
            return []
    
      if request.session.get('rejected') == "Rejected":
              
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/getHomeRejectedRecords/{dsamanualId(request)}')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
            return []
      return res
    else:
         return []
      

def personalApi(request):
    records=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/getByRefCode/{dsamanualId(request)}')
    if records.status_code==200:
      # print("edu../")
      res=records.json()
     
      loans=[]
      allLoans=[]
     
      if request.session.get('approved') == "Approved":
      
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/getApprovedRecords/{dsamanualId(request)}')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
            return []
    
      if request.session.get('rejected') == "Rejected":
              
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/getRejectedRecords/{dsamanualId(request)}')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
            return []
      return res
    else:
         return []


def carApi(request):
    records=requests.get(f'{settings.SOURCE_PROJECT_URL}/cl/getByRefCode/{dsamanualId(request)}')
    if records.status_code==200:
      # print("edu../")
      res=records.json()
     
      loans=[]
      allLoans=[]
     
      if request.session.get('approved') == "Approved":
      
         responseData=requests.get(f'{settings.SOURCE_PROJECT_URL}/cl/ddproject/{dsamanualId(request)}/getApprovedRecords/')
         if responseData.status_code==200:
            res=responseData.json()
            # print(result)            
         else:
            return []
    
      if request.session.get('rejected') == "Rejected":
              
         records=requests.get(f'{settings.SOURCE_PROJECT_URL}/cl/getRejectedRecords/{dsamanualId(request)}')
         if records.status_code==200:
            res=records.json()
            # print(result)            
         else:
            return []
      return res
    else:
         return []
   

def dsaSupport(request):
   return render(request,'DSAsupport.html',{'dsaSupprtUrl':f"{settings.CUSTOMER_SUPPORT_URL}/DSA_create_ticket/",'dsaId':f'{dsamanualId(request)}'})
      
def dsaAllInsurancesCount(request):
   response=requests.get(f"{settings.SOURCE_PROJECT_URL}/commonInsuranceGet/{dsamanualId(request)}")
   if response.status_code==200:

      return response.json()
   else:
      return HttpResponse(response.content,response.status_code)
   
def creditCardCount(request,refCode):
    dsaObj = DSA.objects.prefetch_related('dsa').get(dsa_registerid=refCode)
    dsaApp=dsaObj.dsa.all()
    result=[]
    for i in dsaApp:
       if i.cust_applicationId.startswith('SLNCC'):
          result.append(i.cust_applicationId)
    return len(result)
 
def allCount(request,refCode):
    dsaObj = DSA.objects.prefetch_related('dsa').get(dsa_registerid=refCode)
    dsaApp=dsaObj.dsa.all()
    result,busines,education,personal,home,lap,car,other,gold=[],[],[],[],[],[],[],[],[]
    
    for i in dsaApp:
       if i.cust_applicationId.startswith('SLNCC'):
          result.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNBL'):
          busines.append(i.cust_applicationId)
      
       elif i.cust_applicationId.startswith('SLNEL'):
          education.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNPL'):
          personal.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNHL'):
          home.append(i.cust_applicationId)
         
       elif i.cust_applicationId.startswith('SLNLAP'):
          lap.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNCL'):
          car.append(i.cust_applicationId)
          
       elif i.cust_applicationId.startswith('SLNOL'):
          other.append(i.cust_applicationId)
       else:
          gold.append(i.cust_applicationId)
         
    context={
       'totalApplications':len(dsaApp),
       'creditCard':len(result),
       'businessLength':len(busines),
       'EducationLength':len(education),
       'personalLength':len(personal),
       'homeLength':len(home),
       'carLength':len(car),
       'lapLength':len(lap),
       'otherloan':len(other),
       'goldloan':len(gold),
       'Insurances':dsaAllInsurancesCount(request),
   }
    return context
       
   

#DSA Index MEthod.................................................
def dsaIndex(request):
    totalApplications=dsaTotalAllApplications(request)

    education=[]
    personal=[]
    request.session['common']="business"
    # busi=businessLoanApi(request)

    # bus=businessLoanApi(request)
    return render(request,"DSAIndex.html",allCount(request,dsamanualId(request)))



# Approved Loans Method.............................................
@csrf_exempt
def approvedLoans(request):
  if request.method=='POST':
     if request.POST.get('loantype'):

      if request.POST.get('date'):
      #   print(request.POST.get('date'))
        request.session['startdate']=request.POST.get('date').split(' to ')[0]
        request.session['enddate']=request.POST.get('date').split(' to ')[1]
      else:
        request.session['startdate']=None
        # print( request.POST.get('loantype'))

      loantyp=request.POST.get('loantype')
        # date= request.POST.get('date')
      if request.POST.get('loantype')!='All':
         request.session['loantype']=loantyp
         
         # print(loantyp + "hhhhhoop")
         if request.session.get('All'):
          del request.session['All']
        
      else:
            request.session['All']=loantyp
            if request.session.get('loantype'):
             del request.session['loantype']

# search By Application Id
     if request.POST.get('applicationid'):
      request.session['applicationid']=request.POST.get('applicationid')
      # print(request.POST.get('applicationid')+ "jjjjkk111")
      if request.session.get('loantype') or request.session.get('All'):
         request.session['All']=None
         request.session['loantype']=None
     else:
        request.session['applicationid']=None
        
# search By Application Id
     
  filterLoans=[]
  request.session['approved'] = "Approved"
  allLoans = []
  
     # For TO MAKE EXECUTION TIME LESS..
  with ThreadPoolExecutor() as executor:
        future_business = executor.submit(businessLoanApi, request)
        future_education = executor.submit(educationLoanApi, request)
        future_lap=executor.submit(lapApi,request)
        future_home=executor.submit(homeApi,request)
        future_personal=executor.submit(personalApi,request)
        future_car=executor.submit(carApi,request)

        
  business_result = future_business.result()
  education_result = future_education.result()
  lap_result = future_lap.result()
  home_result=future_home.result()
  per_result=future_personal.result()
  car_result=future_car.result()

  
      
  if business_result:
            allLoans.extend(business_result)
  if education_result:
            allLoans.extend(education_result)
  if lap_result:
     allLoans.extend(lap_result)
  if home_result:
      allLoans.extend(home_result)
  if per_result:
      allLoans.extend(per_result)
  if car_result:
      allLoans.extend(car_result)


#   bus_loan_data = businessLoanApi(request)
#   edu_loan_data=educationLoanApi(request)
  
  del request.session['approved']
    
    # Check if loan_data is a list and extend allLoans, else append it directly
#   if bus_loan_data:
#      allLoans.extend(bus_loan_data)
#     #  print(allLoans)
#   if edu_loan_data:
#         allLoans.extend(edu_loan_data)

  totalLoanAmount=0
  if allLoans:
      
      
      request.session['approvedLoansLength']=len(allLoans)

      if request.session.get('FromalloanstoApproved'):
       for amount in allLoans:
         # print(amount)
         totalLoanAmount+=float(amount.get('required_loan_amount'))
         # print(int(amount.get('required_loan_amount')))

      # print(totalLoanAmount)
       request.session['approvedLoansAmount']=totalLoanAmount
       return 
  
 
   

  if request.session.get('applicationid'):
       for loans in allLoans:
          if loans.get('application_id')== request.session.get('applicationid'):
             filterLoans.append(loans)
      #  print("(0000000000)")

       if not filterLoans:
          request.session['applicationid']=None
          return render(request,'DataTable.html',{'objects': []})
       allLoans=filterLoans



  if request.session.get('loantype'):
     for loans in allLoans:
      #   print("NotAllLoans///////")
      #   print(loans.get('created_at'))
        if  request.session.get('startdate') and loans.get('application_loan_type')==request.session.get('loantype') and loans.get('created_at') >= request.session.get('startdate') and loans.get('created_at') <= request.session.get('enddate'):
           filterLoans.append(loans)
           
        if not request.session.get('startdate') and loans.get('application_loan_type')==request.session.get('loantype'):
           filterLoans.append(loans)
     allLoans=filterLoans
 
#   print(allLoans)
  if request.session.get('All'):
     for loans in allLoans:
      #   print("AllLoans")
      #   print(loans.get('created_at'))

        if  request.session.get('startdate') and loans.get('created_at') >= request.session.get('startdate') and loans.get('created_at') <= request.session.get('enddate'):
           filterLoans.append(loans)
        if not request.session.get('startdate'):
           filterLoans.append(loans)
     allLoans=filterLoans
     
  if allLoans:
    
     paginator = Paginator(allLoans, 10)  
     page = request.GET.get('page') 
     try:
        objects = paginator.page(page)
     except :
        objects = paginator.page(1)
        
    
     start_index = (objects.number - 1) * paginator.per_page + 1
   #   print(f"{objects.number}---{paginator.per_page}")



     if request.session.get('applicationid'):
       request.session['applicationid']=None
      #  print(allLOans)
       return render(request,'DataTable.html',{'objects': objects,'start_index': start_index})


   #    # Check if the request is an AJAX request
   #   if request.headers.get('x-requested-with') == 'XMLGetHttpRequest':
   #      print("Ajex method is activate..........")
   #      return render(request,'AllAprovedLoans.html',{'objects': objects,'start_index': start_index})


     return render(request, "AllAprovedLoans.html", {'objects': objects, 'start_index': start_index,'title':"Approved Loans"})
  else:
     return render(request, "AllAprovedLoans.html", {'objects': [],'title':"Approved Loans"})
  

# Rejected Loans.......................................................
@csrf_exempt
def rejectedLoans(request):
  if request.method=='POST':
     if request.POST.get('loantype'):

      if request.POST.get('date'):
      #   print(request.POST.get('date'))
        request.session['startdate2']=request.POST.get('date').split(' to ')[0]
        request.session['enddate2']=request.POST.get('date').split(' to ')[1]
      else:
        request.session['startdate2']=None
        # print( request.POST.get('loantype'))

      loantyp=request.POST.get('loantype')
        # date= request.POST.get('date')
      if request.POST.get('loantype')!='All':
         request.session['loantype2']=loantyp
         if request.session.get('All2'):
          del request.session['All2']
        
      else:
            request.session['All2']=loantyp
            if request.session.get('loantype2'):
             del request.session['loantype2']

      
# search By Application Id
     if request.POST.get('applicationid'):
       request.session['applicationid1']=request.POST.get('applicationid')
      #  print(request.POST.get('applicationid')+ "jjjjkk111")
       if request.session.get('loantype2') or request.session.get('All2'):
         request.session['All2']=None
         request.session['loantype2']=None
     else:
        request.session['applicationid1']=None
# search By Application Id

           
  filterLoans=[]
  request.session['rejected'] = "Rejected"
  allLoans = []
  
     # For TO MAKE EXECUTION TIME LESS..
  with ThreadPoolExecutor() as executor:
        future_business = executor.submit(businessLoanApi, request)
        future_education = executor.submit(educationLoanApi, request)
        future_lap=executor.submit(lapApi,request)
        future_home=executor.submit(homeApi,request)
        future_personal=executor.submit(personalApi,request)
        future_car=executor.submit(carApi,request)


        
  business_result = future_business.result()
  education_result = future_education.result()
  lap_result = future_lap.result()
  home_result=future_home.result()
  per_result=future_personal.result()
  car_result=future_car.result()

  
      
  if business_result:
            allLoans.extend(business_result)
  if education_result:
            allLoans.extend(education_result)
  if lap_result:
     allLoans.extend(lap_result)
  if home_result:
     allLoans.extend(home_result)
  if per_result:
     allLoans.extend(per_result)
  if car_result:
     allLoans.extend(car_result)

#   bus_loan_data = businessLoanApi(request)
#   edu_loan_data=educationLoanApi(request)
  del request.session['rejected']
    
    # Check if loan_data is a list and extend allLoans, else append it directly
#   if bus_loan_data:
#      allLoans.extend(bus_loan_data)
#     #  print(allLoans)
#   if edu_loan_data:
#         allLoans.extend(edu_loan_data)

# For counting Rejected Loans
  totalLoanAmount=0
  if allLoans:
      request.session['rejectedLoansLength']=len(allLoans)
      # print(len(allLoans))

      if request.session.get('FromalloanstoRejectd'):
       for amount in allLoans:

         totalLoanAmount+=float(amount.get('required_loan_amount'))
         # print(int(amount.get('required_loan_amount')))

      # print(totalLoanAmount)
       request.session['rejectedLoansAmount']=totalLoanAmount
       return 
      


# For counting Rejected Loans

  if request.session.get('applicationid1'):
       for loans in allLoans:
          if loans.get('application_id')== request.session.get('applicationid1'):
             filterLoans.append(loans)
      #  print("(0000000000)")
      #  del request.session['applicationid1']
       if not filterLoans:
          request.session['applicationid1']=None
          return render(request,'DataTable.html',{'objects': []})
       allLoans=filterLoans

# Filters
  if request.session.get('loantype2'):
     for loans in allLoans:
      #   print("NotAllLoans")
      #   print(loans.get('created_at'))
        if  request.session.get('startdate2') and loans.get('application_loan_type')==request.session.get('loantype2') and loans.get('created_at') >= request.session.get('startdate2') and loans.get('created_at') <= request.session.get('enddate2'):
           filterLoans.append(loans)
             
        if not request.session.get('startdate2') and loans.get('application_loan_type')==request.session.get('loantype2'):
           filterLoans.append(loans)
     allLoans=filterLoans

  if request.session.get('All2'):
     for loans in allLoans:
      #   print("AllLoans")
      #   print(loans.get('created_at'))

      #   if  loans.get('created_at') >= request.session.get('startdate') and loans.get('created_at') <= request.session.get('enddate'):
      #      filterLoans.append(loans)
      #   if not request.session.get('startdate') and loans.get('loan_type')==request.session.get('loantype'):
      #      filterLoans.append(loans)
        if  request.session.get('startdate2') and loans.get('created_at') >= request.session.get('startdate2') and loans.get('created_at') <= request.session.get('enddate2'):
           filterLoans.append(loans)
        if not request.session.get('startdate2'):
           filterLoans.append(loans)
     allLoans=filterLoans
# Filters  


  if allLoans:
    #  print(allLoans)
    
     paginator = Paginator(allLoans, 10)
     page = request.GET.get('page') 
    
     try:
        objects = paginator.page(page)
     except :
        objects = paginator.page(1)
    
        
    
     start_index = (objects.number - 1) * paginator.per_page + 1
   #   print(f"{objects.number}---{paginator.per_page}")


     if request.session.get('applicationid1'):
       request.session['applicationid1']=None
      #  print(allLOans)
       return render(request,'DataTable.html',{'objects': objects,'start_index': start_index})


      # Check if the request is an AJAX request
     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      #   print("Ajex method is activate..........")
        return render(request,'AllAprovedLoans.html',{'objects': objects,'start_index': start_index})

     return render(request, "AllAprovedLoans.html", {'objects': objects, 'start_index': start_index,'title':"Rejected Loans"})
  else:
     return render(request, "AllAprovedLoans.html", {'objects': [],'title':"Rejected Loans"})
  
 
def get_all_dataAsJson(request):
   # print(dsamanualId(request))
   data=DSA.objects.prefetch_related('dsa').get(dsa_registerid=dsamanualId(request))
   
   data1=data.dsa.values()
   # print(data.dsaapp.all())
   return JsonResponse(list(data1),safe=False)

# ApplyForms.................................................................

def apply_business(request):
    return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/bl/demo",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})
def apply_Education(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/el/apply-educationalLoan",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})
def home_loan(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/home/",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})
def credit_card(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cc/credit/",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})
def car_loan(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/cl/car-loan-application/",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})
def lap(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/lapapply/",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})
def apply_personal(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/pl/personal/",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})
def apply_gold(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/goldloan/",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})
def apply_otherLoan(request):
   return render(request,"applyLoans.html",{'url':f"{settings.SOURCE_PROJECT_URL}/otherloan/",'dsaId':dsamanualId(request),'sourceUrl':f"{settings.SOURCE_PROJECT_URL}",'dsaUrl':f'{settings.DSA_URL}'})





# All Loans......................................................................
@csrf_exempt
def allLOans(request):

   if request.GET.get('id'):
        template="DemowithOutDashBoard.html"
        an=990
   else:
        an=None
        template="DsaDashboard.html"


   
   # request.session['approved'] = None
   if request.method=='POST':
    
     if request.POST.get('loantype'):
      #   print(request.POST.get('loantype'),"000000000008776")
        if request.POST.get('loansteps'):
         #   print(request.POST.get('loansteps'))
           request.session['loansteps']=request.POST.get('loansteps')
        else:
            if request.session.get('loansteps'):
               del request.session['loansteps']
            
       
      #   print(request.POST.get('date'))
        if request.POST.get('date'):
         # print(request.POST.get('date'))
         request.session['startdate1']=request.POST.get('date').split(' to ')[0]
         request.session['enddate1']=request.POST.get('date').split(' to ')[1]
        else:
            request.session['startdate1']=None
           
      #   print( request.POST.get('loantype'))

        loantyp=request.POST.get('loantype')
        # date= request.POST.get('date')
        if request.POST.get('loantype')!='All':
         request.session['loantype1']=loantyp

         if request.session.get('All1'):
          del request.session['All1']
        
        else:
            request.session['All1']=loantyp
            if request.session.get('loantype1'):
             del request.session['loantype1']

        request.session['loanstatus']=request.POST.get('loanstatus')
        
        # search By Application Id...........
     if request.POST.get('applicationid1'):
         request.session['applicationid2']=request.POST.get('applicationid1')
         # print(request.POST.get('applicationid1')+ "jjjjkk111")
         if request.session.get('loantype1') or request.session.get('All1'):
          request.session['All1']=None
          request.session['loantype1']=None
     else:
      #  request.session['applicationid2']=None
       if request.session.get('applicationid2'):
          del request.session['applicationid2']
# search By Application Id
      
        
   filterLoans=[] 
   allLoansVariable=[]
   allLoansVariableCopy=0


   # For TO MAKE EXECUTION TIME LESS..
   with ThreadPoolExecutor() as executor:
        future_business = executor.submit(businessLoanApi, request)
        future_education = executor.submit(educationLoanApi, request)
        future_lap = executor.submit(lapApi, request)
        future_home=executor.submit(homeApi,request)
        future_personal=executor.submit(personalApi,request)
        future_car=executor.submit(carApi,request)



        
   business_result = future_business.result()
   education_result = future_education.result()
   lap_result = future_lap.result()
   home_result = future_home.result()
   per_result = future_personal.result()
   car_result = future_car.result()


      
   if business_result:
            allLoansVariable.extend(business_result)
   if education_result:
            allLoansVariable.extend(education_result)
   if lap_result:
      allLoansVariable.extend(lap_result)
   if home_result:
      allLoansVariable.extend(home_result)
   if per_result:
      allLoansVariable.extend(per_result)
   if car_result:
      allLoansVariable.extend(car_result)



# OLD APPROACH
   # if businessLoanApi(request):
   #    allLoansVariable.extend(businessLoanApi(request))
   # if educationLoanApi(request):
   #    allLoansVariable.extend(educationLoanApi(request))
   # if homeApi(request):
   #    allLoansVariable.extend(homeApi(request))
   # if personalApi(request):
   #    allLoansVariable.extend(personalApi(request))
   # if lapApi(request):
   #    allLoansVariable.extend(lapApi(request))

   if request.session.get('comission'):
        return allLoansVariable

   AlltotalLoansAmount=0
   if allLoansVariable:
       allLoansVariableCopy=len(allLoansVariable)
       for amount in allLoansVariable:
          AlltotalLoansAmount+=float(amount.get('required_loan_amount'))
          
   # Search Input
   if request.session.get('applicationid2'):
       for loans in allLoansVariable:
          if loans.get('application_id')== request.session.get('applicationid2'):
             filterLoans.append(loans)
      #  print("(0000000000)")

       if not filterLoans:
          request.session['applicationid2']=None
          return render(request,'DataTable.html',{'objects': []})
      #  del request.session['applicationid2']
       allLoansVariable=filterLoans
# Search Input



   if request.session.get('loantype1'):


     if request.session.get('loanstatus')!="All" and request.session.get('loanstatus')!="Pending" and request.session.get('loanstatus')!="Disbursed":
       for loans in allLoansVariable:
      #   loans.get('applicationverification')
     
        if loans.get('verification') is not None:
          a=loans.get('verification')
         #  print("pp1..")
         #  print(a.get('verification_status'))
          if request.session.get('startdate1') and a.get('verification_status')== request.session.get('loanstatus') and loans.get('application_loan_type')==request.session.get('loantype1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
           filterLoans.append(loans)
          if not request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1') and a.get('verification_status')== request.session.get('loanstatus'):
         #   print("pp1.0....")
           filterLoans.append(loans)
       allLoansVariable=filterLoans

     elif request.session.get('loanstatus')=="Pending":
       for loans in allLoansVariable:
        if loans.get('verification') is None:
          a=loans.get('verification')
         #  print("pp2..")
         #  print(loans.get('created_at'))
          if  request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
           filterLoans.append(loans)
          if not request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1'):
           filterLoans.append(loans)
       allLoansVariable=filterLoans

     elif request.session.get('loanstatus')=="Disbursed":
        result=[]
        disbursids=disbursedTotalLoanIds(request)
        for i in allLoansVariable:
           for j in disbursids:
              if  request.session.get('startdate1') and i.get('application_id')==j['application_id'] and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
                 result.append(i)
              if not request.session.get('startdate1') and i.get('application_id')==j['application_id']:
                 result.append(i)
        allLoansVariable=result
           
        
     elif request.session.get('loanstatus')=="All":

        for loans in allLoansVariable:
         #   print("pp3..")
         #   print(loans.get('created_at'))
           if  request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
            filterLoans.append(loans)
           if not request.session.get('startdate1') and loans.get('application_loan_type')==request.session.get('loantype1'):
            filterLoans.append(loans)

        allLoansVariable=filterLoans

        if request.session.get('loansteps'):
           uploadFilters=[]

         #   print("Upload ,,,,,,,//.......")
           if request.session.get('loansteps')=="Uploaddocuments":
              
              for loans in allLoansVariable:
               #   print("Upload Executed.......")
                 if loans.get('documents') is not None:
                  #   print("Upload Executed.......")
                    uploadFilters.append(loans)
              allLoansVariable=uploadFilters
            
           elif request.session.get('loansteps')=="Notuploaddocuments":

              for loans in allLoansVariable:
               #   print("Upload Executed.......")
                 if loans.get('documents') is None:
                  #   print("Upload Executed.......")
                    uploadFilters.append(loans)
              allLoansVariable=uploadFilters
      #   print("All status")
    
              


   if request.session.get('All1'):

      if request.session.get('loanstatus')!="All" and request.session.get('loanstatus')!="Pending" and request.session.get('loanstatus')!="Disbursed":
       for loans in allLoansVariable:
      #   loans.get('applicationverification')
     
         if loans.get('verification') is not None:
           a=loans.get('verification')
         #  print("pp1..")
         #   print(a.get('verification_status'))
           if request.session.get('startdate1') and a.get('verification_status')== request.session.get('loanstatus') and loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
            filterLoans.append(loans)
           if not request.session.get('startdate1') and a.get('verification_status')== request.session.get('loanstatus'):
         #   print("pp1.0....")
            filterLoans.append(loans)
       allLoansVariable=filterLoans
      
      elif request.session.get('loanstatus')=="All":
        for loans in allLoansVariable:
         #   print("pp3..")
         #   print(loans.get('created_at'))
           if  request.session.get('startdate1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
            filterLoans.append(loans)
           if not request.session.get('startdate1'):
            filterLoans.append(loans)
        allLoansVariable=filterLoans

        if request.session.get('loansteps'):
           uploadFilters=[]
         #   print("Upload ,,,,,,,//.......")
           if request.session.get('loansteps')=="Uploaddocuments":
              
              for loans in allLoansVariable:
               #   print("Upload Executed.......")
                 if loans.get('documents') is not None:
                  #   print("Upload Executed.......")
                    uploadFilters.append(loans)

              allLoansVariable=uploadFilters
              
           elif request.session.get('loansteps')=="Notuploaddocuments":
              for loans in allLoansVariable:
               #   print("Upload Executed.......")
                 if loans.get('documents') is None:
                  #   print("Upload Executed.......")
                    uploadFilters.append(loans)
              allLoansVariable=uploadFilters

      elif request.session.get('loanstatus')=="Disbursed":
        result=[]
        disbursids=disbursedTotalLoanIds(request)
        for i in allLoansVariable:
           for j in disbursids:
              if i.get('application_id')==j['application_id']:
                 result.append(i)
        allLoansVariable=result

      elif request.session.get('loanstatus')=="Pending":
       for loans in allLoansVariable:
        if loans.get('verification') is None:
          a=loans.get('verification')
         #  print("pp2..")
         #  print(loans.get('created_at'))
          if  request.session.get('startdate1') and  loans.get('created_at') >= request.session.get('startdate1') and loans.get('created_at') <= request.session.get('enddate1'):
           filterLoans.append(loans)
          if not request.session.get('startdate1'):
           filterLoans.append(loans)
       allLoansVariable=filterLoans

    

   if allLoansVariable:
    #  print(allLoans)
     paginator = Paginator(allLoansVariable, 10)  
     page = request.GET.get('page') 
    
     try:
        objects = paginator.page(page)
     except PageNotAnInteger:
        objects = paginator.page(1)
     except EmptyPage:
        objects = paginator.page(1)
        

    
     start_index = (objects.number - 1) * paginator.per_page + 1
   #   print(f"{objects.number}---{paginator.per_page}")

     


     if request.session.get('applicationid2'):
       request.session['applicationid2']=None
      #  print(allLOans)
       return render(request,'DataTable.html',{'objects': objects,'start_index': start_index})

    
   #   findingMaxMinLengthLoans=[]
     approvalLoansLength,rejectedLoansLength,pendingLoans,disbursedLoansLength=0,0,0,0
     approvalLoansAmount,rejectedLoansAmount,pendingLoansAmount,disbursedTotalAmunt=0,0,0,0

     disbursdAmount=disbursedTotalAmount(request)
     if disbursdAmount:
        disbursedTotalAmunt=disbursdAmount
      #   print(disbursedTotalAmunt)
     disbusedLoans=disbursedTotalLoans(request)
     if disbusedLoans:
        disbursedLoansLength=disbusedLoans
      
     request.session['FromalloanstoApproved']=True
     
     approvedLoans(request)
     if request.session.get('approvedLoansLength'):
       approvalLoansLength=request.session.get('approvedLoansLength')
       approvalLoansAmount=request.session.get('approvedLoansAmount')
       del request.session['approvedLoansAmount']
       del request.session['approvedLoansLength']
   
     del request.session['FromalloanstoApproved']
      
       
      #  print("Approved..")
      #  print(request.session.get('approvedLoansLength'))
      #  print(approvalLoansAmount)
     request.session['FromalloanstoRejectd']=True
     
     rejectedLoans(request)
     if request.session.get('rejectedLoansLength'):

       rejectedLoansLength=request.session.get('rejectedLoansLength')
       rejectedLoansAmount=request.session.get('rejectedLoansAmount')
       del request.session['rejectedLoansLength']
       del request.session['rejectedLoansAmount']
       
     del request.session['FromalloanstoRejectd']
       
      #  print("Rejected..")
      #  print(request.session.get('rejectedLoansLength'))
      #  print(rejectedLoansAmount)

     if allLoansVariableCopy:
       pendingLoans=allLoansVariableCopy-(approvalLoansLength+rejectedLoansLength)
       pendingLoansAmount=AlltotalLoansAmount-(approvalLoansAmount+rejectedLoansAmount)


       

      #  print("All loans..")
      #  print(allLoansVariableCopy)
      #  print(AlltotalLoansAmount)

   #   print("pending loans..")
   #   if pendingLoans:
      #  print(pendingLoans)
      #  print(pendingLoansAmount)

    

     loansTitle=['ApprovedLoans','RejectedLoans','Pending Loans','DisbursedLoans']
     numberOfLoans=[approvalLoansLength,rejectedLoansLength,pendingLoans,disbursedLoansLength]

     loansAmountTitle=['ApprovedAmount','RejectedAmount','PendingAmount','DisbursedAmount']
     loansAmounts=[approvalLoansAmount,rejectedLoansAmount,pendingLoansAmount,disbursedTotalAmunt]



     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      #   print("Ajex method is activate..........")
        return render(request, 'DataTable.html', {'objects': objects, 'start_index': start_index})
    
     return render(request, "AllLoansPage.html",{'objects': objects, 'start_index': start_index,'title':"All Loans",'showgraph':True,'loanstitle':loansTitle,'loansCount':numberOfLoans,'totalLoans':allLoansVariableCopy,'loansAmountTitle':loansAmountTitle,'loansAmounts':loansAmounts,'AlltotalLoansAmount':AlltotalLoansAmount,'template':template,'isTrue':an})
   else:
     return render(request, "AllLoansPage.html", {'objects': [],'title':"All Loans",'template':template,'isTrue':an})



def showAllLoansGraph(request):
    a = "jiii"
    return render(request, "AllLoansGraph.html", {'data': a})
 
 
 #All DSA Records Count Logic
 
def business_Loans_Count(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/business_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
def business_Loans_ApprovedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/business_loan_refcode_ApprovedCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
   
def business_Loans_RejectedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/business_loan_refcode_RejectedCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
   
def education_Loans_Count(request,refCode):
   
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/EduViewsets/{refCode}/education_loan_refCode_LoansCount/')
   if response.status_code==200:
     
      return response.json()
   
   else: return None
   
   
def education_Loans_ApprovedCount(request,refCode):
   
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/EduViewsets/{refCode}/education_loan_refcode_ApprovedCount/')
   if response.status_code==200:
      
      return response.json()
   else: return None
   
   
def education_Loans_RejectedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/el/EduViewsets/{refCode}/education_loan_refcode_RejectedCount/')
   if response.status_code==200:
      return response.json()
   else: return None
   
   
# LAP............
def lap_Loans_Count(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/lapapi/{refCode}/business_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   
def lap_Loans_ApprovedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/lapapi/{refCode}/business_loan_refcode_ApprovedCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   
def lap_Loans_RejectedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/lapapi/{refCode}/business_loan_refcode_RejectedCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}

def home_Loans_Count(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/hlapi/{refCode}/business_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   
def home_Loans_ApprovedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/hlapi/{refCode}/business_loan_refcode_ApprovedCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   
def home_Loans_RejectedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/hlapi/{refCode}/business_loan_refcode_RejectedCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   

def per_Loans_Count(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/plapi/{refCode}/business_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   
def per_Loans_ApprovedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/plapi/{refCode}/business_loan_refcode_ApprovedCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   
def per_Loans_RejectedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/pl/plapi/{refCode}/business_loan_refcode_RejectedCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   

def car_Loans_Count(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/cl/ddproject/{refCode}/education_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   
def car_Loans_ApprovedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/cl/ddproject/{refCode}/education_loan_refcode_ApprovedCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
   
def car_Loans_RejectedCount(request,refCode):
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/cl/ddproject/{refCode}/education_loan_refcode_RejectedCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   
# Credit Card........................
def credit_Loans_Count(request,refCode):
   # print(f'{settings.SOURCE_PROJECT_URL}/lapapi/{refCode}/business_loan_refCode_LoansCount/')
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/business_loan_refCode_LoansCount/')
   if response.status_code==200:
      return response.json()
   else: return {'count':0}
   

   
   
#Dsa IDS......................................
def getAllDsaIds(request):
   res=requests.get(f'{settings.HR_SOURCE_URL}/api/mymodel/custom_giveRefCodeFranCodeAll/')
   if res.status_code==200:
      return res.json()
#Dsa IDS.................................... 
 
 
def AllLoansCount(refCode,date=None):
   # print(date)
  if not date:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_LoansCount/')
  else:
   # print(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_LoansCount/?date={date}')
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_LoansCount/?date={date}')
  if response.status_code==200:
      return response.json()

def AllApprovedLoansCount(refCode,date=None):
  if not date:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_ApprovedCount/')
  else:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_ApprovedCount/?date={date}')
  if response.status_code==200:
      return response.json()

def AllRejectedLoansCount(refCode,date=None):
  if not date:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_RejectedCount/')
  else:
   response=requests.get(f'{settings.SOURCE_PROJECT_URL}/bl/BusiViewsets/{refCode}/All_loan_refCode_RejectedCount/?date={date}')

  if response.status_code==200:
      return response.json()

 
 
 #All History Data...............................
def totalLoansCount(request):
   dsaIds=getAllDsaIds(request)
   listData=[]
   # if request.GET.get('date'):
   #    date=
   with ThreadPoolExecutor() as executor:
      for i in dsaIds:
         
      #Demo To find execution time...............
      #   busCount=business_Loans_Count(request,i.get('dsa_registerid'))
      #   busApprCount=business_Loans_ApprovedCount(request,i.get('dsa_registerid'))
      #   busrejectedCount=business_Loans_RejectedCount(request,i.get('dsa_registerid'))
        
        totalLoansCountedVal=executor.submit(AllLoansCount,i.get('dsa_registerid'),request.GET.get('date'))
        totalresult=totalLoansCountedVal.result()
        
        totalAppreovedLoans=executor.submit(AllApprovedLoansCount,i.get('dsa_registerid'),request.GET.get('date'))
        totalApprovedresult=totalAppreovedLoans.result()
        
        totalRejectedLoans=executor.submit(AllRejectedLoansCount,i.get('dsa_registerid'),request.GET.get('date'))
        totalRejectedresult=totalRejectedLoans.result()
        
      #   #Business...........................
      #   businessTotalLoansThread1 = executor.submit(business_Loans_Count, request,i.get('dsa_registerid'))
      #   businessTotalApprovedThread2=executor.submit(business_Loans_ApprovedCount,request,i.get('dsa_registerid'))
      #   businessTotalApprovedThread3=executor.submit(business_Loans_RejectedCount,request,i.get('dsa_registerid'))
        
      #   busCount=businessTotalLoansThread1.result()
      #   busApprCount=businessTotalApprovedThread2.result()
      #   busrejectedCount=businessTotalApprovedThread3.result()
        
      #   #Education...............................
      #   educationTotalLoansThread1 = executor.submit(education_Loans_Count, request,i.get('dsa_registerid'))
      #   educationTotalApprovedThread2=executor.submit(education_Loans_ApprovedCount,request,i.get('dsa_registerid'))
      #   educationTotalApprovedThread3=executor.submit(education_Loans_RejectedCount,request,i.get('dsa_registerid'))
        
      #   eduCount=educationTotalLoansThread1.result()
      #   eduApprvdCount=educationTotalApprovedThread2.result()
      #   eduRejectCount=educationTotalApprovedThread3.result()
        
        
      # #   LAP..................................
      #   lapTotalLoansThread1 = executor.submit(lap_Loans_Count, request,i.get('dsa_registerid'))
      #   lapTotalApprovedThread2=executor.submit(lap_Loans_ApprovedCount,request,i.get('dsa_registerid'))
      #   lapTotalApprovedThread3=executor.submit(lap_Loans_RejectedCount,request,i.get('dsa_registerid'))
        
      #   lapCount=lapTotalLoansThread1.result()
      #   lapApprvdCount=lapTotalApprovedThread2.result()
      #   lapRejectCount=lapTotalApprovedThread3.result()
         
         # Credit Card...............
        creditTotalLoansThread1 = executor.submit(credit_Loans_Count, request,i.get('dsa_registerid'))
        ccCount=creditTotalLoansThread1.result()
        
        
      # #   HomeLoan....................................
      
      #   homeTotalLoansThread1 = executor.submit(home_Loans_Count, request,i.get('dsa_registerid'))
      #   homeTotalApprovedThread2=executor.submit(home_Loans_ApprovedCount,request,i.get('dsa_registerid'))
      #   homeTotalApprovedThread3=executor.submit(home_Loans_RejectedCount,request,i.get('dsa_registerid'))
        
      #   homeCount=homeTotalLoansThread1.result()
      #   homeApprvdCount=homeTotalApprovedThread2.result()
      #   homeRejectCount=homeTotalApprovedThread3.result()
        
        
      #   # Personal....................................
      
      #   personalTotalLoansThread1 = executor.submit(per_Loans_Count, request,i.get('dsa_registerid'))
      #   personalTotalApprovedThread2=executor.submit(per_Loans_ApprovedCount,request,i.get('dsa_registerid'))
      #   personalApprovedThread3=executor.submit(per_Loans_RejectedCount,request,i.get('dsa_registerid'))
        
      #   personalCount=personalTotalLoansThread1.result()
      #   personalApprvdCount=personalTotalApprovedThread2.result()
      #   personalRejectCount=personalApprovedThread3.result()
        
        
        
      # #   CarLoan
      
      #    # Personal....................................
      
      #   carTotalLoansThread1 = executor.submit(car_Loans_Count, request,i.get('dsa_registerid'))
      #   carTotalApprovedThread2=executor.submit(car_Loans_ApprovedCount,request,i.get('dsa_registerid'))
      #   carApprovedThread3=executor.submit(car_Loans_RejectedCount,request,i.get('dsa_registerid'))
        
      #   carCount=carTotalLoansThread1.result()
      #   carApprvdCount=carTotalApprovedThread2.result()
      #   carRejectCount=carApprovedThread3.result()
        
        
        
        #Calculation..............................
      #   totalLoans=busCount.get('count')+eduCount.get('count')+lapCount.get('count')+homeCount.get('count')+personalCount.get('count')+carCount.get('count')
      #   totalApprvdloans=busApprCount.get('count')+eduApprvdCount.get('count')+lapApprvdCount.get('count')+homeApprvdCount.get('count')+personalApprvdCount.get('count')+carApprvdCount.get('count')
      #   totalRejectdLoans=busrejectedCount.get('count')+eduRejectCount.get('count')+lapRejectCount.get('count')+homeRejectCount.get('count')+personalRejectCount.get('count')+carRejectCount.get('count')
      
        totalPendingLoans=totalresult.get('totalcount')-(totalApprovedresult.get('totalApprovedcount')+totalRejectedresult.get('totrejectedcount'))
        
        
        
        
        data={
           'registerId':i.get('dsa_registerid'),
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
           'creditcardtotalloans':ccCount.get('count'),
           
           'totalinsurance':totalresult.get('totalInsurances'),
           'allinsurance':totalresult.get('allinsurance'),
           'lifeinsurance':totalresult.get('lifeinsurance'),
           'generalinsurance':totalresult.get('generalinsurance'),
           'healthinsurance':totalresult.get('healthinsurance'),
              
           
        }
        listData.append(data)
   return JsonResponse(listData,safe=False)
      #   future_education = executor.submit(educationLoanApi, request)

    

    
def masterData(request):
   response=requests.get(f'{settings.SUPERADMIN_URL}/superadmin/app1/DSAMasterData_AppliViewsets/')
   result = response.json() if response.status_code in [200, 201] else None 
   
   result=result[0] if result else None
   return render(request, "MasterData.html", {'result': result})
