import re
from ipaddress import ip_address
from rest_framework.serializers import Field, ValidationError


class MegaByteField(Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if isinstance(data, int):
            return data
        elif isinstance(data, str):
            data = data.upper()
            match = re.match(r'(\d+) *([MG])B*', data)
            if match:
                value = int(match.group(1))
                if match.group(2) == "M":
                    return value
                if match.group(2) == "G":
                    return value * 1024
                if match.group(2) == "K":
                    return value // 1024
            else:
                raise ValidationError("illegal size format")
        else:
            raise ValidationError("illegal type")


class IPListField(Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            [ip_address(ip) for ip in data.split(',')]
        except ValueError:
            raise ValidationError("not ipv4 address")
        return data
