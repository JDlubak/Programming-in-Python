import json
import csv

from Sheep import Sheep


def get_round_info(round_number: int,
                         wolf_x_pos: float,
                         wolf_y_pos: float,
                         sheep_list: list[Sheep],
                         rounds_list: list[dict]) -> list[dict]:
    sheep_pos = [(sheep.x_pos, sheep.y_pos) for sheep in sheep_list]

    new_round = {
        "round_no": round_number,
        "wolf_pos": (wolf_x_pos, wolf_y_pos),
        "sheep_pos": sheep_pos,
    }

    rounds_list.append(new_round)
    return rounds_list


def save_round_to_json(rounds_list: list[dict]) -> bool:
    try:
        json_string = json.dumps(rounds_list)
        json_string = format_json_str(json_string, indent=4)
        with open('pos.json', 'w', encoding='utf-8') as file:
            file.write(json_string)
        return True
    except Exception as e:
        print(e)
        return False


def format_json_str(string: str, indent: int) -> str:
    """
    Format a compact JSON string to improve readability.

    This function reformats a one-line JSON string,
    adding newlines and indentation for dictionaries and lists.

    Args:
        string (str): The one-line string to format.
        indent (int): The number of spaces per indentation level.

    Returns:
        str: The formatted JSON string, ready to be saved to a file.
    """
    dict_indent = 1 * indent * " "
    key_indent = 2 * indent * " "
    end_sheep_list_indent = 3 * indent * " "
    sheep_list_indent = 4 * indent * " "
    replacements = {
        "]]}, {":
            f']\n{end_sheep_list_indent}]\n{dict_indent}'
            + "},\n" + f'{dict_indent}' + "{ ",
        "[{":
            f'[\n{dict_indent}' + "{ ",
        " \"":
            f'\n{key_indent}\"',
        "[[":
            f'[\n{sheep_list_indent}[',
        "], [":
            f'],\n{sheep_list_indent}[',
        "]}]":
            f'\n{end_sheep_list_indent}]\n{dict_indent}' + "}" + "\n]"
    }
    for key, value in replacements.items():
        string = string.replace(key, value)
    return string


def save_round_to_csv(alive_list: list[tuple]) -> bool:
    try:
        with open('alive.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Round", "Alive number"])
            writer.writerows(alive_list)
            return True
    except Exception as e:
        print(e)
        return False
