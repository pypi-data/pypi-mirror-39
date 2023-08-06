# vbox

A simple wrapper for VirtualBox's VBoxManage cli. It allows you to control and list VMs and attach/detach ISO files.

# Install

`pip install vbox-cli`

# Usage

## List existing VMs
`vbox list`

## List running VMs
`vbox running`

## Start a VM
`vbox start <NAME> [MODE]`

Mode can be

- gui
- sdl
- headless
- separate

## Stop a VM
This command sends a ACPI power off

`vbox stop <NAME>`

## Kill a VM
This command power off the VM

`vbox kill <NAME>`

## Save state and stop a VM
`vbox save <NAME>`

## Load an ISO file on a VM
`vbox load <NAME> <FILENAME>`

## Eject an ISO attached to a VM
`vbox eject <NAME>`
