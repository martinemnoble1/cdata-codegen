import sys
import logging

from django.core.management.base import BaseCommand
from ....i2run import CCP4i2RunnerDjango
from core.CCP4TaskManager import TASKMANAGER

# Get an instance of a logger
logger = logging.getLogger("root")
logger.setLevel(logging.WARNING)


class Command(BaseCommand):

    help = "Configure and run a job in the database"
    requires_system_checks = []

    def add_arguments(self, parser):
        logger.info("sys.argv is [%s]", sys.argv)
        self.i2_runner = CCP4i2RunnerDjango.CCP4i2RunnerDjango(
            the_args=sys.argv[2:],
            parser=parser,
            parent=CCP4Modules.QTAPPLICATION(graphical=False),
        )
        self.i2_runner.parseArgs()

    def handle(self, *args, **options):
        def execute():
            self.i2_runner.execute()

        execute()
        return
