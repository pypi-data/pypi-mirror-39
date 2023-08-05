from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from decimal import InvalidOperation
from inspect import isclass
from uuid import UUID


class InputBase(object):
    def __init__(
        self,
        template_name,
        not_null_default,
        can_sort=False,
        can_filter=False,
        can_search=False,
        is_readonly=True, # TODO
        is_nullable=False,
        verbose_name=None,
        help_text=None,
        choices=None,
        default=None):

        if (not is_nullable) and (default is None):
            default = not_null_default

        self.name = None
        self.can_sort = can_sort
        self.can_filter = can_filter
        self.can_search = can_search
        self.is_readonly = is_readonly
        self.is_nullable = is_nullable
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.choices = choices
        self.default = default

    def _validate(self, errors, raw_data):
        if (raw_data is None) and (not self.is_nullable):
            errors.append(f'No value specified.')


class BlobInput(InputBase):
    def __init__(self, can_upload=False, can_download=False, **kwargs):
        super().__init__('inputs/blob.html', b'', **kwargs)
        self.can_upload = can_upload
        self.can_download = can_download

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)


class BooleanInput(InputBase):
    def __init__(self, **kwargs):
        super().__init__('inputs/boolean.html', False, **kwargs)

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if raw_data is None:
            return False
        else:
            raw_data = raw_data.lower()

            if raw_data in ('t', 'true', 'on', 'yes', '1'):
                return True
            elif raw_data in ('f', 'false', 'off', 'no', '0'):
                return False
            else:
                errors.append(f'Invalid value.')


class CharInput(InputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('inputs/char.html', '', **kwargs)
        self.max_length = max_length

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            return str(raw_data)


class DateInput(InputBase):
    def __init__(self, min_value=date.min, max_value=date.max, formats=('%Y/%m/%d', '%Y-%m-%d'), **kwargs):
        super().__init__('inputs/date.html', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.formats = formats

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            value = None

            for format in self.formats:
                try:
                    value = datetime.strptime(raw_data, format).date()
                    break
                except ValueError:
                    pass

            if value is None:
                errors.append(f'Invalid value.')
            else:
                if value < self.min_value:
                    errors.append(f'Value ({value}) must be after {self.min_value}.')

                if value > self.max_value:
                    errors.append(f'Value ({value}) must be before {self.max_value}.')

            return value


class DateTimeInput(InputBase):
    def __init__(self, min_value=datetime.min, max_value=datetime.max, formats=('%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S'), **kwargs):
        super().__init__('inputs/datetime.html', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.formats = formats

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            value = None

            for format in self.formats:
                try:
                    value = datetime.strptime(raw_data, format)
                    break
                except ValueError:
                    pass

            if value is None:
                errors.append(f'Invalid value.')
            else:
                if value < self.min_value:
                    errors.append(f'Value ({value}) must be after {self.min_value}.')

                if value > self.max_value:
                    errors.append(f'Value ({value}) must be before {self.max_value}.')

            return value


class DecimalInput(InputBase):
    def __init__(self, min_value=0, max_value=100, decimal_places=2, **kwargs):
        super().__init__('inputs/decimal.html', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.decimal_places = decimal_places

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            value = None

            try:
                value = Decimal(raw_data)

                if value < self.min_value:
                    errors.append(f'Value ({value}) must be greater than {self.min_value}.')

                if value > self.max_value:
                    errors.append(f'Value ({value}) must be less than {self.max_value}.')
            except InvalidOperation:
                errors.append(f'Invalid value.')

            return value


class DropDownInput(InputBase):
    def __init__(self, **kwargs):
        super().__init__('inputs/dropdown.html', None, **kwargs)

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)


class FileInput(InputBase):
    def __init__(self, **kwargs):
        super().__init__('inputs/file.html', None, **kwargs)

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        return raw_data


class ForeignKeyInput(InputBase):
    def __init__(self, model=None, query=None, **kwargs):
        super().__init__('inputs/foreign-key.html', None, **kwargs)

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)


class IntegerInput(InputBase):
    def __init__(self, min_value=0, max_value=100, **kwargs):
        super().__init__('inputs/integer.html', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            value = None

            try:
                value = int(raw_data)

                if value < self.min_value:
                    errors.append(f'Value ({value}) must be greater than {self.min_value}.')

                if value > self.max_value:
                    errors.append(f'Value ({value}) must be less than {self.max_value}.')
            except ValueError:
                errors.append(f'Invalid value.')

            return value


class PasswordInput(InputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('inputs/password.html', '', **kwargs)
        self.max_length = max_length

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            return str(raw_data)


class SlugInput(InputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('inputs/slug.html', '', **kwargs)
        self.max_length = max_length

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            return str(raw_data)

class TextInput(InputBase):
    def __init__(self, **kwargs):
        super().__init__('inputs/text.html', '', **kwargs)

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            return str(raw_data)


class TimeInput(InputBase):
    def __init__(self, min_value=time.min, max_value=time.max, formats=('%H:%M:%S', '%H:%M'), **kwargs):
        super().__init__('inputs/time.html', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.formats = formats

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            value = None

            for format in self.formats:
                try:
                    value = datetime.strptime(raw_data, format).time()
                    break
                except ValueError:
                    pass

            if value is None:
                errors.append(f'Invalid value.')
            else:
                if value < self.min_value:
                    errors.append(f'Value ({value}) must be after {self.min_value}.')

                if value > self.max_value:
                    errors.append(f'Value ({value}) must be before {self.max_value}.')

            return value


class UUIDInput(InputBase):
    def __init__(self, **kwargs):
        super().__init__('inputs/uuid.html', '00000000-0000-0000-0000-000000000000', **kwargs)

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            value = None

            try:
                value = UUID(raw_data)
            except ValueError:
                errors.append(f'Invalid value.')

            return value


class UrlInput(InputBase):
    def __init__(self, **kwargs):
        super().__init__('inputs/url.html', '', **kwargs)

    def _validate(self, errors, raw_data):
        super()._validate(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > 8192:
                errors.append(f'Length must be less than 8192.')

            return str(raw_data)


class FormMeta(object):
    def __init__(self, inputs, *args, **kwargs):
        self.inputs = inputs


class FormBase(object):
    def __new__(cls, *args, **kwargs):
        meta_dict = {}
        input_dict = {}

        for base in reversed(cls.__mro__):
            meta_class = getattr(base, 'Meta', None)

            if meta_class and isclass(meta_class):
                for name in dir(meta_class):
                    if not name.startswith('_'):
                        meta_dict[name] = getattr(meta_class, name)
            
            for name in dir(base):
                if not name.startswith('_'):
                    input = getattr(base, name)
                    input.name = name

                    if isinstance(input, InputBase):
                        input_dict[name] = input

        result = super().__new__(cls)
        result._meta = FormMeta(input_dict, meta_dict)

        return result

    def __init__(self, prefix='', **kwargs):
        self.prefix = prefix
        self._raw_data = {}
        self.data = {}
        self.errors = {}
        self.update(kwargs)

    def update(self, data):
        self._raw_data = {}

        for name, value in data.items():
            if name.startswith(self.prefix):
                self._raw_data[name[len(self.prefix):]] = value

    def validate(self):
        self.errors = {}
        self.data = {}
        is_valid = True

        for input in self._meta.inputs.values():
            errors = []
            self.data[input.name] = input._validate(errors, self._raw_data.get(input.name))
            self.errors[input.name] = errors
            is_valid = is_valid and (not errors)

        return is_valid

    def _get_list_layout(self, request):
        pass

    def _get_item_layout(self, request):
        pass
