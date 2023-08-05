#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "youliangzhang"
import click
import six
import hello52

def read_config(ctx, param, value):
    if not value:
        return {}
    import json

    def underline_dict(d):
        if not isinstance(d, dict):
            return d
        return dict((k.replace('-', '_'), underline_dict(v)) for k, v in six.iteritems(d))

    config = underline_dict(json.load(value))
    ctx.default_map = config
    return config

@click.group(invoke_without_command=True)
@click.option('-c', '--config', callback=read_config, type=click.File('r'),
              help='a json file with default values for subcommands. {"webui": {"port":5001}}')
@click.option('--debug', envvar='DEBUG', default=False, is_flag=True, help='debug mode')
@click.version_option(version=hello52.version.__version__, prog_name=hello52.version.script_name)
@click.pass_context
def cli(ctx,**kwargs):
    print('-'*30)
    print(ctx)
    print('-'*30)
    print(kwargs)
    print(dir(hello52))


def main():
    cli()



if __name__ == '__main__':
    main()