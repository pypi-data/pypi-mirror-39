from dotpup.utils import symlink, save_operation
from pathlib import Path

from .base import BaseCommand


def do_link(repo_file: Path, target_file: Path):
  if target_file.is_dir():
    target_file = target_file / repo_file.name

  if not target_file.parent.exists():
    target_file.parent.mkdir(parents=True, exist_ok=True)

  symlink(repo_file, target_file)
  save_operation(repo_file, target_file)


class LinkCommand(BaseCommand):
  def __init__(self):
    super().__init__(
        name="link",
        desc="Creates a symlink from a repo file to a target location "
        "and records the operation in dotpup.json for autolinking.")
    self.parser.add_argument("repo_file")
    self.parser.add_argument("target_file")

  def run(self, args):
    repo_file = Path(args.repo_file)
    target_file = Path(args.target_file)
    do_link(repo_file, target_file)
    return 0


command = LinkCommand()
