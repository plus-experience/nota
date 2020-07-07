from django.test import TestCase
from college.models import *
from college.serializers import not_a_serializer, ProfessorSerializer


class ThroughputTest(TestCase):

	@classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        # Create Students, Lectures, Professors
        pass

    def test_drf(self):
    	pass

    def test_nota(self):
    	pass

    def test_serpy(self):
    	pass
