import os
from django.db import models

# Create your models here.

class SuperAdmin(models.Model):
    adminId=models.CharField(max_length=100)
    adminBranch=models.CharField(max_length=100)


class SuperAdminApplications(models.Model):
    connection=models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, related_name='superadmin',blank=True,null=True)
    customer_applicationId=models.CharField(max_length=100)
    

class DSAMasterData(models.Model):
    MasterDataImage=models.FileField(upload_to='DSA/MasterData/')
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    def delete(self, *args, **kwargs):
        if self.MasterDataImage and os.path.isfile(self.MasterDataImage.path):os.remove(self.MasterDataImage.path)
        super(DSAMasterData, self).delete(*args, **kwargs)

class FranchiseMasterData(models.Model):
    MasterDataImage=models.FileField(upload_to='Franchise/MasterData/')
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    
    def delete(self, *args, **kwargs):
        if self.MasterDataImage and os.path.isfile(self.MasterDataImage.path):os.remove(self.MasterDataImage.path)
        super(FranchiseMasterData, self).delete(*args, **kwargs)

    

class AccountsMasterData(models.Model):
    MasterDataImage=models.FileField(upload_to='Accounts/MasterData/')
    created_at = models.DateField(auto_now_add=True,null=True,blank=True)
    
    def delete(self, *args, **kwargs):
        if self.MasterDataImage and os.path.isfile(self.MasterDataImage.path):os.remove(self.MasterDataImage.path)
        super(AccountsMasterData, self).delete(*args, **kwargs)
