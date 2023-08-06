#!/usr/bin/env python
from .modules.trapeze import Trapeze
import json, argparse, click
from pathlib import Path
import colorama as c

@click.command()
@click.argument('action', type=click.Choice(['push','pull', 'init']))
@click.option('--config', default=".trapeze")
def main(action, config) :
    # initialize colorama for cli output
    c.init()

    if action == "init" :
        click.echo(c.Fore.BLACK + c.Back.GREEN + "Generating configuration file..." + c.Style.RESET_ALL)
        createConfig(config)
        exit

    # Open Config
    try :
        with open(config) as f :
            config_data = json.load(f)
    except FileNotFoundError :
        config_data = createConfig(config)

    # Init Trapeze
    t = Trapeze(config_data['name'], config_data['bucket'])
    files = config_data['files']
    t.add_files(files)

    # handle action
    click.echo(c.Fore.BLACK + c.Back.GREEN + "{0}ing to {1}...".format(action.capitalize(), config_data['bucket']) + c.Style.RESET_ALL)
    if action == "push" :
        t.push()
    elif action == "pull" :
        t.pull()

def createConfig(config) :
    if click.confirm("The config file ({0}) was not found.  Create one?".format(config), default = True) :
        # Open Global Config
        global_config_file = "{0}/.trapeze".format( str(Path.home()) )
        try :
            global_config_data = { "bucket": None }
            with open(global_config_file) as f :
                global_config_data = json.load(f)
        except FileNotFoundError :
            pass

        data = {
            "name": click.prompt("Application Name"),
            "bucket": click.prompt("AWS S3 Bucket", default = global_config_data['bucket'] ),
            "files": []
        }
        # get existing files
        t = Trapeze(data['name'], data['bucket'])
        objects = t.get_files()
        if "Contents" in objects :
            data['files'] = [ x['Key'].replace(data['name'] + "/", "") for x in objects['Contents'] ]
        click.echo(data)
        if click.confirm("Add files?", default=True) :
            # populate files
            click.echo("Which files would you like to track?")
            while True :
                filename = click.prompt("File Path")
                data['files'].append(filename)
                click.echo(data['files'])
                if not click.confirm("Add more?", default=True) :
                    break

        # save
        with open(config, 'w') as f :
            json.dump(data, f)

        return data
