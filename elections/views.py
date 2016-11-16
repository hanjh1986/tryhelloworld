from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Candidate, Poll, Choice #models에 정의된 Candidate를 import
import datetime
from django.db.models import Sum
from django.http import HttpResponseNotFound #추가
from django.http import Http404 #추가
from django.shortcuts import get_object_or_404 #추가
from django.shortcuts import render_to_response

def custom_404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def index(request):
    candidates = Candidate.objects.all()
    context = {'candidates' : candidates} #context에 모든 후보에 대한 정보를 저장
    return render(request, 'elections/index.html', context) # context로 html에 모든 후보에 대한 정보를 전달

def areas(request, area):
    today = datetime.datetime.now()
    try :
        poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte=today) # get에 인자로 조건을 전달해줍니다.
        candidates = Candidate.objects.filter(area = area) # Candidate의 area와 매개변수 area가 같은 객체만 불러오기
    except:
        poll = None
        candidates = None
    context = {'candidates': candidates,
    'area' : area,
    'poll' : poll }
    return render(request, 'elections/area.html', context)

def polls(request, poll_id):
    poll = Poll.objects.get(pk = poll_id)
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()

    #return HttpResponse("finish")
    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area = area)
    polls = Poll.objects.filter(area = area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date

        # poll.id에 해당하는 전체 투표수
        total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))
        result['total_votes'] = total_votes['votes__sum']

        rates = [] #지지율
        for candidate in candidates:
            # choice가 하나도 없는 경우 - 예외처리로 0을 append
            try:
                choice = Choice.objects.get(poll = poll, candidate = candidate)
                rates.append(
                    round(choice.votes * 100 / result['total_votes'], 1)
                    )
            except :
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)

    context = {'candidates':candidates, 'area':area,
    'poll_results' : poll_results}
    return render(request, 'elections/result.html', context)

#def candidates(request, name):
#    try :
#        candidate = Candidate.object.get(name = name)
#    except:
#        return HttpResponseNotFound("없는 페이지 입니다.")
#    return HttpResponse(candidate.name)

#def candidates(request, name):
#    try :
#        candidate = Candidate.object.get(name = name)
#    except:
#        raise Http404
#    return HttpResponse(candidate.name)

def candidates(request, name):
    candidate = get_object_or_404(Candidate, name = name)
    return HttpResponse(candidate.name)
#def index(request):
#    candidates = Candidate.objects.all() #Candidate에 있는 모든 객체를 불러옵니다
#    str = "" #마지막에 return해 줄 문자열입니다.
#    for candidate in candidates:
#        str += "{}기호 {}번 ({})<BR>".format(candidate.name, candidate.party_number, candidate.area) #<BR>은 html에서 다음 줄로 이동하기 위해 쓰입니다.
#        str += candidate.introduction + "<P>" #<P>는 html에서 단락을 바꾸기 위해 쓰입니다.
#    return HttpResponse(str)
