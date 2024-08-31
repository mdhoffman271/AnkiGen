

import argparse
import os

from ankigen.src.cli.gen import generate_anki


# todo help text
def main():
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers(required=True)

    build_parser = subparsers.add_parser('build')
    build_parser.set_defaults(func=build)

    gen_parser = subparsers.add_parser('gen')
    gen_parser.set_defaults(func=gen)
    gen_parser.add_argument('spec_path', type=str)
    gen_parser.add_argument('out_dir', type=str)

    command_names = ', '.join(subparsers.choices.keys())
    main_parser.epilog = f'For more info: "ankigen {{{command_names}}} --help"'

    args = main_parser.parse_args()
    args.func(args)


def gen(args: argparse.Namespace):
    spec_path = args.spec_path
    out_dir = args.out_dir

    spec_path = os.path.abspath(spec_path)
    out_dir = os.path.abspath(out_dir)

    generate_anki(spec_path, out_dir)


def build(_: argparse.Namespace):
    # this will be an interactive tool to generate json/yaml
    raise NotImplementedError()


main()
