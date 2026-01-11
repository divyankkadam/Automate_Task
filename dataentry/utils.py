import csv
import datetime
import hashlib
import os
import time
from django.apps import apps
from django.conf import settings
from django.db import DataError
from django.core.management.base import CommandError
from django.core.mail import EmailMessage

from emails.models import Email, EmailTracking , Sent, Subscriber
from bs4 import BeautifulSoup

# Helper function  - A helper function is a small reusable function that performs a specific task to support the main program logic and improve code readability and maintainability.
def get_all_custom_models():
    default_models = ['ContentType' , 'Session' , 'LogEntry' , 'Group' , 'Permission' , 'User' , 'Upload']

    custom_models = []
    for model in apps.get_models():
        
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models
    


def check_csv_errors(file_path,model_name):

    #search for model across all instal app
    model  = None
    for app_config in apps.get_app_configs():                            #  is a method used to retrieve the configuration object ( app_config ) for a specific installed application. 
        # try to serach for models 
        try:
            model = apps.get_model(app_config.label , model_name )       # Returns the Model with the given model_name , label . 
            break                                                        # stop searching if found
        except LookupError:
            continue                                                     # model not found in this app , continue searching in app

    if not model:
        raise CommandError(f"Model {model_name} not found in any app")   # to provide a clean, readable failure message to the user in the terminal

    # Compare CSV header with model's fields names
    # get all fields name of the model that we found 
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']

    try:
        with open(file_path , 'r') as file:
            reader = csv.DictReader(file)                                    # DictReader - reading a CSV file and mapping the information in each row to a dictionary and return a iterator
            csv_header = reader.fieldnames
            
            # compare csv header with model field name 
            if csv_header != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields")
    except Exception as e:
        raise e
    
    # Notify by user by email

    
    return model


def send_email_notification(mail_subject, message, to_email , attachment=None , email_id=None ):
    try:
        from_email  = settings.DEFAULT_FROM_EMAIL
        for recipient_email in to_email :
            new_message = message
            # Create Email Tracking record 
            if email_id  :
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list , email_address = recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()

                email_tracking = EmailTracking.objects.create(
                    email = email ,
                    subscriber = subscriber,
                    unique_id = unique_id,   
                )
                
                base_url = settings.BASE_URL
                # Generate the tracking pixel 
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"

                # Search for link in the email body 
                soup = BeautifulSoup(message, 'html.parser')
                urls = [a['href'] for a in soup.find_all('a' , href=True)]

                # If there are link or url in emial body, inject our click tracking url to that original link
                if urls:
                    for url in urls:
                        # make the final tracking url
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}",f"{tracking_url}")
                else :
                    print("No URL found in email body")
                
                # Create the email content with tracking  pixel image
                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'>" 
                new_message += open_tracking_img
                
            mail = EmailMessage(mail_subject, new_message, from_email , to=[recipient_email])
            if attachment is not None:
                mail.attach_file(attachment)
            
            mail.content_subtype = "html"
            mail.send()

        # Store the total sent emails inside the Sent model 
        if email_id :
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
        
    except Exception as e:
        raise e
    

    
    


def generate_csv_file(model_name):
    #generate the timestamp of current date and time 
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # define the csv file name/path

    export_dir = 'exported_data'
    file_name = f"exported_{model_name}_data_{timestamp}.csv"
    file_path = os.path.join(settings.MEDIA_ROOT,export_dir,file_name)
    print('File path' , file_path)
    return  file_path
 
