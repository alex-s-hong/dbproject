# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Poll, User, Choice, Purchase, Product
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User as auth_user
from django.template.context import RequestContext
from django.db import transaction

@csrf_exempt

def index(request):
	products = Product.objects.all()
	context = {'products': products}
	return render(request, 'elections/index.html', context)

@csrf_exempt
def areas(request, area):
	today = datetime.datetime.now()
	try:
		poll = Poll.objects.get(area = area, start_date__lte=
			today, end_date__gte=today)
		products = Product.objects.filter(area = area)
	except:
		poll = None
		products = None	
	context = {'products': products,
	'area': area,
	'poll': poll}
	return render(request,'elections/area.html',context)

@csrf_exempt
def polls(request,poll_id):
	#import pdb;pdb.set_trace()
	poll = Poll.objects.get(pk=poll_id)
	selection = request.POST['choice']
	

	try:
		choice = Choice.objects.get(poll_id = poll_id, product_id = selection)
		choice.votes +=1
		choice.save()
	except:
		choice = Choice(poll_id = poll_id, product_id = selection, votes = 1)
		choice.save()

	return HttpResponseRedirect("/areas/{}/results".format(poll.area))

@csrf_exempt
@transaction.atomic
def payment(request, product):
	product = Purchase.objects.get(product_id = product.id)
	buyer = request.POST['purchase']
	
	purchase = Purchase.objects.get(product_id = product.id, buyer = request.user.username)
	
	
	
	
@csrf_exempt
def results(request, area):
    products = Product.objects.filter(area = area)

    polls = Poll.objects.filter(area = area)
    #poll과 result 합쳐서 하나로 표현하기 
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))
        result['total_votes'] = total_votes['votes__sum']
        
        rates = []
        for product in products:
        	try:
	        	choice = Choice.objects.get(poll_id = poll.id, product_id = product.id)
	        	rates.append(
	        		round(choice.votes * 100/result['total_votes'],2)
	        		)
        	except:
        		rates.append(0)
        result['rates'] = rates
        poll_results.append(result)
   
    context = {'products': products, 'area' :area,
    'poll_results': poll_results}     
        
    return render(request, 'elections/result.html', context)

@csrf_exempt
def create_user(request):
	#import pdb;pdb.set_trace()
	print request.user.username
	id = request.POST['id']
	password = request.POST['password']
	
	user = User(id=id,password=password)
	user.save()
	return render(request,'elections/result.html')


@csrf_exempt
def login(request):
	return render_to_response('elections/login.html', locals(), RequestContext(request))

@csrf_exempt
def authenticate(request):
	#import pdb;pdb.set_trace()
	user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
	if user == None:
		return HttpResponse('username or password error')
	
	auth.login(request, user)
	return HttpResponseRedirect(request.POST.get('next', '/') or '/')
	
@csrf_exempt
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')
	
@csrf_exempt
def signup(request):
	return render_to_response('elections/signup.html', locals(), RequestContext(request))

@csrf_exempt
def create(request):
	user = User(username=request.POST['username'], 
									email=request.POST['email'],
									password=request.POST['password'],
									authority=request.POST['authorization'])
	user.save()
	user = auth_user.objects.create_user(request.POST['username'],
									request.POST['email'],
									request.POST['password']
									) 
	user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
	auth.login(request, user)
	return HttpResponseRedirect(request.POST.get('next', '/') or '/')



