# encoding: utf-8
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User, UserManager
import datetime

####################################################################################################
#######################################   Catalogs  ################################################  
####################################################################################################
class Area(TimeStampedModel):
  AREAS = (
    (u'a', u'Dirección'),
    (u'b', u'Secretaría Académica'),
    (u'c', u'Técnica y Administrativa'),
    (u'd', u'MMSS'),
    (u'e', u'UPD y Soporte Técnico'),
    (u'f', u'ISCA'),
    (u'g', u'Métodos Matemáticos y Numéricos'),
    (u'h', u'Electrónica y Automatización'),
    (u'i', u'Ciencias de la Computación'),
    (u'j', u'Laboratorio MPyE'),
    (u'k', u'Soporte Técnico'),
    (u'l', u'MPyE y Aulas'),
    (u'm', u'Biblioteca'),
    (u'n', u'Posgrado en MCIC'),
  )
  """Areas inside the institute."""
  name        = models.CharField(max_length=80)
  description = models.CharField(max_length=100)
  enabled     = models.BooleanField(default=True)

  def __unicode__(self):
    return u"%s, %s" % (self.name , self.description)

####################################################################################################
class Room(TimeStampedModel):
  """It Could be an office, a lab, etc."""
  name        = models.CharField(max_length=80)
  description = models.CharField(max_length=100)
  enabled     = models.BooleanField(default=True)

  def __unicode__(self):
    return u"%s, %s" % (self.name , self.description)


####################################################################################################
class Location(TimeStampedModel):
  INSTITUTES = (
    (u'IIMAS', u'Instituto de Matematicas Aplicadas y Sistemas'),
  )

  BUILDINGS = (
    (u'EA', u'Edificio Anexo'),
    (u'EP', u'Edificio Principal'),
  )

  FLOORS = (
    (u'PB', u'Planta Baja'),
    (u'PP', u'Primer Piso'),
    (u'SP', u'Segundo Piso'),
    (u'TP', u'Tercero Piso'),
    (u'CP', u'Cuarto Piso'),
    (u'S', u'Sotano'),
  )

  LOCATION_TYPES = (
    (u'C', u'Cubiculo'),
    (u'D', u'Laboratorio'),
    (u'A', u'Area abierta'),
    (u'P', u'Pasillo'),
  )

  """It represents and specific place inside the Institute."""
  name        = models.CharField(max_length=80)
  description = models.CharField(max_length=100)
  institute   = models.CharField(blank=True, null=True, max_length=20, choices=INSTITUTES)
  building    = models.CharField(blank=True, null=True, max_length=20, choices=BUILDINGS)
  floor       = models.CharField(blank=True, null=True, max_length=20, choices=FLOORS)
  location_type  = models.CharField(blank=True, null=True, max_length=20, choices=LOCATION_TYPES)
  enabled     = models.BooleanField(default=True)
  # Relationships
  area         = models.ForeignKey(Area)
  room         = models.ForeignKey(Room)
  
  class Meta:
    verbose_name_plural = "Locations"
  
  def __unicode__(self):
    return u"%s, %s" % (self.name , self.description)


####################################################################################################
class MapKey(TimeStampedModel):
  """Codes used to represent some state in the map"""
  key         = models.CharField(max_length=10)
  name        = models.CharField(max_length=80)
  description = models.CharField(max_length=100)
  enabled     = models.BooleanField(default=True)
  color       = models.CharField(max_length=10)
  meaning     = models.CharField(max_length=50)

  def __unicode__(self):
    return u"%s, %s" % (self.name , self.description)


####################################################################################################
class Message(TimeStampedModel):
  """Messages used when the alarm is activated"""
  name        = models.CharField(max_length=80)
  description = models.CharField(max_length=100)
  enabled     = models.BooleanField(default=True)
  text        = models.CharField(max_length=100)
  
  def __unicode__(self):
    return u"%s, %s" % (self.name , self.description)



####################################################################################################
#######################################   Domain  ##################################################  
####################################################################################################
class Switch(TimeStampedModel):
  """Switchs"""
  name        = models.CharField(max_length=80)
  description = models.CharField(max_length=100)
  enabled     = models.BooleanField(default=True)
  identifier  = models.PositiveIntegerField(null=False)
  ip_address  = models.CharField(max_length=80)
  ports_number = models.PositiveIntegerField(null=False)
  # Relationships
  location     = models.ForeignKey(Location)
  
  def __unicode__(self):
    return u"%s, %s" % (self.name , self.description)
    
####################################################################################################
class Computer(TimeStampedModel):
  """Computers in the institute"""
  name          = models.CharField(max_length=80)
  description   = models.CharField(max_length=100)
  brand         = models.CharField(max_length=80)
  hd_size     = models.CharField(max_length=80)
  memory_size = models.CharField(max_length=80)
  serial_number = models.CharField(max_length=80)
  ip_address    = models.CharField(max_length=80)
  port          = models.PositiveIntegerField(null=False)
  # Relationships
  switch        = models.ForeignKey(Area)
  location     = models.ForeignKey(Location)
  
  def __unicode__(self):
    return u"%s, %s" % (self.name , self.description)


####################################################################################################
class Employee(User):
  """
  We use the django authorization model to represent our employess.
  We only define the extra fields required for our alarm system.
  """
  telephone      = models.CharField(blank=True, null=True, max_length=15)
  birth_date     = models.DateField(blank=True, null=True)
  contract_date  = models.DateField(default=datetime.datetime.now)
  comments       = models.TextField(blank=True, null=True)

  def __unicode__(self):
    return u"%s, %s" % (self.first_name , self.last_name)


