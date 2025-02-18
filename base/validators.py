from datetime import datetime
import pytz
from rest_framework.exceptions import ValidationError


def validate_charfield_length(name, name_str):
    if len(name) < 3:
        raise ValidationError(f"{name_str} field must consist of at least 3 characters.")
    return name

def validate_if_dt_not_from_the_future(dt, dt_name):
    now_utc = datetime.now(pytz.UTC)
    if dt > now_utc:
        raise ValidationError(f"{dt_name} datetime cannot be from the future.")
    return dt

def validate_system_name(system_name):
    return validate_charfield_length(system_name, "System name")


def validate_activation_dt(activation_dt):
    return validate_if_dt_not_from_the_future(activation_dt, "Activation")


def validate_sensor_name(sensor_name):
    return validate_charfield_length(sensor_name, "Sensor name")


def validate_read_dt(read_dt):
    return validate_if_dt_not_from_the_future(read_dt, "Sensor reading")