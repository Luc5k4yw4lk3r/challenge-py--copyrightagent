from argparse import ArgumentParser
from getColor import getColor
from typing import List, Any, Dict


COMMANDS = [
    {"--format": {"dest": "format", "help": "Shown in format. Example: hex or rgb"}},
    {
        "--color-list": {
            "dest": "color_list",
            "nargs": "+",
            "required": "True",
            "help": "The information will be returned in the order in which the parameters are passed. Example: blue red black",
        }
    },
]

SCRIPT_DESCRIPTION = (
    "This script allows us to obtain details of information of different colors."
    "By default, the information is displayed in this format: Color(name=black, hex=#000000, rgb={'R': 0, 'G': 0, 'B': 0})"
    "Execution script example: ./colors.py --format hex --color-list black green blue caqui red"
)

FORMATS = ["hex", "rgb"]


class Color(object):
    def __init__(self, name, HEX, RGB):
        self.name = name
        self.hex = HEX
        self.rgb = RGB

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if len(value) < 2:
            raise AttributeError(f"The attribute name:{value} is not valid")
        self.__name = value.upper()

    @property
    def hex(self):
        return self.__hex

    @hex.setter
    def hex(self, value: str):
        if len(value) < 2:
            raise AttributeError(f"The attribute hex:{value} is not valid")
        self.__hex = value.upper()

    @property
    def rgb(self):
        return self.__rgb

    @rgb.setter
    def rgb(self, value: Dict):
        if not value:
            raise AttributeError(f"The attribute rgb:{value} is not valid")
        self.__rgb = value

    def __repr__(self) -> str:
        return f"Color(name={self.name}, hex={self.hex}, rgb={self.rgb})"


def build_parser() -> object:
    parser = ArgumentParser(description=SCRIPT_DESCRIPTION)
    for command in COMMANDS:
        for command_name, options in command.items():
            parser.add_argument(command_name, **options)
    return parser


def main() -> None:
    parser = build_parser()
    options = parser.parse_args()

    colors, colors_not_found = getColors(options.color_list)

    print("\n\nInformation about colors")
    if options.format in FORMATS:
        output(colors, ["name", options.format])
    else:
        output(colors)
    print("\n\nColors not found")
    output(colors_not_found)


def output(items: List, attributes: Any = None) -> None:
    for item in items:
        if not attributes:
            print(item)
        else:
            for att in attributes:
                value = getattr(item, att)
                print(value, end=" ")
            print("")


def getColors(color_name_list: List[str]) -> List:
    colors_detail = []
    colors_errors = []
    for color_name in color_name_list:
        try:
            color_detail = getColor(color_name)
            if not color_detail:
                raise ValueError(f"The color:{color_name} was not found")
            colors_detail.append(Color(**color_detail))
        except (ValueError, AttributeError) as e:
            colors_errors.append((color_name, f"{e}"))
    return colors_detail, colors_errors


if __name__ == "__main__":
    main()