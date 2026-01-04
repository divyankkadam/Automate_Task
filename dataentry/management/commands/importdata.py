from django.core.management.base import BaseCommand , CommandError
# from dataentry.models import Student
from django.apps import apps # import all apps

import csv

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
            raise CommandError(f"Model {model_name} not found in any app")   # to provide a clean, readable failure message to the user in the termina

        with open(file_path , 'r') as file:
            reader = csv.DictReader(file)                                    # DictReader - reading a CSV file and mapping the information in each row to a dictionary
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data imported from csv successfuly Successfully!"))
            