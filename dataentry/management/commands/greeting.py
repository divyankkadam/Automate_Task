from django.core.management.base import BaseCommand

# Custom management commands in Django allow developers to create their own terminal commands to automate backend tasks and interact with Django projects using ORM and settings.

class Command(BaseCommand):
    help = "Gretting Command"   # command level help text

    def add_arguments(self, parser): 
        parser.add_argument('name' , type=str , help='Sepecificy user name')  # argument level help text 


    def handle(self , *args , **kargs):
        name = kargs['name']
        greeting = f'Hi {name}  ! Good evening'
        self.stdout.write(self.style.SUCCESS(greeting) )    # SUCCESS WARING ERROR
        # self.stderr.write(greeting)


    