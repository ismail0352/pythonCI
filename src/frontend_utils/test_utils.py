"""
Utilities for running tests
"""

# https://github.com/django-nose/django-nose

import django_nose

# We use this test runner class to avoid errors due to missing database config
# http://www.librador.com/2011/05/23/How-to-run-Django-tests-without-a-database/

class DatabaselessTestRunner(django_nose.NoseTestSuiteRunner):
    """A test suite runner, based on the django-nose suite runner,
    that does not set up and tear down a database.

    To use this runner, put this line in settings.py:
    TEST_RUNNER = 'frontend_utils.test_utils.DatabaselessTestRunner'
    """

    def setup_databases(self):
        """Overrides NoseTestSuiteRunner"""
        pass

    def teardown_databases(self, *args, **kwargs):
        """Overrides NoseTestSuiteRunner"""
        pass


# To run all tests:
# ./manage.py test

# Show standard output from tests:
# ./manage.py test -s

# Run just a single test method on a test class:
# ./manage.py test tests/test_timezone_handling.py:TestTimezoneHandling.test_good_browsers

# To see all of the test options:
# ./manage.py help test
