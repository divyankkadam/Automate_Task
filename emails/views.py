from django.conf import settings
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from .models import Email, EmailTracking, Sent, Subscriber
from . task import send_email_task  
from django.db.models import Sum
from django.utils import timezone

# Create your views here.
def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST , request.FILES)
        if email_form.is_valid():
            email = email_form.save()

            # send an email
            mail_subject = request.POST.get('subject')
            email_messages = request.POST.get('body')
            to_email = settings.DEFAULT_TO_EMAIL
            email_list = request.POST.get('email_list')

            # Access the selected email list
            email_list = email.email_list

            #Extract email address from the subscriber model in the selected email list
            subscriber = Subscriber.objects.filter(email_list=email_list)

            to_email = [ email.email_address for email in subscriber]
            print(to_email)

            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None

            email_id = email.id
            print(email_id)
            # handover email sending task to celery
            send_email_task.delay(mail_subject,email_messages,to_email, attachment , email_id)
            
            # Display a success message
            messages.success(request , 'Email Send Successfully.')
            return redirect('send_email')
        else:
            messages.error(request, "Form is not valid")
            return redirect('send_email')
    else:
        email = EmailForm()
        context = {
            'email_form' : email,
        }
        return render(request , 'emails/send-email.html' , context )



def track_click(request, unique_id ):
    # Login to store the tracking info
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        url = request.GET.get('url')
        # check if clicked_at field is already set or not
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)
    except:
        return HttpResponse('Email Tracking record not found!')
    



def track_open(request, unique_id ):
    # Logic to store the tracking info
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # check if opened_at field is already set or not
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse('Email opened Successfully')
        else:
            print('Email alredy opened')
            return HttpResponse('Email already opened')
    except:
        return HttpResponse('Email Tracking record not found!')




def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')).order_by('-sent_at')

    context = {
        'emails' : emails,
    }
    return render(request , 'emails/track_dashboard.html' , context ) 
 


def track_stats(request,pk):
    email = get_object_or_404(Email , pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'email':email,
        'total_sent':sent.total_sent,
    }

    return render(request , 'emails/track_stats.html',context)

