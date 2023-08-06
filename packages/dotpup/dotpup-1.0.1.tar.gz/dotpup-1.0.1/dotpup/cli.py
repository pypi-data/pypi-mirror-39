from argparse import ArgumentParser
from importlib import import_module
from sys import argv

from dotpup import output


class DotPup(ArgumentParser):
  # list of allowed commands to protect
  # from importing arbitrary modules
  commands = ["link", "store", "update"]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.add_argument("command")
    self.all_commands = self.load_all("dotpup.commands")

  def load_all(self, module_name):
    all_commands = {}
    for cmd in self.commands:
      mod = import_module(f"{module_name}.{cmd}")
      all_commands[cmd] = mod.command
    return all_commands

  def print_help(self):
    super().print_help()
    print("\ncommands:")
    for cmd in self.all_commands.values():
      print(cmd.format_help(), end="\n\n")

  def run_command(self, cmd, args) -> int:
    if cmd not in self.commands:
      output.error("No such command.")
      return 1
    command = self.all_commands[cmd]
    return command(args)

  def run(self) -> int:
    args = self.parse_args(argv[1:2])
    rest = argv[2:]
    return self.run_command(args.command, rest)


def cli():
  exit(DotPup().run())
