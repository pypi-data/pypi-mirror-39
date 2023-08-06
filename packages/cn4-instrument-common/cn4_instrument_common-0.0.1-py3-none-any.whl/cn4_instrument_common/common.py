class InstrumentInterfaceBase(object):
    """Base class for implementing instrument drivers."""
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

    def get_entities():
        """Returns a list of all entities."""
        raise NotImplementedError()        
        pass

    def get_entity_description():
        """Returns a list of all entities."""
        raise NotImplementedError()                
        pass

    def is_connected():
        """Return the connected state of the driver. A driver does not need to 
        implement this. """
        raise NotImplementedError()                        
        pass

    def supports_connected():
        """True indicates that connect needs to be called before driver interaction."""
        raise NotImplementedError()                        
        pass

    def connect():
        """Connects a driver to it's instrument."""
        raise NotImplementedError()                        
        pass

    def disconnect():
        """Disconnects a driver from it's instrument."""
        raise NotImplementedError()                        
        pass

class EntityDescription(object):
    """An EntityDescription gives all necessary information to an instrument driver 
    entity. It can be part of a user documentation."""

    """Id of an entity."""
    entity_id=None
    """Type of an entity."""
    entity_type=None
    """Entity can be read."""
    readable=False
    """Entity can be written."""
    writeable=False
    """Entity is internal and not for external use."""
    internal=False