from django.core.management.base import BaseCommand
from django.conf import settings
from monitor.domain import *

class Command(BaseCommand):
  help = ("Run the monitor demon")
  
  def handle(self, *args, **options):
    print "Running the demon..."
    switchMonitor = SwitchMonitor()
    switchMonitor.start()
    
    
    