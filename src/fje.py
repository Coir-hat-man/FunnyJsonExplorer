
from utils import *
import json
import argparse
from loadIcon import *

def main():
    icon_factories,map,icon_choices = load_icon_factories('loadIcon.json')
    parser = argparse.ArgumentParser(description="Funny JSON Explorer (FJE)")
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the JSON file')
    parser.add_argument('-s', '--style', type=str, choices=['tree', 'rectangle'], required=True, help='Visualization style: tree or rectangle')
    parser.add_argument('-i', '--icon', type=str, choices=icon_choices, required=True, help='Icon family: simple')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        json_data = json.load(f)

    # if args.icon=='simple':
    #     icon_factory = SimpleIconFactory()
    # elif args.icon=='poker':
    #     icon_factory=PokerFaceFactory()
    icon_factory=map[args.icon]

    if args.style == 'tree':
        builder = TreeBuilder(icon_factory)
    elif args.style == 'rectangle':
        builder = RectangleBuilder(icon_factory)

    root_node = builder.build(json_data)

    # 打印根节点的子节点
    builder.show()

if __name__ == '__main__':
    main()