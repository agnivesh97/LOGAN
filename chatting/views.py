from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.serializers import json
#from openid.consumer.consumer import _httpResponseToMessage
import time
import json
from posts.models import *
from django.db.models import Q
# Create your views here.

def messagehtml(request):
    if request.session.get("sessionid",None):
        sessionid=request.session["sessionid"]
        user=People.objects.get(peopleid=sessionid)
        return render(request, "message.html", {'sessionid': sessionid,'user':user,'pic':request.session['sessionpic']})


def create_conversation(request,userid=None):
    if request.method=="POST":
        if request.session.get("sessionid",None):
            senderid=request.session['sessionid']
            receiverid=userid
            reply=json.loads(request.body.decode('utf-8'))["message_reply"]
            print("create")
            print(senderid)
            print(receiverid)
            try:
                entry_conversation_obj=list(conversation.objects.filter(Q(senderid=People(senderid),receiverid=People(receiverid))|Q(senderid=People(receiverid),receiverid=People(senderid))))
                print(entry_conversation_obj)
                entry_conversation_obj= entry_conversation_obj[0]
                conversationid=entry_conversation_obj.cid
            except Exception as e:
                entry_conversation_obj=conversation(senderid=People(senderid),receiverid=People(receiverid))
                entry_conversation_obj.save()
                entry_conversation_obj = conversation.objects.get(senderid=senderid, receiverid=receiverid)
                conversationid = entry_conversation_obj.cid
                print(e)
            entry_msg_obj=message(cid=conversation(conversationid),msgsenderid=People(senderid),msgreceiverid=People(receiverid),reply=reply)
            entry_msg_obj.save()

        return JsonResponse({'reply':reply},safe=False)

def load_conversation_list(request):
    if request.method=='POST':
        #receiverid=userid

        if request.session.get("sessionid",None):
            sessionid=request.session['sessionid']
            #sessionid=
            print(sessionid)
            try:
                conversation_context_list=[]
                conversation_obj=conversation.objects.filter(Q(receiverid=sessionid)|Q(senderid=sessionid))
                for convers in conversation_obj:
                    try:
                        conversation_context={}
                        convid = convers.cid
                        senderid = convers.senderid
                        message_main = message.objects.filter(msgsenderid=senderid,cid=convid).order_by('-mid').first()
                        message_reply=str(message_main)
                        print("start")
                        print(convers.receiverid)
                        print(convers.senderid)
                        print(sessionid)
                        if str(convers.senderid)==str(sessionid):
                            print("sakdak") 
                            user_obj=People.objects.get(peopleid=str(convers.receiverid))
                              
                        elif convers.senderid!=sessionid:
                            user_obj=People.objects.get(peopleid=str(senderid))
                            print("agniu")
                        username=user_obj.username
                        userid=user_obj.peopleid
                        conversation_context['userid']=userid
                        conversation_context['username']=username
                        conversation_context['message']=message_reply
                        conversation_context['user_pic']=user_obj.photo
                        conversation_context_list.append(conversation_context)
                        print(user_obj.peopleid)
                    except Exception as e:
                        print(e)
                        q = 0
            except Exception as e:
                print(e)
                p=0
    return JsonResponse(conversation_context_list,safe=False)


def load_messages(request,userid=None):
    if request.method=='POST':
        viewuserid=userid
        if request.session.get("sessionid",None):
            sessionid=request.session['sessionid']
            conversation_context_list = []

            try:
                conversation_obj = conversation.objects.filter(Q(senderid=sessionid,receiverid=viewuserid) | Q(receiverid=sessionid,senderid=viewuserid))
                for conver in conversation_obj:


                    convid = conver.cid
                    senderid=conver.senderid
                    receiverid=conver.receiverid


                    message_obj = message.objects.filter(Q(msgsenderid=senderid,msgreceiverid=receiverid,cid=convid)| Q(msgsenderid=receiverid,msgreceiverid=senderid,cid=convid) )
                    #print("The message object is"+str(message_obj))
                    for messages in message_obj:
                        messageid=messages.mid
                        message_reply = messages.reply
                        message_receiverid = messages.msgreceiverid
                        message_senderid=messages.msgsenderid
                        

                        #print("The message receiver id is "+str(message_receiverid)+"The message sender id is "+str(message_senderid))
                        user_obj1 = People.objects.get(peopleid=str(message_senderid))
                        user_obj2=People.objects.get(peopleid=str(userid))
                        #print("The first obj is"+str(user_obj1)+"The second obj is"+str(user_obj2))

                        sender_username = user_obj1.username
                        receiver_username=user_obj2.username

                        conversation_context = {}
                        conversation_context['sendername']=sender_username
                        conversation_context['receivername']=receiver_username
                        conversation_context['sessionuserid']=str(sessionid)
                        conversation_context['msgsenderid']=str(message_senderid)
                        conversation_context['msgreceiverid']=str(message_receiverid)
                        conversation_context['messageid']=messageid
                        conversation_context['message_reply']=message_reply
                        conversation_context['receiverpic']=user_obj2.photo
                        conversation_context['senderid']=sessionid
                        conversation_context['reciverid']=userid

                        #print (conversation_context)
                        conversation_context_list.append(conversation_context)

                        #print (conversation_context_list)




            except Exception as e:
                r=0
            return JsonResponse(conversation_context_list,safe=False)


def polling_message(request,userid=None):
    if request.method=="POST":
        if request.session.get("sessionid",None):
            viewuserid=userid
            sessionid=request.session['sessionid']
            receiverid = userid
            senderid = sessionid
            count_messages=0
            try:

                conversation_obj = conversation.objects.filter(Q(senderid=sessionid,receiverid=viewuserid) | Q(receiverid=sessionid,senderid=viewuserid))
                for conver in conversation_obj:
                    convid = conver.cid
                    senderid = conver.senderid
                    receiverid = conver.receiverid
                    message_obj = message.objects.filter(Q(msgsenderid=senderid, msgreceiverid=receiverid, cid=convid) | Q(msgsenderid=receiverid,msgreceiverid=senderid, cid=convid))
                    count_messages=count_messages+len(message_obj)

            except Exception as e:
                print(str(e))
            print(count_messages)
            return JsonResponse({'noofmessages':count_messages},safe=False)

