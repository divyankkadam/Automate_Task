from django.core.management.base import BaseCommand

from dataentry.models import Student

class Command(BaseCommand):

    help = "It Will  insert the data to the databse"

    def handle(self , *args  , **kwargs):
        # logic
        dataset = [
            {'roll_no':1 , 'name':'Person1' , 'age':20 },
            {'roll_no':5 , 'name':'Person5' , 'age':25 },
            {'roll_no':3 , 'name':'Person3' , 'age':22 },
            {'roll_no':6 , 'name':'Person6' , 'age':26 },
        ]

        for data in dataset:
            roll_no = data['roll_no']
            existing_recocrd = Student.objects.filter(roll_no=roll_no).exists()
            if not existing_recocrd:
                Student.objects.create(roll_no = data['roll_no'] , name = data['name'] , age= data['age'])
            else :
                self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists'))

        self.stdout.write(self.style.SUCCESS('Data inserted Successfuly'))
