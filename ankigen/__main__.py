

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
    gen_parser.add_argument('lang', type=str)
    gen_parser.add_argument('spec_path', type=str)
    gen_parser.add_argument('out_path', type=str)

    command_names = ', '.join(subparsers.choices.keys())
    main_parser.epilog = f'For more info: "ankigen {{{command_names}}} --help"'

    args = main_parser.parse_args()
    args.func(args)


def gen(args: argparse.Namespace):
    lang = args.lang
    spec_path = args.spec_path
    out_path = args.out_path

    if out_path.endswith(os.path.sep) or out_path.endswith('.'):
        out_path = os.path.join(out_path, f'{lang}.txt')

    spec_path = os.path.abspath(spec_path)
    out_path = os.path.abspath(out_path)

    generate_anki(lang, spec_path, out_path)


def build(_: argparse.Namespace):
    # this will be an interactive tool to generate json/yaml
    raise NotImplementedError()


main()
