# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.template import Context
import datetime
from django.http import HttpResponse
import re

from .forms import *
from .models import *


def health(request):
    return HttpResponse("3")

@login_required
def index(request):
    template_name = 'ics_tool/home.html'

    if request.method == "GET":
        cnt = Donors.objects.count()
        dnt = Donations.objects.count()
        return render(request, template_name, {'cnt':cnt, 'dnt':dnt})

    form = SearchDataForm(request.POST)
    if form.is_valid():

      results = 'Welcome'

      return render(request,'ics_tool/home.html',{'Results' : results})

    print(form.errors)

    return render(request,'ics_tool/home.html',{})


@login_required
def add_donor(request):
    template_name = 'ics_tool/add_donor.html'

    if request.method == "GET":
        return render(request, template_name)

    form = AddDonorForm(request.POST)
    if form.is_valid():
      OrganizationName = request.POST.get('OrganizationName', '')
      Salutation       = request.POST.get('Salutation', '')
      FirstName        = request.POST.get('FirstName', '')
      LastName         = request.POST.get('LastName', '')
      Email            = request.POST.get('Email', '')
      PhoneNumber      = request.POST.get('PhoneNumber', '')
      Comments         = request.POST.get('Comments', '')
      StreetAddress    = request.POST.get('StreetAddress', '')
      City             = request.POST.get('City', '')
      State            = request.POST.get('State', '')
      Zip              = request.POST.get('Zip', '')
      ICS              = request.POST.get('ICS', '')
        
      try:
          d = Donors.objects.get(FirstName=FirstName,LastName=LastName,Email=Email)
          return render(request,'ics_tool/add_donor.html',{'Error':'Name and Email Combination Exist'})
      except Exception as e:
          print (e)
          pass
  

      LoadDonorObj = Donors(OrganizationName=OrganizationName,Salutation=Salutation,FirstName=FirstName,LastName=LastName,
                            Email=Email,PhoneNumber=PhoneNumber,Comments=Comments,StreetAddress=StreetAddress,City=City,State=State,Zip=Zip,ICS=ICS)
      LoadDonorObj.save()

      return render(request,'ics_tool/donor_success.html',{})

    print(form.errors)

    return render(request,'ics_tool/add_donor.html',{})

@login_required
def edit_donor(request):
    template_name = 'ics_tool/add_donor.html'

    if request.method == "GET":
        pid = request.GET.get('id','')
        donors = Donors.objects.get(id=pid)
        return render(request, 'ics_tool/edit_donor.html',{'donors':donors})

    form = AddDonorForm(request.POST)
    if form.is_valid():
      pid              = request.POST.get('id','')
      OrganizationName = request.POST.get('OrganizationName', '')
      Salutation       = request.POST.get('Salutation', '')
      FirstName        = request.POST.get('FirstName', '')
      LastName         = request.POST.get('LastName', '')
      Email            = request.POST.get('Email', '')
      PhoneNumber      = request.POST.get('PhoneNumber', '')
      Comments         = request.POST.get('Comments', '')
      StreetAddress    = request.POST.get('StreetAddress', '')
      City             = request.POST.get('City', '')
      State            = request.POST.get('State', '')
      Zip              = request.POST.get('Zip', '')
      ICS              = request.POST.get('ICS', '')

      d = Donors.objects.get(id=pid)

      d.OrganizationName=OrganizationName
      d.Salutation=Salutation
      d.FirstName=FirstName
      d.LastName=LastName
      d.Email=Email
      d.PhoneNumber=PhoneNumber
      d.Comments=Comments
      d.StreetAddress=StreetAddress
      d.City=City
      d.State=State
      d.Zip=Zip
      d.ICS=ICS
      d.save()

      return render(request,'ics_tool/search_donor.html',{})

    print(form.errors)

    return render(request,'ics_tool/search_donor.html',{})

@login_required
def search_donor(request):

    template_name = 'ics_tool/search_donor.html'

    if request.method == "GET":
        return render(request, template_name)

    form = SearchDonorForm(request.POST)
    if form.is_valid():
      SearchQuery = request.POST.get('SearchQuery', '')

      results = Donors.objects.filter(Q(FirstName__icontains=SearchQuery)).values()

      return render(request,'ics_tool/donor_results.html',{'Results' : results})

    print(form.errors)

    return render(request,'ics_tool/search_donor.html',{})

@login_required
def feedback(request):

    template_name = 'ics_tool/feedback.html'

    if request.method == "GET":
        return render(request, template_name)

    form = FeedbackForm(request.POST)
    if form.is_valid():
      SearchQuery = request.POST.get('SearchQuery', '')
      LoadDonorObj = Feedback(Feedback=SearchQuery)
      LoadDonorObj.save()
      return render(request,'ics_tool/home.html',{})

    print(form.errors)

    return render(request,'ics_tool/home.html',{})

@login_required
def add_inkind(request):
    template_name = 'ics_tool/add_inkind.html'

    if request.method == "GET":
       results = []
       try:
          Donor = Donors.objects.all()
          for list in Donor:
              a ={}
              a['Donor']   = list.FirstName + ' ' + list.LastName + ' | ' + list.Email
              a['DonorId'] = list.id
              results.append(a)
          return render(request, template_name,{'Results': results})	 
       except Exception as e:
          return render(request, template_name,{'Error': e})

    if request.method == 'POST':
       Donor          = request.POST.get('Donor', '')
       DonationDate   = datetime.datetime.strptime(request.POST.get('DonationDate', ''), '%m/%d/%Y').strftime('%Y-%m-%d')
       DonationAmount = request.POST.get('DonationAmount', '')
       Description    = request.POST.get('Description', '')
	
       try:
         LoadDonationsObj = Donations(donor_id_id=int(Donor),donation_date=DonationDate,comments=Description)
         LoadDonationsObj.save()
         donations = Donations.objects.get(pk=LoadDonationsObj.pk)  
         LoadInkindObj    = InKind(donationID_id=LoadDonationsObj.pk,description=Description,approxValue=DonationAmount)
         return render(request,'ics_tool/add_inkind.html',{'Success':'Success'})
       except Exception as e:
         return render(request,'ics_tool/add_inkind.html',{'Error':e})

	
@login_required
def add_items(request):
    template_name = 'ics_tool/add_items.html'

    if request.method == "GET":
       results = []
       try:
          Donor = Donors.objects.all()
          for list in Donor:
              a ={}
              a['Donor']   = list.FirstName + ' ' + list.LastName + ' | ' + list.Email
              a['DonorId'] = list.id
              results.append(a)
          return render(request, template_name,{'Results': results})	 
       except Exception as e:
          return render(request, template_name,{'Error': e})

    if request.method == 'POST':
        Donor        = request.POST.get('Donor', '')
        Grocery      = request.POST.get('Grocery', '')
        Meat         = request.POST.get('Meat', '')
        Bread        = request.POST.get('Bread', '')
        Produce      = request.POST.get('Produce', '')
        Toiletries   = request.POST.get('Toiletries', '')
        Diaper       = request.POST.get('Diaper', '')
        Other        = request.POST.get('Other', '')
        TotalPounds  = request.POST.get('TotalPounds', '')
        DonationDate = datetime.datetime.strptime(request.POST.get('DonationDate', ''), '%m/%d/%Y').strftime('%Y-%m-%d')
        ItemsDescription = request.POST.get('ItemsDescription', '')
	
        try:
         LoadDonationsObj = Donations(donor_id_id=int(Donor),donation_date=DonationDate,comments=Description)
         LoadDonationsObj.save()
         donations = Donations.objects.get(pk=LoadDonationsObj.pk)  
         LoadCatDonationsObj    = CatDonations(donationID_id=LoadDonationsObj.pk,desc=ItemsDescription,Grocery=Grocery,Meat=Meat,Bread = Bread, 
				 Produce=Produce,Toiletries=Toiletries,Diaper= Diaper, Other = Other, TotalPounds=TotalPounds)
         return render(request,'ics_tool/add_items.html',{'Success':'Success'})
        except Exception as e:
         return render(request,'ics_tool/add_items.html',{'Error':e})

def add_events(request):
    return HttpResponse("3")

@login_required
def donor_report(request):
    Donor = Donors.objects.all()
    results = []
    for list in Donor:
        a ={}
        a['FN']   = list.FirstName 
        a['LN']   = list.LastName 
        a['EM']   = list.Email
        a['PN'] = list.PhoneNumber
        a['AD'] = list.StreetAddress + ',' + list.City
        results.append(a)
    return render(request, 'ics_tool/donor_report.html',{'Results': results})

@login_required
def donation_report(request):
	
	CatDonation = CatDonations.objects.all()
	results = []
	for list in CatDonation:
		a = {}
		a['DI'] = list.donationID   
		a['GR'] = list.Grocery 
		a['MT'] = list.Meat
		a['BR'] = list.Bread
		a['PR'] = list.Produce
		a['TL'] = list.Toiletries
		a['DIA'] = list.Diaper
		a['PN'] = list.TotalPounds 
		results.append(a)
	return render(request,'ics_tool/donation_report.html',{'Results': results})
	


