from django.db import models


class Professor(models.Model):
	name = models.CharField(max_length=100)


class Major(models.Model):
	name = models.CharField(max_length=100)


class Lecture(models.Model):
	name = models.CharField(max_length=100)
	lecturer = models.ForeignKey('college.Professor', related_name='lectures', on_delete=models.CASCADE)
	attendees = models.ManyToManyField('college.Student', related_name='lectures')


class Student(models.Model):
	name = models.CharField(max_length=100)
	major = models.ForeignKey('college.Major', on_delete=models.SET_NULL, null=True)
