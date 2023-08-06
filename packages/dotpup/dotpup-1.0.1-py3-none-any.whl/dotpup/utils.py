import os
import platform

from pathlib import Path

from . import config


def get_repo_path() -> Path:
  if "DOTPUP_HOME" not in os.environ:
    raise RuntimeError("ERROR: Please set DOTPUP_HOME.")
  return Path(os.getenv("DOTPUP_HOME"))


def shellify_var(var_name: str) -> str:
  if platform.system() == "Windows":
    return f"%{var_name}%"
  else:
    return f"${var_name}"


def unexpand(filepath, env_var="HOME") -> str:
  filepath = str(filepath)
  val = os.getenv(env_var)
  return filepath.replace(val, shellify_var(env_var))


def remove_prefix(filepath, env_var="HOME") -> str:
  filepath = str(filepath)
  val = os.getenv(env_var)
  unprefixed = filepath.replace(val, "")
  print(unprefixed)
  if unprefixed[0] in ("/", "\\"):
    unprefixed = unprefixed[1:]
  return unprefixed


def symlink(src: Path, dst: Path, record=True):
  src = src.absolute()
  dst = dst.absolute()
  system = platform.system()
  if system != "Windows":
    os.symlink(src, dst)
  else:
    raise NotImplementedError()


def save_operation(repo_file: Path, target_file: Path):
  repo_file = str(repo_file.absolute().relative_to(get_repo_path()))
  target_file = str(unexpand(target_file.absolute()))

  cfg = config.load_config()
  if "operations" not in cfg:
    cfg["operations"] = {}

  os_name = platform.system()
  if os_name not in cfg["operations"]:
    cfg["operations"][os_name] = {}
  cfg["operations"][os_name][repo_file] = target_file
  config.save_config(cfg)