from django.core.management.base import BaseCommand
# BaseCommand - parent class used to create custom management commands .  It handles the interface between the command line and your Python logic. 

class Command(BaseCommand):
    help = "Prints Hello World"

    def handle(self , *args , **kwargs ):
        self.stdout.write('Hello world')
    


