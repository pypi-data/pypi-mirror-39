import datetime
import re

from .exceptions import ValidationError


class Field:

    def __init__(self, regex=None, index=None, required=False, *args, **kwargs):
        self.regex = regex

        self.required = required
        if 'blank' in kwargs:
            self.required = not kwargs['blank']
        self.index = index

    def to_python(self, value):
        if self.required and not value:
            raise ValidationError('Field may not be blank')

        if self.regex and not re.match(self.regex, value):
            raise ValidationError('Doesn\'t match "{}"'.format(
                self.regex
            ))

        return value


class DateField(Field):

    def __init__(self, date_formats=[], *args, **kwargs):
        self.date_formats = date_formats or ['%m/%d/%y', '%m/%d/%Y']
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        for fmt in self.date_formats:
            try:
                return datetime.datetime.strptime(value, fmt).date()
            except (ValueError, TypeError):
                continue
        if value:
            raise ValidationError('Invalid date format')


class IntegerField(Field):

    def to_python(self, value):
        value = super().to_python(value)
        try:
            return int(value)
        except (ValueError, TypeError):
            if value:
                raise ValidationError('Must be an int')


class FloatField(Field):

    def to_python(self, value):
        value = super().to_python(value)
        try:
            return float(value)
        except (ValueError, TypeError):
            if value:
                raise ValidationError('Must be a float')
