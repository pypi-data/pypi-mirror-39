from argparse import ArgumentParser
from textwrap import TextWrapper

from abc import abstractmethod, ABC


class BaseCommand(ABC):
  def __init__(self, name, desc):
    self.name = name
    self.parser = ArgumentParser(description=desc)
    prog = self.parser.prog
    self.parser.prog = f"{prog} {self.name}"

  def __call__(self, args):
    parsed_args = self.parser.parse_args(args)
    return self.run(parsed_args)

  def format_help(self):
    wrapper = TextWrapper()
    lines = wrapper.wrap(f"  {self.name:8}{self.parser.description}")
    first, rest = lines[0], lines[1:]
    final = [first]
    for line in rest:
      final.append(" " * 10 + line)
    return "\n".join(final)

  def format_usage(self):
    usage = self.parser.format_usage()
    usage = usage.replace(self.parser.prog, f"{self.parser.prog} {self.name}")
    return f""

  @abstractmethod
  def run(self, args) -> int:
    pass