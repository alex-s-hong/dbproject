# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Candidate, Poll, Choice, User
from django.views.decorators.csrf import csrf_exempt



import datetime


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
        
        poll_results.append(result)
   
    context = {'candidates': candidates, 'area' :area,
    'poll_results': poll_results}     
        
    return render(request, 'elections/result.html', context)

@csrf_exempt
def create_user(request):
	#import pdb;pdb.set_trace()
	id = request.POST['id']
	password = request.POST['password']
	
	user = User(id=id,password=password,authority=)
	user.save()
	return render(request,'elections/result.html')

	#str = ''
	#for candidate in candidate:
	#	str += "{} 기호 {}번 ({})<br>".format(candidate.name,
	#		candidate.party_number,
	#		candidate.area)
	#	str += candidate.introduction+"</p>"

	#return HttpResponse(str)
	
