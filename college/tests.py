import time

from django.db.models import Prefetch
from django.test import TestCase, override_settings
from college.models import *
from college.serializers import not_a_serializer, LectureDRFSerializer, LectureSerpySerializer, LectureDjangoBaseSerializer


class ThroughputTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(30):
            majors = []
            for j in range(10):
                majors.append(Major(name='ComputerEngineering'))
                majors.append(Major(name='Korean'))
            Major.objects.bulk_create(majors)
        majors = Major.objects.all()

        for i in range(30):
            students = []
            for j in range(100):
                students.append(Student(name='Ugaemi', major=majors[0]))
                students.append(Student(name='Giuk', major=majors[0]))
            Student.objects.bulk_create(students)
        students = Student.objects.all()

        for i in range(30):
            professors = []
            for j in range(30):
                professors.append(Professor(name='Devsusu'))
            Professor.objects.bulk_create(professors)
        professors = Professor.objects.all()

        for i in range(30):
            lectures = []
            for j in range(10):
                lectures.append(Lecture(name='Python', lecturer=professors[0]))
            Lecture.objects.bulk_create(lectures)
        lectures = Lecture.objects.all()

        for lecture in lectures:
            attendees = students[:40]
            lecture.attendees.add(*attendees)

        cls.lectures = lectures

    def setUp(self):
        self.start = time.time()

    def tearDown(self) -> None:
        t = time.time() - self.start
        print(f'{self.msg}: {int(round(t * 1000))}')

    @override_settings(DEBUG=True)
    def test_dbs(self):
        self.msg = 'Django Serializer Run-Time'
        lectures = self.lectures.prefetch_related(
            Prefetch(
                'attendees',
                queryset=Student.objects.filter(
                    major__name='ComputerEngineering',
                ),
            ),
            'attendees__major',
            'lecturer',
        )
        serializer = LectureDjangoBaseSerializer()
        results = serializer.serialize(lectures)

    @override_settings(DEBUG=True)
    def test_drf(self):
        self.msg = 'DRF Serializer Run-Time'
        lectures = self.lectures.prefetch_related(
            Prefetch(
                'attendees',
                queryset=Student.objects.filter(
                    major__name='ComputerEngineering',
                ),
            ),
            'attendees__major',
            'lecturer',
        )
        results = LectureDRFSerializer(lectures, many=True).data

    @override_settings(DEBUG=True)
    def test_serpy(self):
        self.msg = 'Serpy Serializer Run-Time'
        lectures = self.lectures.prefetch_related(
            Prefetch(
                'attendees',
                queryset=Student.objects.filter(
                    major__name='ComputerEngineering',
                ),
            ),
            'attendees__major',
            'lecturer',
        )
        results = LectureSerpySerializer(lectures, many=True).data

    @override_settings(DEBUG=True)
    def test_nota(self):
        self.msg = 'Nota Serializer Run-Time'
        lectures = self.lectures.prefetch_related(
            Prefetch(
                'attendees',
                queryset=Student.objects.filter(
                    major__name='ComputerEngineering',
                ),
            ),
            'attendees__major',
            'lecturer',
        )
        lectures_fields = {
            'concrete_fields': ['id', 'name'],
            'complex_fields': {
                'lecturer': lambda x: x.lecturer.name,
            },
            'many_fields': {
                'attendees': {
                    'concrete_fields': ['id', 'name'],
                    'complex_fields': {
                        'major': lambda x: x.major.name,
                    },
                    'many_fields': {},
                },
            },
        }
        results = not_a_serializer(lectures, lectures_fields)
