from django.shortcuts import *
from .models import *
import datetime
from datetime import timedelta,timezone
from django.contrib.auth.decorators import login_required # login_required decorator
from django.contrib import messages

### Some Settings ###
BOXES = 53  # Total number of boxes in crossword
CORRECT_POINTS = 4  # Marks awarded on correct response
INCORRECT_POINTS = 1 # Marks deduced on incorrect response 
UNATTEMPT_POINTS = 0
TIME_ALLOTED = 2 # Time alloted for the quiz (in minutes)
######

@login_required
def dashboard(request):
    # messages.success(request, 'Your password was updated successfully!')
    return render(request,"dashboard.html",locals())


@login_required
def play(request):
    user_id = request.user
    objs = leaderboard.objects.filter(user=user_id, completed=True)

    if not objs.exists():
        if request.method == 'GET':
            user = leaderboard.objects.filter(user=user_id)    
            if not user.exists():
                user = leaderboard(
                user=user_id,
                )
                user.save()
                return redirect(reverse('play'))
            time_elapsed = datetime.datetime.now(timezone.utc) - user[0].started_at
            time_alloted = user[0].started_at + datetime.timedelta(minutes = TIME_ALLOTED)
            time_remaining = time_alloted - datetime.datetime.now(timezone.utc)
            time_remaining = round(time_remaining/ timedelta(minutes=1),2)
            if time_remaining <=0:
                messages.error(request, 'Time Over!')
                return redirect(reverse('results'))
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
            user.finished_at=datetime.datetime.now()    
            user.save()
        messages.success(request, 'Thank You! Check results.')
        return redirect(reverse('results'))    
    else:
        messages.warning(request, 'Completed! Check results.')
        return redirect(reverse('results'))
    return render(request,"start.html",locals())


@login_required
def results(request):
    time_taken = []
    users = leaderboard.objects.all().extra(select={
                                        'new_score': 'score IS NULL',
                                    },
                                    order_by=['new_score','-score'],
                                )
    for user in users:
        if user.finished_at is not None:
            time = user.finished_at - user.started_at
            time_taken.append(round(time/ timedelta(minutes=1),2))
        else:
            time_taken.append(None)

    data = zip(users,time_taken)
    
    return render(request,"leaderboard.html",locals())
