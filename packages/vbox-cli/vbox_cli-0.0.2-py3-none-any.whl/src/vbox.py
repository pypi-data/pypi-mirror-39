#!/usr/bin/python

import os
import argparse
import re
from subprocess import check_output, CalledProcessError



def get_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='sub-command help')

    # list
    parser_list = subparsers.add_parser('list', help='List existing VMs')
    parser_list.set_defaults(command='list')

    # running
    parser_running = subparsers.add_parser('running', help='List running VMs')
    parser_running.set_defaults(command='running')

    # start
    parser_start = subparsers.add_parser('start', help='Start a VM')
    parser_start.set_defaults(command='start')
    parser_start.add_argument('name', help='Name of VM to start')
    parser_start.add_argument("mode", choices=["gui", "sdl", "headless", "separate"], default="headless", nargs='?')

    # stop
    parser_stop = subparsers.add_parser('stop', help='Stop a VM gracefully')
    parser_stop.set_defaults(command='stop')
    parser_stop.add_argument('name', help='Name of VM to stop')

    # kill
    parser_kill = subparsers.add_parser('kill', help='Poweroff a VM')
    parser_kill.set_defaults(command='kill')
    parser_kill.add_argument('name', help='Name of VM to poweroff')

    # save
    parser_save = subparsers.add_parser('save', help='Save state of a VM and stop it')
    parser_save.set_defaults(command='save')
    parser_save.add_argument('name', help='Name of VM to save')

    # load ISO
    parser_save = subparsers.add_parser('load', help='Load an ISO file in a VM')
    parser_save.set_defaults(command='load')
    parser_save.add_argument('name', help='Name of VM')
    parser_save.add_argument('file', help='Path to ISO')

    # eject ISO
    parser_save = subparsers.add_parser('eject', help='Eject the ISO file attached to a VM')
    parser_save.set_defaults(command='eject')
    parser_save.add_argument('name', help='Name of VM')

    return parser

def run_command(cmd):
    try:
        return check_output(cmd, encoding="utf-8").strip()
    except CalledProcessError as e:
        print(e.output)
        exit(1)

def parse_vm_list(str):
    p = re.compile("\"(.*)\".*{(.*)}")

    for item in str:
        m = p.search(item)
        if m:
            print(m.group(1))

def cmd_list():
    cmd = ["VBoxManage", "list", "vms"]

    output = run_command(cmd).split("\n")
    parse_vm_list(output)

def cmd_running():
    cmd = ["VBoxManage", "list", "runningvms"]

    output = run_command(cmd).split("\n")
    parse_vm_list(output)

def cmd_start(name, mode):
    cmd = ["VBoxManage", "startvm", name, "--type", mode]
    output = run_command(cmd)

    print(output)

def cmd_restart(name):
    cmd = ["VBoxManage", "controlvm", name, "reset"]
    output = run_command(cmd)

    print(output)

def cmd_stop(name):
    cmd = ["VBoxManage", "controlvm", name, "acpipowerbutton"]
    output = run_command(cmd)

    print(output)

def cmd_kill(name):
    cmd = ["VBoxManage", "controlvm", name, "poweroff"]
    output = run_command(cmd)

    print(output)

def cmd_save(name):
    cmd = ["VBoxManage", "controlvm", name, "save"]
    output = run_command(cmd)

    print(output)

def cmd_load(name, file):
    filepath = os.path.abspath(file)
    if not os.path.isfile(filepath):
        print("ISO file does not exists")
        exit(1)

    cmd = [
        "VBoxManage", "storageattach", name, "--storagectl", "IDE", "--port", "0",
        "--device", "0", "--type", "dvddrive", "--medium", filepath
    ]

    output = run_command(cmd)

    print(output)

def cmd_eject(name):
    cmd = [
        "VBoxManage", "storageattach", name, "--storagectl", "IDE", "--port", "0",
        "--device", "0", "--medium", "none"
    ]

    output = run_command(cmd)

    print(output)


def main():
    parser = get_parser()
    args = parser.parse_args()

    if not hasattr(args, "command"):
        parser.print_help()
        exit(0)

    command = args.command.strip()
    if command == "list":
        cmd_list()
    elif command == "running":
        cmd_running()
    elif command == "start":
        cmd_start(args.name, args.mode)
    elif command == "restart":
        cmd_restart(args.name)
    elif command == "stop":
        cmd_stop(args.name)
    elif command == "kill":
        cmd_kill(args.name)
    elif command == "save":
        cmd_save(args.name)
    elif command == "load":
        cmd_load(args.name, args.file)
    elif command == "eject":
        cmd_eject(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()