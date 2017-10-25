#from django.http import HttpResponse
from django.core.serializers import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response
#from openid.consumer.consumer import _httpResponseToMessage
import json
import posts
#from posts import models

import time

# Create your views here.
from posts.models import *


def create_question(request,id=None):
    if request.method=='POST':
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        placeid=id
        questiontime=time.time()
        questiontxt=json.loads(request.body.decode('utf-8'))["newquestion"]
        print ("THE SESSION ID IS"+str(sessionid))
        entry_question=People_Question(
            questiontext=questiontxt,
            place_id=Place(placeid),
            userid=People(sessionid),

        )
        entry_question.save()
        return HttpResponse()



def create_answer(request,id=None):
    if request.method=='POST':
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        placeid=id
        answertxt=json.loads(request.body.decode('utf-8'))["answertxt"]
        answerqid=json.loads(request.body.decode('utf-8'))["answerqid"]
        answertime=time.time()
        entry_answer=People_Answer(
            answertext=answertxt,
            answerquesid=People_Question(answerqid),
            userid=People(sessionid),
            placeid=Place(placeid),
            time=answertime

        )
        entry_answer.save()
        noofanswers=len(People_Answer.objects.filter(answerquesid=answerqid))
        return JsonResponse({'quesid':answerqid,'noofanswers':noofanswers})

def qahtml(request):
    sessionid=request.session.get('sessionid', None)
    return render(request,"qa.html",{'sessionid':sessionid})


def del_question(request,id=None):
    if request.method=='POST':
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        placeid=id
        questionid=json.loads(request.body.decode('utf-8'))["qid"]
        try:
            del_obj=People_Question.objects.get(quesid=questionid,place_id=placeid,userid=sessionid)
            del_obj.delete()
        except Exception as e:
            p=0

    return HttpResponse()


def del_answer(request,id=None):
    if request.method=='POST':
        placeid=id
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        questionid=json.loads(request.body.decode('utf-8'))["qid"]
        answerid=json.loads(request.body.decode('utf-8'))["answerid"]
        try:
            del_ans_obj=People_Answer.objects.get(answerid=answerid,answerquesid=questionid,placeid=placeid,userid=sessionid)
            del_ans_obj.delete()
        except Exception as e:
            p=0
    return HttpResponse()

def edit_question(request,id=None):
    if request.method=='POST':
        placeid=id
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        questionid=json.loads(request.body.decode('utf-8'))["qid"]
        questiontxt=json.loads(request.body.decode('utf-8'))["questiontxt"]
        try:
            edit_obj=People_Question.objects.get(quesid=questionid,place_id=placeid,userid=sessionid)
            edit_obj.questiontext=questiontxt
            edit_obj.save()
        except Exception as e:
            p=0

    return HttpResponse()

def edit_answer(request,id=None):
    if request.method=='POST':
        placeid=id
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        questionid=json.loads(request.body.decode('utf-8'))["qid"]
        answerid=json.loads(request.body.decode('utf-8'))["answerid"]
        answertxt=json.loads(request.body.decode('utf-8'))['answertxt']
        #print (answertxt)
        try:
            edit_answer_obj=People_Answer.objects.get(answerid=answerid,answerquesid=questionid,placeid=placeid,userid=sessionid)
            edit_answer_obj.answertext=answertxt
            edit_answer_obj.save()
        except Exception as e:
            p=0

    return HttpResponse()



def load_question(request,id=None):

    placeid=id
    sessionid=0
    if request.session.get('sessionid',None):
            sessionid=request.session['sessionid']
    question_obj=People_Question.objects.filter(place_id=placeid)

    if question_obj:
        question_context_list=[]
        for question in question_obj:
            questiontxt=question.questiontext
            quesid=question.quesid
            userid=question.userid


            try:
                question_status_obj = People_Question_Status.objects.get(placeid=placeid,quesid=quesid,userid=sessionid)
                status = question_status_obj.status
                #print (status)
            except Exception as e:
                status = False


            try:
                question_status_obj_like=People_Question_Status.objects.filter(placeid=placeid,quesid=quesid,status=True)
                count_likes = len(question_status_obj_like)
            except Exception as e:
                count_likes=0



            count_answers = len(People_Answer.objects.filter(answerquesid=quesid))
            user_obj=People.objects.get(peopleid=str(userid))
            if user_obj:
                username=user_obj.username
                quserid=user_obj.peopleid
                pic=user_obj.photo

            #print(username+' '+str(quserid)+' '+str(placeid)+' '+questiontxt)
            question_context={}
            question_context_dictionary={}
            question_context['username']=username
            question_context['pic']=pic
            question_context['userid']=quserid
            question_context['placeid']=placeid
            question_context['sessionid']=sessionid
            question_context['questiontxt']=questiontxt
            #print(username + ' ' + str(quserid) + ' ' + str(placeid) + ' ' + questiontxt)
            question_context['quesid']=quesid
            #question_context['questiontime']=time
            question_context['status']=status
            question_context['nooflikes']=count_likes
            #question_context['noofunlikes']=count_unlikes
            question_context['noofanswers']=count_answers
            question_context_list.append(question_context)
            #question_context_dictionary['question_context_list']=question_context_list

    #print (question_context_list)
    #print(question_context_list)
    return JsonResponse(question_context_list,safe=False)


def load_answer(request,id=None):
    if request.method=='POST':
        sessionid=0
        #sessionid=request.session['sessionid']
        if  request.session.get('sessionid',None):
            
            sessionid=request.session['sessionid']
        placeid=id
        #answerquesid=json.loads(request.GET('quesid'))
        answerquesid=json.loads(request.body.decode('utf-8'))["quesid"]

        answer_obj=People_Answer.objects.filter(placeid=placeid,answerquesid=answerquesid)
        answer_context_list=[]

        if answer_obj:
            for answer in answer_obj:
                answertxt=answer.answertext
                answerid=answer.answerid
                answertime=answer.time
                userid=answer.userid
                try:
                    answer_status_obj=People_Answer_Status.objects.get(questionid=answerquesid,answerid=answerid,placeid=placeid,userid=sessionid)
                    answerstatus=answer_status_obj.answerstatus
                except Exception as e:
                    answerstatus=False

                try:
                    answer_status_obj_like=People_Answer_Status.objects.filter(questionid=answerquesid,answerid=answerid,placeid=placeid,answerstatus=True)
                    answer_count_like=len(answer_status_obj_like)
                except Exception as e:
                    answer_count_like=0

                user_obj=People.objects.get(peopleid=str(userid))
                if user_obj:
                    answerusername=user_obj.username
                    quserid=user_obj.peopleid
                    pic=user_obj.photo


                answer_context={}
                answer_context['username']=answerusername
                answer_context['pic']=pic
                answer_context['userid']=quserid
                answer_context['answerqid']=answerquesid
                answer_context['sessionid']=sessionid
                answer_context['answerid']=answerid
                answer_context['answertime']=answertime
                answer_context['answertxt']=answertxt
                answer_context['answerstatus']=answerstatus
                answer_context['placeid']=placeid
                answer_context['noofanswerlikes']=answer_count_like
                answer_context['iseditable']=False
                #answer_context['noofanswerunlike']=answer_count_unlike
                #print(answer_context['username']+" "+str(answer_context['userid'])+" "+str(answer_context['quesid'])+" "+answer_context['answertxt'])
                answer_context_list.append(answer_context)
        #print (answer_context_list)
        return JsonResponse(answer_context_list, safe=False)


newstatus=''
def voting(request,id=None):
    global newstatus
    if request.method=='POST':
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        placeid=id
        quesid=json.loads(request.body.decode('utf-8'))["quesid"]
        #print ("Code is coming till here")
        print("The question id is"+str(quesid))
        try:
            upvote_obj=People_Question_Status.objects.get(quesid=quesid,userid=sessionid,placeid=placeid)
            if upvote_obj:
                status = upvote_obj.status
                newreport=upvote_obj.report

                if status == False:

                    upvote_obj.status=True
                    upvote_obj.report=newreport
                    upvote_obj.save()
                    newstatus=True
                elif status==True:
                    upvote_obj.status=False
                    upvote_obj.report=newreport
                    upvote_obj.delete()
                    newstatus=False

        except Exception as e:
            entry_upvote = People_Question_Status(quesid=People_Question(quesid), status=True, userid=People(sessionid), placeid=Place(placeid),report='none')
            entry_upvote.save()
            newstatus=True

        #new_upvote_obj=People_Question_Status.objects.get(quesid=quesid,userid=sessionid,placeid=placeid)

        

        new_obj_status_like = People_Question_Status.objects.filter(quesid=quesid,placeid=placeid, status=True)
        count_new_obj_status_like = len(new_obj_status_like)
        context_like={}
        context_like['sessionid']=sessionid
        context_like['quesid']=quesid
        context_like['placeid']=placeid
        context_like['status']=newstatus
        context_like['nooflike']=count_new_obj_status_like
        #context_like['noofunlike']=count_new_downvote_obj_status_unlike

        return JsonResponse(context_like,safe=False)


def report(request,id=None):
    if request.method=='POST':
        placeid=id
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        quesid=json.loads(request.body.decode('utf-8'))["quesid"]
        newreport=json.loads(request.body.decode('utf-8'))["report"]
        #print (str(newreport)+" "+str(quesid))


        try:
            status_obj = People_Question_Status.objects.get(quesid=quesid, placeid=placeid, userid=sessionid)
            #print ("In the try section")
            status_obj.report=newreport

            status_obj.save()
        except Exception as e:
            entry_status_obj=People_Question_Status(quesid=People_Question(quesid),placeid=Place(placeid),userid=People(sessionid),report=newreport)
            #print ("In the exception state")
            entry_status_obj.save()


        return HttpResponse()





def downvoting(request):
    global newstatus
    if request.method == 'POST':
        sessionid = request.session['sessionid']
        placeid = request.POST['placeid']
        quesid = request.POST['quesid']

        downvote_obj = People_Question_Status.objects.get(quesid=quesid, userid=sessionid, placeid=placeid)
        if downvote_obj:
            status=downvote_obj.status
            if status == 'LIKE':
                downvote_obj.status='UNLIKE'
            elif status=='UNLIKE':
                downvote_obj.delete()
        else:
            entry_downvote = People_Question_Status(quesid=quesid, status='UNLIKE', userid=sessionid, placeid=placeid)
            entry_downvote.save()


        new_downvote_obj = People_Question_Status.objects.get(quesid=quesid, userid=sessionid, placeid=placeid)
        if new_downvote_obj:
            newstatus = new_downvote_obj.status
        elif not new_downvote_obj:
            newstatus=''
        new_downvote_obj_status_like=People_Question_Status.objects.get(quesid=quesid, userid=sessionid, placeid=placeid,status='LIKE')
        new_downvote_obj_status_unlike=People_Question_Status.objects.get(quesid=quesid, userid=sessionid, placeid=placeid,status='UNLIKE')
        count_new_downvote_obj_status_like=len(new_downvote_obj_status_like)
        count_new_downvote_obj_status_unlike=len(new_downvote_obj_status_unlike)

        context_unlike = {}
        context_unlike['sessionid'] = sessionid
        context_unlike['quesid'] = quesid
        context_unlike['placeid'] = placeid
        context_unlike['status'] = newstatus
        context_unlike['nooflike']=count_new_downvote_obj_status_like
        context_unlike['noofunlike']=count_new_downvote_obj_status_unlike
        return render_to_response(context_unlike)


newanswerstatus=''
def answervoting(request,id=None):
    global newanswerstatus
    if request.method=='POST':
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        quesid=json.loads(request.body.decode('utf-8'))["quesid"]
        placeid = id
        answerid=json.loads(request.body.decode('utf-8'))["answerid"]

        try:
            answer_upvote_obj=People_Answer_Status.objects.get(questionid=quesid,answerid=answerid,userid=sessionid,placeid=placeid)
            #print("In the try state " + str(quesid) + " " + str(answerid) + " " + str(sessionid))
            if answer_upvote_obj:
                answerstatus = answer_upvote_obj.answerstatus

                if answerstatus == False:

                    answer_upvote_obj.answerstatus = True
                    answer_upvote_obj.save()
                    newanswerstatus=True
                elif answerstatus == True:
                    answer_upvote_obj.answerstatus = False
                    answer_upvote_obj.delete()
                    newanswerstatus=False


        except Exception as e:
            #print ("In the exception state "+str(quesid)+" "+str(answerid)+" "+str(sessionid))
            entry_answer=People_Answer_Status(answerid=People_Answer(answerid),questionid=People_Question(quesid),placeid=Place(placeid),userid=People(sessionid),answerstatus=True,answerreport='none')
            entry_answer.save()
            newanswerstatus=True
            #print(entry_answer.answerstatus)
       
        new_answer_status_like = People_Answer_Status.objects.filter(questionid=quesid, answerid=answerid,placeid=placeid, answerstatus=True)

        count_new_answer_status_like = len(new_answer_status_like)

        context_answer_like={}
        context_answer_like['userid']=sessionid
        context_answer_like['placeid']=placeid
        context_answer_like['quesid']=quesid
        context_answer_like['answerid']=answerid
        context_answer_like['answerstatus']=newanswerstatus
        context_answer_like['noofanswerlike']=count_new_answer_status_like

        return JsonResponse(context_answer_like)


def answerreport(request,id=None):
    if request.method=='POST':
        placeid=id
        if not request.session.get('sessionid',None):
            return HttpResponse("Login required")
        sessionid=request.session['sessionid']
        quesid=json.loads(request.body.decode('utf-8'))['quesid']
        answerid=json.loads(request.body.decode('utf-8'))['answerid']
        newanswerreport=json.loads(request.body.decode('utf-8'))['answerreport']

        try:

            answer_status_obj=People_Answer_Status.objects.get(answerid=answerid,questionid=quesid,placeid=placeid,userid=sessionid)
            #print("In the try state " + str(quesid) + " " + str(answerid) + " " + str(sessionid))
            answer_status_obj.answerreport=newanswerreport
            answer_status_obj.save()

        except Exception as e:
            #print("In the exception state " + str(quesid) + " " + str(answerid) + " " + str(sessionid))
            entry_answer_status_obj=People_Answer_Status(answerid=People_Answer(answerid),questionid=People_Question(quesid),placeid=Place(placeid),userid=People(sessionid),answerreport=newanswerreport)
            entry_answer_status_obj.save()

        return HttpResponse()


def answerdownvoting(request):
    global newanswerstatus
    if request.method=='POST':
        sessionid=request.session['sessionid']
        quesid=request.session['quesid']
        placeid = request.POST['placeid']
        answerid=request.POST['answerid']
        answer_downvote_obj=People_Answer_Status.objects.get(quesid=quesid,answerid=answerid,userid=sessionid,placeid=placeid)

        if answer_downvote_obj:
            answerstatus=answer_downvote_obj.answerstatus
            if answerstatus=='LIKE':
                answer_downvote_obj.answerstatus='UNLIKE'
            elif answerstatus=='UNLIKE':
                answer_downvote_obj.delete()
        else:
            entry_answer=People_Answer_Status(answerid=answerid,quesid=quesid,placeid=placeid,userid=sessionid,answerstatus='UNLIKE')
            entry_answer.save()
        new_answer_downvote_obj = People_Answer_Status.objects.get(quesid=quesid, answerid=answerid, userid=sessionid,
                                                                     placeid=placeid)
        if new_answer_downvote_obj:
            newanswerstatus=new_answer_downvote_obj.answerstatus

        elif not new_answer_downvote_obj:
            newanswerstatus=''
        new_answer_status_like=People_Answer_Status.objects.get(quesid=quesid, answerid=answerid, userid=sessionid,
                                                                     placeid=placeid,answerstatus='LIKE')
        new_answer_status_unlike = People_Answer_Status.objects.get(quesid=quesid, answerid=answerid,
                                                                        userid=sessionid,
                                                                        placeid=placeid, answerstatus='UNLIKE')
        count_new_answer_status_like=len(new_answer_status_like)
        count_new_answer_status_unlike=len(new_answer_status_unlike)

        context_answer_unlike={}
        context_answer_unlike['userid']=sessionid
        context_answer_unlike['placeid']=placeid
        context_answer_unlike['quesid']=quesid
        context_answer_unlike['answerid']=answerid
        context_answer_unlike['answerstatus']=newanswerstatus
        context_answer_unlike['noofanswerlike']=count_new_answer_status_like
        context_answer_unlike['noofanswerunlike']=count_new_answer_status_unlike
        return render_to_response(context_answer_unlike)



def create_review(request):
    if request.method=='POST':
        userid=request.session['sessionid']
        placeid=request.POST['placeid']
        reviewtxt=request.POST['reviewtxt']
        entry_review_obj=Review(user_id=userid,placeid=placeid,review_text=reviewtxt)
        entry_review_obj.save()



def load_review(request):
    if request.method=='POST':
        sessionid=request.session['sessionid']
        placeid=request.POST['placeid']
        review_obj=Review.objects.get(user_id=sessionid,placeid=placeid)
        review_context_list=[]
        if review_obj:
            for review in review_obj:
                reviewid=review.review_id
                reviewtxt=review.review_text
                placeid=review.placeid
                userid=review.user_id
                user_obj=People(peopleid=userid)
                review_status_obj=Review_status.objects.get(review_id=reviewid,user_id=sessionid,placeid=placeid)
                review_status_obj_like=Review_status.objects.get(review_id=reviewid,user_id=sessionid,placeid=placeid,status='LIKE')
                review_status_obj_unlike=Review_status.objects.get(review_id=reviewid,user_id=sessionid,placeid=placeid,status='UNLIKE')
                count_review_like=len(review_status_obj_like)
                count_review_unlike=len(review_status_obj_unlike)
                if review_status_obj:
                    reviewstatus=review_status_obj.status
                elif not review_status_obj:
                    reviewstatus=''
                if user_obj:
                    username=user_obj.peopleid
                    reviewuserid=user_obj.peopleid
                review_context={}
                review_context['reviewid']=reviewid
                review_context['reviewtxt']=reviewtxt
                review_context['placeid']=placeid
                review_context['userid']=reviewuserid
                review_context['username']=username
                review_context['reviewstatus']=reviewstatus
                review_context['noofreviewlike']=count_review_like
                review_context['noofreviewunlike']=count_review_unlike
                review_context_list.extend(review_context)
        return  render_to_response(review_context_list)

newreviewstatus=''

def review_upvote(request):
    global newreviewstatus
    if request.method=='POST':
        sessionid=request.session['sessionid']
        placeid=request.POST['placeid']
        reviewid=request.POST['reviewid']
        review_obj=Review.objects.get(user_id=sessionid,placeid=placeid,review_id=reviewid)
        if review_obj:
            review_status=review_obj.status
            if review_status=='UNLIKE':
                review_obj.status='LIKE'
            elif review_status=='LIKE':
                review_obj.delete()
        else:
            entry_review_status=Review_status(review_id=reviewid,user_id=sessionid,placeid=placeid,status='LIKE')
            entry_review_status.save()
        new_review_obj=Review_status.objects.get(user_id=sessionid,placeid=placeid,review_id=reviewid)
        if new_review_obj:
            newreviewstatus=new_review_obj.status
        elif not new_review_obj:
            newreviewstatus=''
        count_new_review_object_like = Review.objects.get(user_id=sessionid, placeid=placeid, review_id=reviewid,
                                                          status='LIKE')
        count_new_review_object_unlike = Review.objects.get(user_id=sessionid, placeid=placeid, review_id=reviewid,
                                                            status='UNLIKE')
        no_of_review_like = len(count_new_review_object_like)
        no_of_review_unlike = len(count_new_review_object_unlike)
        context_review={}
        context_review['userid']=sessionid
        context_review['placeid']=placeid
        context_review['reviewid']=reviewid
        context_review['status']=newreviewstatus
        context_review['noofreviewlike']=no_of_review_like
        context_review['noofreviewunlike']=no_of_review_unlike

        return  render_to_response(context_review)


def review_downvote(request):
    global newreviewstatus
    if request.method == 'POST':
        sessionid = request.session['sessionid']
        placeid = request.POST['placeid']
        reviewid = request.POST['reviewid']
        review_obj = Review.objects.get(user_id=sessionid, placeid=placeid, review_id=reviewid)
        if review_obj:
            review_status = review_obj.status
            if review_status == 'LIKE':
                review_obj.status = 'UNLIKE'
            elif review_status == 'UNLIKE':
                review_obj.delete()
        else:
            review_status = Review_status(review_id=reviewid, user_id=sessionid, placeid=placeid, status='UNLIKE')
            review_status.save()
        new_review_obj = Review.objects.get(user_id=sessionid, placeid=placeid, review_id=reviewid)
        if new_review_obj:
            newreviewstatus = new_review_obj.status
        elif not  new_review_obj:
            newreviewstatus=''
        count_new_review_object_like=Review.objects.get(user_id=sessionid, placeid=placeid, review_id=reviewid,status='LIKE')
        count_new_review_object_unlike=Review.objects.get(user_id=sessionid, placeid=placeid, review_id=reviewid,status='UNLIKE')
        no_of_review_like=len(count_new_review_object_like)
        no_of_review_unlike=len(count_new_review_object_unlike)

        context_review = {}
        context_review['userid'] = sessionid
        context_review['placeid'] = placeid
        context_review['reviewid'] = reviewid
        context_review['status'] = newreviewstatus
        context_review['noofreviewlike']=no_of_review_like
        context_review['noofreviewunlike']=no_of_review_unlike
        return render_to_response(context_review)



