from django.conf import settings
from django.shortcuts import redirect, render
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from .models import Subscriber
from . task import send_email_task  

# Create your views here.
def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST , request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()

            # send an email
            mail_subject = request.POST.get('subject')
            email_messages = request.POST.get('body')
            to_email = settings.DEFAULT_TO_EMAIL
            email_list = request.POST.get('email_list')

            # Access the selected email list
            email_list = email_form.email_list

            #Extract email address from the subscriber model in the selected email list
            subscriber = Subscriber.objects.filter(email_list=email_list)

            to_email = [ email.email_address for email in subscriber]
            print(to_email)

            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment = None

            # handover email sending task to celery
            send_email_task.delay(mail_subject,email_messages,to_email, attachment)
            
            # Display a success message
            messages.success(request , 'Email Send Successfully.')
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context = {
            'email_form' : email_form,
        }
        return render(request , 'emails/send-email.html' , context )


