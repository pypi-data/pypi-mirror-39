# Django User Settings

## Installation
Install using `pip`:

```bash
pip install django-user-settings
```

## Requirements

**django-user-settings** requires these:
- django
- psycopg2

## Example

Put `user_settings` to `INSTALLED_APPS` in `settings.py` like this:

```python
INSTALLED_APPS= (
    ...
    'user_settings',
)
```

**Optional:

If you don't use your User model, django-user-settings will use default django User model.

```python
from django.contrib.auth.models import User
```

Otherwise, you will need to add your User model to `AUTH_USER_MODEL` in `settings.py`:

```python
AUTH_USER_MODEL = 'myapp.MyUser'
```

Now, you are ready to use **django-user-settings**, start with importing:

```python
from user_settings.utils import get_user_setting, set_user_setting
```

```python
get_user_setting(key, default_value=None, **kwargs)
```
Return user's setting in Python's dictionary

**Arguments**

`key`: setting's name

`default_value`: if **django-user-settings** cannot find suitable settings, this will be set to value of this key

`**kwargs`:
```
    'request': django's request

    'uid': PK of user you want to get setting
```
If you pass both `request` and `uid`, **django-user-settings** will get settings of user with pk=`uid`.

If you pass only `request`, **django-user-settings** will get settings of current authenticated user.

If you pass `uid` = None, **django-user-settings** will get settings with no specific user.

```python
set_user_setting(key, value, **kwargs)
```

**Arguments**

`key`: setting's name

`value`: setting's value

`**kwargs`:
    'request': django's request, we will use this to get current authenticated user.
    'uid': ID of user whose settings will be saved.


If you pass both `request` and `uid`, **django-user-settings** will save settings for user with pk=`uid`.

If you pass only `request`, **django-user-settings** will save settings for current authenticated user.

If you pass `uid` = None, **django-user-settings** will save settings with no specific user.
