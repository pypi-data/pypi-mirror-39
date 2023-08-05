# Carehome
A stupidly named package for creating MOO-style objects with Python.

Objects support multiple inheritance, properties, events, and methods. The resulting database can be dumped and loaded to and from dictionary objects.

## Events
The following events are used throughout the code. Any other events which are baked into the main code base should be added here.

### on_init
Called when the object is initialised.

#### Arguments
None

### on_destroy
Called before the object is destroyed, and the object is still valid.

#### Arguments
None

### on_enter
Called before an object enters another one.

#### Arguments

* The thing which is moving into this object.

### on_exit
Called before an object exits another.

#### Arguments

* The object which is leaving.
