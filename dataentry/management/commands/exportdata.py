import datetime
from django.core.management.base import BaseCommand
import csv
from django.apps import apps

# propsed command = python manage.py exportdata model_name
class Command(BaseCommand):
    help = "Export data from Student model to CSV file "

    def add_arguments(self , parser):
        parser.add_argument('model_name' ,type=str , help='Model name')
    
    def handle(self , *args , **kwargs ):
        model_name = kwargs['model_name'].capitalize()
        
        # Search through all installed apps for the model
        model = None 
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label , model_name)
                break                                                       # Stop executing if model is  found 
            except LookupError:
                pass
        
        if not model :
            self.stderr.write(f'Model {model} cound not found')
            return 
        
        #fetch the data from database
        data = model.objects.all()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_path = f"exported_{model_name}_data_{timestamp}.csv"
        

        # open csv file and write data 
        with open(file_path , 'w', newline='') as file:
            writer = csv.writer(file)

            # we want field names of model that are trying to export  
            writer.writerow([field.name for field in model._meta.fields])   # Write the CSV Header 

            for dt in data :
                writer.writerow([getattr(dt , field.name )for field in model._meta.fields])


        self.stdout.write(self.style.SUCCESS("Data Exported Successfully"))





    


