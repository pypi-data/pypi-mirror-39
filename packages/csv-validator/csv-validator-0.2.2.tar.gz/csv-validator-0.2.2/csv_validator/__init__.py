import csv
import collections

from .fields import Field
from .exceptions import ValidationError


class ValidationMetaclass(type):

    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(cls, name, bases, dct):
        subclass = type.__new__(cls, name, bases, dct)

        subclass._fieldnames = []
        subclass._fields = {}
        for key, value in dct.items():
            if isinstance(value, Field):
                subclass._fields[key] = value
                if value.index is None:
                    subclass._fieldnames.append(key)
                else:
                    if not isinstance(value.index, int):
                        continue
                    elif value.index < len(subclass._fieldnames):

                        raise AttributeError('Field "{}" has an index that conflicts with "{}"'.format(
                            key, subclass._fieldnames[value.index]
                        ))

                    extra_count = value.index - len(subclass._fieldnames) + 1
                    for i in range(extra_count):
                        index = len(subclass._fieldnames)
                        fieldname = 'not_captured_{}'.format(index)
                        subclass._fields[fieldname] = None
                        subclass._fieldnames.append(fieldname)

                    subclass._fieldnames[value.index] = key
        return subclass


class DictReader(csv.DictReader, metaclass=ValidationMetaclass):

    def __init__(self, *args, error_limit=100, **kwargs):
        super().__init__(*args, **kwargs)

        self.errors = {}
        self.error_count = 0
        self.error_limit = error_limit

    @property
    def fieldnames(self):
        return self.__class__._fieldnames

    def __next__(self):
        row = next(self.reader)

        # Skip the first row if it's headers...
        if self.line_num == 0:
            if self.fieldnames == []:
                for index, fieldname in enumerate(row):

                    mapped = False
                    for key, value in self._fields.items():
                        if value and value.index == fieldname:
                            self.__class__._fieldnames.append(key)
                            mapped = True
                    
                    if not mapped:
                        fieldname = 'not_captured_{}'.format(index)
                        self.__class__._fields[fieldname] = None
                        self.__class__._fieldnames.append(fieldname)

                missing = set(self._fields.keys()) - set(self.fieldnames)
                if missing:
                    raise ValidationError('Fields missing in header: {}'.format(', '.join(missing)))

                row = next(self.reader)
            else:
                for i, fieldname in enumerate(self.fieldnames):

                    if fieldname.startswith('not_captured'):
                        continue

                    original_fieldname = self.__class__._fields[fieldname].index

                    if len(row) > i and row[i] != original_fieldname:
                        break
                else:
                    row = next(self.reader)

                if self.fieldnames == row:
                    row = next(self.reader)

        # unlike the basic reader, we prefer not to return blanks,
        # because we will typically wind up with a dict full of None
        # values
        while row == []:
            row = next(self.reader)
        d = dict(zip(self.fieldnames, row))

        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval

        error_dict = {}
        for name, field in self._fields.items():
            if name.startswith('not_captured_'):
                if name in d:
                    del d[name]
                continue
            try:
                d[name] = field.to_python(d[name])
            except ValidationError as e:

                if field.required:
                    error_dict[name] = str(e)
                else:
                    d[name] = None

                if self.error_count >= self.error_limit:
                    continue

        if error_dict:
            raise ValidationError(error_dict)

        self.line_num = self.reader.line_num

        return d

    def iter_lines(self, skip_errors=False):
        '''A generator yielding a two-tuple of (line_number, row), where
        row is a dictionary in the same form as the default iterator'''
        self.errors = {}

        line_number = 0
        while True:
            
            try:
                row = next(self)
            except ValidationError as e:
                if skip_errors:
                    self.errors[line_number] = e.error_dict
                else:
                    raise
            except StopIteration:
                break
            else:
                yield line_number, row
            finally:
                line_number += 1
