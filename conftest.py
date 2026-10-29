# Root conftest: its presence makes pytest prepend the repo root to
# sys.path, so `import src...` resolves when tests run from a fresh
# checkout even before the package is installed.