# models.py

from django.db import models

class DisbursementData(models.Model):
    application_id = models.CharField(max_length=100)  
    fran_code = models.CharField(max_length=100,null=True,blank=True)
    dsa_code = models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=1000,default='')
    refid=models.CharField(max_length=500,null=True,blank=True)
    franchrefid=models.CharField(max_length=400,null=True,blank=True)
    created_at=models.DateField(null=True,blank=True)
    def __str__(self):
        return f"{self.application_id} - {self.fran_code} - {self.dsa_code}"
    
from datetime import date
class DisbursementDetail(models.Model):
    disbursement = models.OneToOneField(DisbursementData, on_delete=models.CASCADE, related_name='detail')
    bank_nbfc_name=models.CharField(max_length=50,null=True,blank=True)
    bank_loginid=models.CharField(max_length=20,null=True,blank=True)
    location=models.CharField(max_length=20,null=True,blank=True)
    loan_amount=models.CharField(max_length=20,null=True,blank=True)
    disbursement_date=models.DateField(default=date.today)
    tenure=models.CharField(max_length=50,null=True,blank=True)
    roi=models.CharField(max_length=50,null=True,blank=True)
    insurance=models.CharField(max_length=50,null=True,blank=True)
    net_disbursement=models.CharField(max_length=50,null=True,blank=True)
    bank_person_name=models.CharField(max_length=50,null=True,blank=True)
    mobile_no=models.CharField(max_length=10,null=True,blank=True)
    comment=models.TextField(max_length=500,null=True,blank=True)
    def __str__(self):
        return f"{self.bank_nbfc_name} - {self.disbursement.application_id}"
    

class InputWindow(models.Model):
    disbursement = models.ForeignKey(DisbursementData, on_delete=models.CASCADE, related_name='input_windows')
    payout_slab_amount_or_percentage = models.CharField(max_length=10)
    payout_input_date = models.DateTimeField(null=True,blank=True)
    UTR_number = models.CharField(max_length=30)
    credited_bank_name = models.CharField(max_length=50)
    credited_bank_ac_number = models.CharField(max_length=20)
    TDS = models.CharField(max_length=50)
    net_loan_amount = models.DecimalField(max_digits=10, decimal_places=0,default=0.00)
    net_amount_received = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)

class Disbursement(models.Model):
    disbursement = models.ForeignKey(DisbursementData, on_delete=models.CASCADE, related_name='output_windows',null=True,blank=True)
    disbursement_detail=models.ForeignKey(DisbursementDetail,on_delete=models.CASCADE,null=True,blank=True,related_name='output_windows')
    input_window=models.ForeignKey(InputWindow,on_delete=models.CASCADE,null=True,related_name='output_windows',blank=True)
    branch_payout_slab_in_Rs = models.CharField(max_length=20, null=True, blank=True)
    dsa_payout_slab_in_Rs = models.CharField(max_length=50, null=True, blank=True)
    refCode=models.CharField(max_length=1000,null=True,blank=True)
    franchCode=models.CharField(max_length=1000,null=True,blank=True)
    application_id=models.CharField(max_length=1000,null=True)
    dsaIsClaim=models.BooleanField(default=False,null=True,blank=True)
    franchiseIsClaim=models.BooleanField(default=False,null=True,blank=True)
    dateClaimed=models.DateField(auto_now_add=True)
    loan_amount=models.CharField(max_length=100,null=True,blank=True)
    disbursedAmount=models.CharField(max_length=100,null=True)
    created_at=models.DateField(auto_now_add=True)
    date= models.DateField(null=True,blank=True)
    appliCreatedAt=models.DateField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.disbursement_detail:
            self.date = self.disbursement_detail.disbursement_date
            self.loan_amount = self.input_window.net_loan_amount
            self.disbursedAmount=self.input_window.net_amount_received
        
        if self.disbursement:
            self.appliCreatedAt = self.disbursement.created_at

        print(self.application_id)
        super(Disbursement, self).save(*args, **kwargs)


class SettlementWindow(models.Model):
    disbursement = models.ForeignKey(DisbursementData, on_delete=models.CASCADE, related_name='settle_windows',blank=True,null=True)
    output_window=models.ForeignKey(Disbursement,on_delete=models.CASCADE,null=True,related_name='settle_windows')
    application_id=models.CharField(max_length=1000)
    refCode=models.CharField(max_length=1000,null=True,blank=True)
    franchCode=models.CharField(max_length=1000,null=True,blank=True)
    Settlement_Date=models.DateField(default=date.today)
    UTR_Number=models.CharField(max_length=30)
    dsa_Amount_in_Rs=models.PositiveIntegerField(null=True,blank=True)
    franch_Amount_in_Rs=models.PositiveIntegerField(null=True,blank=True)
    DR_From_Bank=models.CharField(max_length=100)
    Settlement_By=models.CharField(max_length=100)
    DR_Bank_Account_Number=models.CharField(max_length=20)
   
    created_at=models.DateField(auto_now_add=True)



