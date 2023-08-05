import enum

default_app_config = 'django_adminstats.apps.Config'


class Step(enum.Enum):
    DAY = 'd'
    MONTH = 'm'
    YEAR = 'y'
