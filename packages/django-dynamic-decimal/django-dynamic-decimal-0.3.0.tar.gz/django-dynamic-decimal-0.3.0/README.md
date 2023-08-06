django-dynamic-decimal
==========================

Plug django-dynamic-decimal into your Django project to save dynamic decimals to database.

## Installing

```bash
$ pip install django-dynamic-decimal
```

## Usage

```
from dynamic_decimal.db.fields import DynamicDecimalField

class Obj(models.Model):
  decimal = DynamicDecimalField(
    # Default value
    # max_length=255,
  )
  
```
