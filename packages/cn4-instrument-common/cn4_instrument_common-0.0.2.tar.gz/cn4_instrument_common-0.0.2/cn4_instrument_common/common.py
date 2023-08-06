'''
____________________________________________________________________________
    File:         common.py
    File Created: Friday, 14th December 2018 8:46:15 am
    Author:       David Kremzow
    Copyright (C) 2018 - 2018 David Kremzow
____________________________________________________________________________
'''
from .event import EventHook

class InstrumentInterfaceBase(object):
    """Base class for implementing instrument drivers."""

    def __init__(self):
        self.on_value_changed=EventHook()
        self.on_notify=EventHook()


    def get_manufacturer(self):
        """Returns the manufacturer of the instrument."""
        raise NotImplementedError()
        pass

    def get_type(self):
        """Returns all supported instrument types supported."""
        raise NotImplementedError()        
        pass

    def get_values(self, *valueIds):
        """Returns a list of values for the requested valueIds."""
        raise NotImplementedError()        
        pass

    def set_values(self, **idValuePairs):
        """Returns a list of values for the requested valueIds."""
        raise NotImplementedError()        
        pass

    def get_entities(self):
        """Returns a list of all entities."""
        raise NotImplementedError()        
        pass

    def get_entity_description(self):
        """Returns a list of all entities."""
        raise NotImplementedError()
        pass

    def is_connected(self):
        """Return the connected state of the driver. A driver does not need to 
        implement this. """
        raise NotImplementedError()
        pass

    def supports_connected(self):
        """True indicates that connect needs to be called before driver interaction."""
        raise NotImplementedError()                        
        pass

    def connect(self):
        """Connects a driver to it's instrument."""
        raise NotImplementedError()                        
        pass

    def disconnect(self):
        """Disconnects a driver from it's instrument."""
        raise NotImplementedError()                        
        pass

class EntityDescription(object):
    """An EntityDescription gives all necessary information to an instrument driver 
    entity. It can be part of a user documentation."""

    def __init__(self, id, type, *args, **kwargs):
        #Id of an entity.
        if not id:
            raise AttributeError('Id must not be None or empty string.')
        self.entity_id = id
        #Type of an entity.
        if not type:
            raise AttributeError('Type must not be None.')
        self.entity_type = type
        #Entity can be read.
        self.readable=kwargs.get('readable', True)
        #Entity can be written.
        self.writable=kwargs.get('writable', False)
        #Entity is internal and not for external use.
        self.internal=kwargs.get('internal', False)


class Entity(object):
    """An Entity value and description of an entity. It shall only be used inside an
    instrument."""

    def __init__(self, desc):
        if not isinstance(desc, EntityDescription):
            raise AttributeError('Paramaeter <desc> must be of type EntityDescription')
        self.entity_desc = desc

    """Description of an entity."""
    entity_desc=None
    """Value of an entity."""
    entity_value=None    

class EntityDictionary(dict):
    """Dictionary with event support. It's intention is to be used in instruments for
    keeping the values."""  
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        self.on_value_changed=EventHook()
        self.on_value_added=EventHook()
        self.on_value_deleted=EventHook()

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        value_added = key not in self
        old_value = self.get(key)
        dict.__setitem__(self, key, val)
        if value_added: self.on_value_added.fire(key=key, new_value=val)
        if not old_value==val: self.on_value_changed.fire(key=key, new_value=val, old_value=old_value)

    def __delitem__(self, key):
        ret_val =  dict.__delitem__(self, key)
        self.on_value_deleted.fire(key=key)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def set_entity(self, entity):
        self[entity.entity_desc.id]=entity

    def create_entity(self, entity_desc):
        self[entity_desc.id]=Entity(entity_desc)
