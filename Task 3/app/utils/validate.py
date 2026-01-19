from typing import Any, Tuple, Type

from app.models import Data

AVAILABLE_KEYS = ['category', 'width', 'height', 'length', 'weight']
FLOAT_VALS = ['width', 'height', 'length', 'weight']


def validate_point(input_data: dict,
                   is_prediction: bool = False,
                   for_api: bool = False) -> Tuple[bool, Any]:
    if not isinstance(input_data, dict):
        return False, "Invalid or missing JSON body."

    values = {}
    errors = []

    for key in AVAILABLE_KEYS:
        if is_prediction and key == 'category':
            if 'category' in input_data:
                errors.append("category is not allowed for predictions")
            continue

        if key not in input_data:
            errors.append(f"{key} is required")
            continue

        value = input_data[key]
        expected = (int, float) if key in FLOAT_VALS else int
        err = get_field_value_error(value, expected, key)
        if err:
            errors.append(err)
        else:
            values[key] = value

    for extra_key in input_data:
        if extra_key not in AVAILABLE_KEYS:
            errors.append(f"unexpected field: {extra_key}")

    if errors:
        if for_api:
            return False, errors
        message_start = "An error occurred: " if len(errors) == 1 \
            else "Multiple errors occurred:<br>"
        return False, message_start + ",<br>".join(errors) + "."

    else:
        point = Data(
            category=values['category'] if not is_prediction else None,
            width=values['width'],
            height=values['height'],
            length=values['length'],
            weight=values['weight']
        )
        return True, point


def get_field_value_error(value: Any,
                          expected_type: Type | Tuple[Type, ...],
                          field_name: str) -> str:
    if value is None:
        return f'value for {field_name} is required'
    if isinstance(value, str) and value.strip() == "":
        return f'{field_name} must not be empty'
    try:
        if isinstance(expected_type, tuple):
            if float in expected_type or int in expected_type:
                value = float(value)
        elif expected_type == int:
            value = int(value)
        elif expected_type == float:
            value = float(value)
    except (ValueError, TypeError):
        type_names = " or ".join([t.__name__ for t in expected_type]) \
            if isinstance(expected_type, tuple) \
            else expected_type.__name__
        return f'{field_name} must be {type_names}'
    if value <= 0:
        return f'{field_name} must be greater than 0'
    return ""


def validate_point_id(point_id: Any) -> Tuple[bool, str]:
    try:
        point_id = int(point_id)
        if point_id <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return False, "Invalid id, must be a positive integer"
    return True, ""
