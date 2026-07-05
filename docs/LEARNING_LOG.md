--- 0.2
def + type hints: функции в Python, аннотации типов как документация для IDE
pytest discovery: файлы test_*.py, функции test_* — никакой регистрации
ruff --fix: линтер умеет автоматически исправлять некоторые нарушения


--- 0.3
__init__.py запускается при import qsat — всё в нём становится атрибутом пакета
pathlib.Path + __file__ — надёжный способ строить пути относительно файла, независимо от cwd
[build-system] + uv sync — делает пакет installable, import qsat работает везде в venv


--- 0.4
GitHub Actions: YAML-описание пайплайна, uses: vs run:
[build-system] в pyproject.toml делает пакет installable — без этого import qsat работает только в pytest
Deprecation warning ≠ ошибка: CI зелёный, предупреждение уйдёт когда авторы обновят экшены