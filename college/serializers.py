from django.forms import model_to_dict
from college.models import *


def not_a_serializer(queryset, options):
    """
    options keys required
    :param queryset: QuerySet()
    :param options: {
        'concrete_fields': ['field', ...],
        'complex_fields': lambda function,
        'many_fields': {
            'many_to_one_or_many_fields': {
                'concrete_fields': ['field', ...],
                'complex_fields': lambda function,
                'many_fields': {},
            },
        },
    }
    :return: dict
    """
    results = []
    for obj in queryset:
        row = {}
        row.update(model_to_dict(obj, fields=options['concrete_fields']))
        for k, v in options['complex_fields'].items():
            row[k] = v(obj)
        for k, v in options['many_fields'].items():
            name = v['dict_name'] if 'dict_name' in v else k
            tmpObj = getattr(obj, k)
            if 'related_descriptors' in type(tmpObj).__module__:
                row[name] = not_a_serializer(tmpObj.all(), v)
            else:
                row[name] = not_a_serializer([tmpObj], v)
        results.append(row)
    return results


from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['name']


class LectureSerializer(serializers.ModelSerializer):
    attendees = StudentSerializer(many=True)

    class Meta:
        model = Lecture
        fields = ['name', 'attendees']


class ProfessorSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True)

    class Meta:
        model = Professor
        fields = ['name', 'lectures']
