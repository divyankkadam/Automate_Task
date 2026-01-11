from django.core.mail import EmailMessage
from awd_main.celery import app
import time 
from django.core.management import call_command
from django.conf import settings
from . utils import generate_csv_file, send_email_notification

@app.task                 # make a function a Celery task.
def celery_test_task():
    time.sleep(10)
    #send email
    mail_subject = "Test subject"
    message = "This is Test email"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject , message , to_email)
    return 'Email send  SuccessFully'


@app.task
def import_data_task(file_path,model_name):
        try:
            call_command('importdata',file_path , model_name)  # To execute a custom management command from within your views 
        except Exception as e:
            raise e
        
        mail_subject = "Imported Data Completed"
        message = "Your data imported has been successful"
        to_email = settings.DEFAULT_TO_EMAIL
        send_email_notification(mail_subject , message , [to_email])
        return 'Data imported successfully.'

@app.task
def export_data_task(model_name):
        try:
            call_command('exportdata' , model_name)
        except Exception as e:
            raise e
        
        file_path = generate_csv_file(model_name)

        #send email with attachment
        mail_subject = 'Export Data Successful'
        message = "Export data sucessful. Please find the attachment"
        to_email = settings.DEFAULT_TO_EMAIL
        send_email_notification(mail_subject , message , [to_email] , attachment=file_path)
        return 'Export Data Task executed successfully.'
        
        

