import sys
import logging
import argparse
import traceback

from django.core.management.base import BaseCommand
from ....i2run import CCP4i2RunnerDjango

# Get an instance of a logger
logger = logging.getLogger("root")
logger.setLevel(logging.WARNING)


class Command(BaseCommand):

    help = "Configure and run a job in the database"
    requires_system_checks = []

    def add_arguments(self, parser):
        # Don't add any arguments - we'll handle them manually in handle()
        pass

    def handle(self, *args, **options):
        """
        Use sys.argv directly to bypass Django's argument parsing.
        CCP4i2RunnerDjango will handle all argument parsing.
        """
        # sys.argv structure: ['manage.py', 'i2run', 'task_name', ...args...]
        # We want everything after 'i2run'
        the_args = sys.argv[2:]
        logger.info(f"i2run args: {the_args}")

        try:
            parser = argparse.ArgumentParser()

            # Modern approach: No Qt parent needed
            self.i2_runner = CCP4i2RunnerDjango.CCP4i2RunnerDjango(
                the_args=the_args,
                parser=parser,
                parent=None,  # No Qt spoof needed - using modern async approach
            )

            self.i2_runner.parseArgs()

            # Execute directly
            result = self.i2_runner.execute()
            logger.info(f"i2run execute() returned: {result}")

        except Exception as e:
            logger.error(f"i2run failed with exception: {e}")
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            print(f"\nERROR: i2run failed")
            print(f"Exception: {e}")
            print(f"\nTraceback:")
            print(traceback.format_exc())
            raise
