from django.shortcuts import *
from .models import *
import datetime

### Some Settings ###
BOXES = 6  # Total number of boxes in crossword
CORRECT_POINTS = 5  # Marks awarded on correct response
INCORRECT_POINTS = 2 # Marks deduced on incorrect response 
UNATTEMPT_POINTS = 0
######

# Create your views here.
def play(request):
    user_id = request.user
    objs = leaderboard.objects.filter(user=user_id, completed=True)

    if not objs.exists():
        if request.method == 'GET':
            user = leaderboard(
                user=user_id,
                )
            user.save()
            user = leaderboard.objects.get(user=user_id)
            ideal_finish = user.started_at+ datetime.timedelta(minutes = 60)
            # now = datetime.datetime.now()
            # time_left = (ideal_finish - now) * days * 24 * 60
            print(ideal_finish)

            return render(request,"start.html",locals())
        else:
            score = 0
            for i in range(1,BOXES+1):
                response = str(request.POST.get(str(i), None))

                obj = answers.objects.get(q=str(i))

                if response == str(obj.ans):
                    score += CORRECT_POINTS
                elif response == '':
                    score += UNATTEMPT_POINTS
                else:
                    score -= INCORRECT_POINTS
            user = leaderboard.objects.get(user=user_id)
            user.score =score
            user.completed=True    
            user.save()
        return redirect(reverse('results'))    
    else:
        return redirect(reverse('results'))
    return render(request,"start.html",locals())



def results(request):
    return render(request,"leaderboard.html",locals())
