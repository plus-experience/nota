from django.forms import model_to_dict
from college.models import *


from django.core.serializers.python import Serializer


class BaseSerializer(Serializer):
    def get_dump_object(self, obj):
        data = self._current
        if not self.use_natural_primary_keys or not hasattr(obj, 'natural_key'):
            data["id"] = self._value_from_field(obj, obj._meta.pk)
        return data


class StudentDjangoBaseSerializer(BaseSerializer):

    def end_object(self, obj):
        self._current['major'] = obj.major.name
        return super(StudentDjangoBaseSerializer, self).end_object(obj)


class LectureDjangoBaseSerializer(BaseSerializer):

    def end_object(self, obj):
        relatedSerializer = StudentDjangoBaseSerializer()
        self._current['attendees'] = relatedSerializer.serialize(obj.attendees.all())
        self._current['lecturer'] = obj.lecturer.name
        return super(LectureDjangoBaseSerializer, self).end_object(obj)


from rest_framework import serializers


class StudentDRFSerializer(serializers.ModelSerializer):
    major = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'major']

    def get_major(self, obj):
        return obj.major.name


class LectureDRFSerializer(serializers.ModelSerializer):
    attendees = StudentDRFSerializer(many=True)
    lecturer = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ['id', 'name', 'attendees', 'lecturer']

    def get_lecturer(self, obj):
        return obj.lecturer.name


import serpy


class StudentSerpySerializer(serpy.Serializer):
    id = serpy.IntField()
    name = serpy.StrField()
    major = serpy.MethodField()

    def get_major(self, obj):
        return obj.major.name


class LectureSerpySerializer(serpy.Serializer):
    id = serpy.IntField()
    name = serpy.StrField()
    lecturer = serpy.MethodField()
    attendees = StudentSerpySerializer(many=True, attr='attendees.all', call=True)

    def get_lecturer(self, obj):
        return obj.lecturer.name


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
