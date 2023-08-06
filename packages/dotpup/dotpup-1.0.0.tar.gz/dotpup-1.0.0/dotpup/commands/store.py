from pathlib import Path

from dotpup.utils import symlink, get_repo_path

import dotpup.output as output

from .base import BaseCommand


class StoreCommand(BaseCommand):
  def __init__(self):
    super().__init__(
        name="store",
        desc="Moves a file to the repository, creates a symlink in place "
        "of the original and records the operation")
    self.parser.add_argument("target_file")

  def run(self, args):
    import shutil
    from dotpup.utils import remove_prefix, get_repo_path, save_operation

    # Move to repo and symlink back
    repo = get_repo_path()
    target_file = Path(args.target_file).absolute()
    repo_file = Path(f"{repo}/{remove_prefix(target_file)}")
    repo_file.parent.mkdir(exist_ok=True, parents=True)
    shutil.move(args.target_file, repo_file)
    symlink(repo_file, target_file)

    save_operation(repo_file, target_file)
    return 0


command = StoreCommand()
