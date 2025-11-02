import sys
import logging

from django.core.management.base import BaseCommand
from ....i2run import CCP4i2RunnerDjango

# Get an instance of a logger
logger = logging.getLogger("root")
logger.setLevel(logging.WARNING)


class Command(BaseCommand):

    help = "Configure and run a job in the database"
    requires_system_checks = []

    def add_arguments(self, parser):
        logger.info("sys.argv is [%s]", sys.argv)
        # Modern approach: No Qt parent needed
        self.i2_runner = CCP4i2RunnerDjango.CCP4i2RunnerDjango(
            the_args=sys.argv[2:],
            parser=parser,
            parent=None,  # No Qt spoof needed - using modern async approach
        )
        self.i2_runner.parseArgs()

    def handle(self, *args, **options):
        # Direct execution - no Qt event loop wrapper needed
        self.i2_runner.execute()
        return
