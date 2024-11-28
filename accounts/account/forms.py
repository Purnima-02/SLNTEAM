from django import forms
from .models import *
class InputWindowForm(forms.ModelForm):
    class Meta:
        model=InputWindow
        fields='__all__'
        exclude=['disbursement']
        widgets={
    'payout_input_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
}

class OutputDisForm(forms.ModelForm):
    class Meta:
        model=Disbursement
        fields='__all__'
        exclude=['refCode','disbursement_detail','application_id','dsaIsClaim','franchCode','disbursement','input_window','date','appliCreatedAt','loan_amount','franchiseIsClaim','disbursedAmount']

class SettlementForm(forms.ModelForm):
    class Meta:
        model=SettlementWindow
        fields='__all__'
        exclude=['disbursement','refCode','application_id','franchCode','output_window','refid']
        widgets={
    'Settlement_Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
}
