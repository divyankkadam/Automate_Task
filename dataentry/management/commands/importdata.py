from django.core.management.base import BaseCommand , CommandError
# from dataentry.models import Student
from django.apps import apps # import all apps

import csv

from django.db import DataError

# proposed command - python manage.py importdata file_path model_name
class Command(BaseCommand):

    help = "Import dat from csv file "

    def add_arguments(self, parser):
        parser.add_argument('file_path' , type=str , help='Path to the CSV file')
        parser.add_argument('model_name' , type=str , help='Name of model')

    def handle(self, *args, **Kwargs):
        file_path = Kwargs['file_path']
        model_name = Kwargs['model_name'].capitalize()

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
        

        with open(file_path , 'r') as file:
            reader = csv.DictReader(file)                                    # DictReader - reading a CSV file and mapping the information in each row to a dictionary and return a iterator
            csv_header = reader.fieldnames
            
            # compare csv header with model field name 
            if csv_header != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields")
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data imported from csv successfuly Successfully!"))
            