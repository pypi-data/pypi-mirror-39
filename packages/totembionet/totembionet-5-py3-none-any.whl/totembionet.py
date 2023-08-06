# coding: utf-8

from argparse import ArgumentParser
import docker
import webbrowser
import os
import sys
import subprocess


dir_path = os.path.dirname(os.path.abspath(__file__))


IMAGE_NAME = 'totembionet'
CONTAINER_NAME = 'totembionet'
URL = 'http://localhost:8888'

COMMANDS = {}


def command(**kwargs):
    def wrapper(callback):
        COMMANDS[callback.__name__] = (kwargs, callback)
        return callback
    return wrapper


@command(help='build the image')
def build(namespace):
    subprocess.run(['docker', 'build', '-t', IMAGE_NAME, 'totembionet'],
                   stdout=sys.stdout, stderr=sys.stderr)


@command(help='build the image and start the container')
def up(namespace):
    build(namespace)
    subprocess.run(['docker-compose', 'up', '-d'], stdout=sys.stdout, stderr=sys.stderr)
    webbrowser.open(URL)


@command(help='start the container')
def start(namespace):
    subprocess.run(['docker-compose', 'start', '-d'], stdout=sys.stdout, stderr=sys.stderr)
    webbrowser.open(URL)


@command(help='stop the container')
def stop(namespace):
    subprocess.run(['docker-compose', 'stop'], stdout=sys.stdout, stderr=sys.stderr)


@command(help='stop the container and remove the images')
def down(namespace):
    subprocess.run(['docker-compose', 'down'], stdout=sys.stdout, stderr=sys.stderr)


def totembionet_image(client):
    try:
        return client.images.get(IMAGE_NAME)
    except docker.errors.ImageNotFound:
        return None


def totembionet_container(client):
    try:
        return client.containers.get(CONTAINER_NAME)
    except docker.errors.NotFound:
        return None


def main():
    parser = ArgumentParser(description="Totembionet interactive notebook docker.")
    subparsers = parser.add_subparsers(dest='command')

    for command, (kwargs, _) in COMMANDS.items():
        subparsers.add_parser(command, **kwargs)

    namespace = parser.parse_args()

    _, command = COMMANDS[namespace.command]
    with cd(dir_path):
        command(namespace)


class cd:
    def __init__(self, dirname):
        self.dirname = dirname

    def __enter__(self):
        self.curdir = os.getcwd()
        os.chdir(self.dirname)

    def __exit__(self, type, value, traceback):
        os.chdir(self.curdir)