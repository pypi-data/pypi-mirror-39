APP_NAME = "dpup"


def _print(app, prefix, text):
  print(f"[{app}] {prefix:8} {text}")


def info(text, app=APP_NAME):
  _print(app, "info", text)


def warn(text, app=APP_NAME):
  _print(app, "warn", text)


def error(text, app=APP_NAME):
  _print(app, "error", text)
