from django.core.management.base import BaseCommand , CommandError
# from dataentry.models import Student
from django.apps import apps # import all apps
from dataentry.utils import check_csv_errors 

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

        model = check_csv_errors(file_path,model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data imported from csv successfuly Successfully!"))
            