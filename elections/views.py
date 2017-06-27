# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Candidate, Poll, Choice, User
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.template.context import RequestContext


# Create your views here
def index(request):
	candidates = Candidate.objects.all()
	context = {'candidates': candidates}
	return render(request, 'elections/index.html', context)

def areas(request, area):
	today = datetime.datetime.now()
	try:
		poll = Poll.objects.get(area = area, start_date__lte=
			today, end_date__gte=today)
		candidates = Candidate.objects.filter(area = area)
	except:
		poll = None
		candidates = None	
	context = {'candidates': candidates,
	'area': area,
	'poll': poll}
	return render(request,'elections/area.html',context)

def polls(request,poll_id):
	poll = Poll.objects.get(pk=poll_id)
	selection = request.POST['choice']
	

	try:
		choice = Choice.objects.get(poll_id = poll_id, candidate_id = selection)
		choice.votes +=1
		choice.save()
	except:
		choice = Choice(poll_id = poll_id, candidate_id = selection, votes = 1)
		choice.save()

	return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area = area)

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
        for candidate in candidates:
        	try:
	        	choice = Choice.objects.get(poll_id = poll.id, candidate_id = candidate.id)
	        	rates.append(
	        		round(choice.votes * 100/result['total_votes'],2)
	        		)
        	except:
        		rates.append(0)
        result['rates'] = rates
        poll_results.append(result)
   
    context = {'candidates': candidates, 'area' :area,
    'poll_results': poll_results}     
        
    return render(request, 'elections/result.html', context)

@csrf_exempt
def create_user(request):
	#import pdb;pdb.set_trace()
	id = request.POST['id']
	password = request.POST['password']
	
	user = User(id=id,password=password,authority=authority)
	user.save()
	return render(request,'elections/result.html')



def login(request):
	return render_to_response('login.html', locals(), RequestContext(request))

def authenticate(request):
	user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
	if user == None:
		return HttpResponse('username or password error')
	
	auth.login(request, user)
	return HttpResponseRedirect(request.POST.get('next', '/') or '/')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def signup(request):
	return render_to_response('signup.html', locals(), RequestContext(request))

def create(request):
	user = User.objects.create_user(username=request.POST['username'], 
									email=request.POST['email'],
									password=request.POST['password'])
	user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
	auth.login(request, user)
	return HttpResponseRedirect(request.POST.get('next', '/') or '/')
