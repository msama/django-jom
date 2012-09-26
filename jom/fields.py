'''
Created on Jul 19, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import datetime
from types import NoneType

from django.template.defaultfilters import safe
from django.template.loader import render_to_string

from jom import factory as jom_factory
from django.contrib.sites.models import Site


class JomField(object):
    """ Define the base class for a field.
    """
    
    def __init__(self, instance, name, readonly = False,
                 factory = jom_factory.JomFactory.default()):
        self.name = name
        self.instance = instance
        self.readonly = readonly
        self.factory = factory

    def getValue(self):
        return getattr(self.instance, self.name)

    def toString(self):
        raise AssertionError(
                "JomField is abstract")
    
    def toJavascript(self):
        raise AssertionError(
                "JomField is abstract")
        
    @classmethod
    def renderField(self, clazz, name, readonly = False):
        dictionary = {
                'clazz': clazz,
                'name': name,
                'readonly': readonly
                }
        
        return render_to_string(
                'jom/JomField.js', dictionary = dictionary)


class BooleanJomField(JomField):
    """ Define a field wrapping a boolean.
    """
    
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, bool):
            raise AssertionError(
                "Value should be a boolean. Found: %s." % value)
        super(BooleanJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.getValue()
    
    def toJavascript(self):
        return "true" if self.getValue() else "false"
  
        
class NumeralJomField(JomField):
    """ Define a field wrapping a numeral.
    """
    
    def __init__(self, instance, name, readonly = False,
                 factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, (int, long, float, NoneType)):
            raise AssertionError(
                "Value should be a number. Found: %s." % value)
        super(NumeralJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.getValue()
    
    def toJavascript(self):
        # marked safe to avoid comma separators
        return safe(self.getValue())
    
    @classmethod
    def renderField(self, clazz, name, readonly = False):
        dictionary = {
                'clazz': clazz,
                'name': name,
                'readonly': readonly
                }
        
        return render_to_string(
                'jom/NumeralJomField.js', dictionary = dictionary)


class StringJomField(JomField):
    """ Define a field wrapping a string.
    """
    
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, (str, unicode, NoneType)):
            value = getattr(instance, name)
            raise AssertionError(
                "Value should be a string. Found: %s." % value)
        super(StringJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return safe(self.getValue())
    
    def toJavascript(self):
        # TODO(msama): handle tabs and new lines
        value = self.getValue() if self.getValue() else ""
        return safe("\"%s\"" % value.replace("\"", "\\\""))
    

class JavascriptJomField(JomField):
    """ Define a field wrapping a string.
    """
    
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, (str, unicode, NoneType)):
            raise AssertionError(
                "Value should be a string. Found: %s." % value)
        super(JavascriptJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.getValue()
    
    def toJavascript(self):
        if self.getValue():
            return safe(self.getValue())
        else:
            return safe("null")
    

class UrlJomField(JomField):
    """ Define a field wrapping a file.
    """
    def __init__(self, instance, name, readonly = False,
                 factory = jom_factory.JomFactory.default()):
        # TODO(msama): type checking
        super(UrlJomField, self).__init__(instance, name, readonly, factory)
        
    def getValue(self):
        try:
            filefield = getattr(self.instance, self.name)
            if filefield.name != None:
                return "http://%s%s" % (Site.objects.get_current(), filefield.url)
            else:
                return ""
        except ValueError:
            return ""
                
    def toString(self):
        return self.getValue()
    
    def toJavascript(self):
        return safe("\"%s\"" % self.getValue())


class DateJomField(JomField):
    """ Define a field wrapping a boolean.
    """
    
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, (datetime.date.Date, 
                datetime.time.Time, datetime.datetime.DateTime)):
            raise AssertionError(
                "Value should be a datetime. Found: %s." % value)
        super(DateJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.getValue()
    
    def toJavascript(self):
        return self.getValue()
    

class ForeignKeyJomField(JomField):
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        
        for f in instance._meta.fields:
            if f.name == name: 
                self.related = f.rel.to
        if self.related == None:
            raise AssertionError(
                "name should be a related field")
        super(ForeignKeyJomField, self).__init__(instance, name, readonly, factory)
    
    def getValue(self):
        try:
            return getattr(self.instance, self.name)
        except self.related.DoesNotExist:
            return None
    
    def toString(self):
        value = self.getValue()
        return value.id if value else "null"
    
    def toJavascript(self):
        value = self.getValue()
        return value.id if value else "null"

    @classmethod
    def renderField(self, clazz, name, fk_clazz, readonly = False):
        dictionary = {
                'clazz': clazz,
                'name': name,
                'fk_clazz': fk_clazz,
                'readonly': readonly
                }
        
        return render_to_string(
                'jom/ForeignKeyJomField.js', dictionary = dictionary)