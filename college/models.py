from django.db import models


class Professor(models.Model):
	name = models.CharField(max_length=100)


class Lecture(models.Model):
	name = models.CharField(max_length=100)
	lecturer = models.ForeignKey('college.Professor', related_name='lectures')
	attendees = models.ManyToMany('college.Student', related_name='lectures')


class Student(models.Model):
	name = models.CharField(max_length=100)
