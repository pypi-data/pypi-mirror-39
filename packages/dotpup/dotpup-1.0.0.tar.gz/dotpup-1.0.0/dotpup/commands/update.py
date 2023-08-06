import platform

from .base import BaseCommand


class UpdateCommand(BaseCommand):
  def __init__(self):
    super().__init__(
        name="update",
        desc="Attempts to execute all recorded linking operations. "
        "Typically, you will clone or update your repository and run "
        "update to get any new files linked in your system. "
        "This command only creates links, never removes them. ")
    self.parser.add_argument(
        "--platform",
        help="Set this argument to apply a different platform from the "
        "currently running one. All operations will be recorded for the "
        "current platform.",
        required=False,
        default=platform.system())
    self.parser.add_argument(
        "--force",
        help="Force overwriting existing target files. A .bak backup will be "
        "created.",
        default=False,
        action="store_true")

  def run(self, args):
    from dotpup.config import load_config
    from dotpup.utils import get_repo_path
    from .link import do_link
    from os.path import expandvars
    from pathlib import Path
    cfg = load_config()
    if "operations" not in cfg:
      print("ERROR: No operations were recorded yet. Use `dpup store` "
            "and `dpup link` to record them manually.")
      return 1
    ops = cfg["operations"]
    if args.platform not in ops:
      print(f"ERROR: Platform '{args.platform}' has no recorded "
            "operations so far.")
      all_platforms = ", ".join(sorted(ops.keys()))
      if all_platforms:
        print(f"There are recorded operations for: {all_platforms}")
        print(
            "You may use --platform to apply operations from a different one.")
        return 1
    repo = get_repo_path()
    for src, dst in ops[args.platform].items():
      src = repo / src
      dst = Path(expandvars(dst))
      print(f"Linking {src} -> {dst}")
      if dst.exists():
        print("WARN: file exists, skipping.")
        continue
      do_link(src, dst)


command = UpdateCommand()