TypesValidator
==============

ejemplo:
```python

from typesvalidator.typesvalidator import TypesValidator

class Persona(object):
    pass

@TypesValidator.validator(True)
def ala(nom: str)->Persona:
    print ("sd")
    a = Persona()
    return a


ala("cocho")

```