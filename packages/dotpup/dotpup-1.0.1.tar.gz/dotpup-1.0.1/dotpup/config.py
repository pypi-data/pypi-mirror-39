import json

config_filename = "dotpup.json"


def _conf_path():
  from dotpup.utils import get_repo_path
  return get_repo_path() / config_filename


def load_config():
  conf_path = _conf_path()
  if not conf_path.exists():
    with conf_path.open("w") as cfg:
      json.dump({}, cfg)
      return {}

  with conf_path.open() as cfg:
    return json.load(cfg)


def save_config(cfg_data: dict):
  with open(_conf_path(), "w") as cfg:
    json.dump(cfg_data, cfg, sort_keys=True, indent=2)
