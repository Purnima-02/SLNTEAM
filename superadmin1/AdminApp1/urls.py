from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from AdminApp1.App1RestApi import AdminViewsets,Admin_AppliViewsets,DSAMasterData_AppliViewsets,FranchiseMasterData_AppliViewsets


router=DefaultRouter()
router.register('AdminViewsets',AdminViewsets,basename='admin-view-sets')
router.register('adminApplicationViewsets',Admin_AppliViewsets,basename='adminappli-view-sets')
router.register('DSAMasterData_AppliViewsets',DSAMasterData_AppliViewsets,basename='DSAMasterData_AppliViewsets')
router.register('FranchiseMasterData_AppliViewsets',FranchiseMasterData_AppliViewsets,basename='FranchiseMasterData_AppliViewsets')


urlpatterns = [
    
    
    
     path('dashboard',dsaDashBoard,name='Dashboard'),
     
     # Apply Loans
    path('apply-business',apply_business,name="apply-business"),
    path('applyEducation',apply_Education,name='applyEducation'),
    path('apply-home',home_loan,name='apply-home'),
    path('creditapply',credit_card,name='creditapply'),
    path('applycar',car_loan,name='applyCar'),
    path('lap',lap,name='lap'),
    path('apply-personal',apply_personal,name='apply-personal'),
    path('applyGold',apply_gold,name='applyGold'),
    path('applyotherLoan',apply_otherLoan,name='applyotherLoan'),
# Apply Loans

 
    #  Insurance.........
     path('lifeInsurance',lifeInsurance,name='lifeInsurance'),
     path('generalInsurance',generalInsurance,name='generalInsurance'),
     path('healthInsurance',healthInsurance,name='healthInsurance'),
     path('allInsurance',allInsurance,name='allInsurance'),
     
     
     
     #  CheckEligiblity.........
     path('educheckEligible',educheckEligible,name='educheckEligible'),
     path('busicheckEligible',busicheckEligible,name='busicheckEligible'),
     path('lapcheckEligible',lapcheckEligible,name='lapcheckEligible'),
     path('homecheckEligible',homecheckEligible,name='homecheckEligible'),
     path('personalcheckEligible',personalcheckEligible,name='personalcheckEligible'),
     path('carcheckEligible',carcheckEligible,name='carcheckEligible'),
     path('creditcheckEligible',creditcheckEligible,name='creditcheckEligible'),
     path('goldcheckEligible',goldcheckEligible,name='goldcheckEligible'),
     path('othercheckEligible',othercheckEligible,name='othercheckEligible'),
     
     
     path("getAdmin/<str:register_id>",AdminViewsets.as_view({"get":"getByRegisterId"}),name="get-admin"),
     
     path('dsaTrack',dsaTrack,name='dsaTrack'),
     path('salesTrack',salesTrack,name='salesTrack'),
     path('getAllDsaIds',getAllDsaIds,name='getAllDsaIds'),
     path('demo',demo,name='demo'),
     
     path('franchiseTrack',franchiseTrack,name='franchiseTrack'),
     path('allFranchiseAmounts',allFranchiseAmounts,name='allFranchiseAmounts'),
     
     path('Indexpage',dashBoardIndexpage,name='dashBoardIndexpage'),
     
     
     path('HoBranchAllClosedData',slnHoBranchTotalLoansIncludingDSASales,name='slnHoBranchTotalLoansIncludingDSASales'),
     path('superadminLoansCount',slnSuperAdminTotalLoans,name='slnSuperAdminTotalLoans'),

     
    path('DsaMasterData',dsaMasterData,name='DsaMasterData'),
    path('FranchiseMasterData',franchiseMasterData,name='FranchiseMasterData'),
    path('AccountsMasterData',accountsMasterData,name='AccountsMasterData'),

    path('Login',superadminLogin,name='Login'),
    path('Logout',logOut,name='Logout'),
     path("",include(router.urls)),
     
    
]