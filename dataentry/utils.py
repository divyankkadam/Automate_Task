import csv
from django.apps import apps
from django.conf import settings
from django.db import DataError
from django.core.management.base import CommandError
from django.core.mail import EmailMessage

# Helper function 
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


def send_email_notification(mail_subject, message, to_email):
    try:
        from_email  = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email , to=[to_email])
        mail.send()
    except Exception as e:
        raise e