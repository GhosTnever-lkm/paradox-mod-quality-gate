# Paradox Mod Quality Gate

**Открытый preflight-набор для модов Paradox:** запускает ModRelease Studio и Paradox Mod Workbench в GitHub Actions, сводит результаты в один отчёт и показывает находки рядом с pull request.

[![CI](https://github.com/GhosTnever-lkm/paradox-mod-quality-gate/actions/workflows/ci.yml/badge.svg)](https://github.com/GhosTnever-lkm/paradox-mod-quality-gate/actions/workflows/ci.yml) · [![Version](https://img.shields.io/github/v/release/GhosTnever-lkm/paradox-mod-quality-gate?sort=semver)](https://github.com/GhosTnever-lkm/paradox-mod-quality-gate/releases) · ![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

> Анализаторы проверяют структуру и известные правила. Чистый отчёт не гарантирует, что мод запускается в игре или полностью совместим.

## Возможности

- проверки метаданных, локализации, упаковки и секретов через [ModRelease Studio](https://github.com/GhosTnever-lkm/modrelease-studio);
- сравнение файлов модпака, зависимостей и Clausewitz-скриптов через [Paradox Mod Workbench](https://github.com/GhosTnever-lkm/paradox-mod-workbench);
- GitHub error/warning annotations, сводка job и JSON/Markdown отчёты;
- режимы блокировки: `error`, `warning` или `never`;
- сканеры работают только для чтения; artifact содержит только отчёты, не ZIP и не исходники мода.

## Быстрый старт

Сохраните как `.github/workflows/mod-quality.yml`:

```yaml
name: Mod quality
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  preflight:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: GhosTnever-lkm/paradox-mod-quality-gate@v1.0.11
        with:
          mod-path: .
          gate: error
```

Папка `mod-path` передаётся обоим сканерам. Для Workbench можно задать `workbench-paths` — несколько папок или ZIP, по одному пути на строку. Пути должны существовать внутри workspace.

## Входы

| Input | По умолчанию | Описание |
|---|---|---|
| `mod-path` | `.` | Папка/ZIP для ModRelease Studio и путь Workbench, если список ниже пуст. |
| `config-file` | пусто | Путь к TOML-политике ModRelease Studio внутри workspace. |
| `workbench-paths` | пусто | Список папок/ZIP Workbench, каждый путь с новой строки. |
| `gate` | `error` | `error`, `warning` или `never`. Ошибки сканера/входа всегда завершают action с ошибкой. |
| `python-version` | `3.12` | Версия Python. |
| `artifact-name` | `paradox-mod-quality-report` | Название отчётного artifact. |

## Пользовательская политика релиза

Передайте `config-file` с TOML-политикой ModRelease Studio, чтобы включить проверки обязательных путей. Путь должен быть внутри checkout. `ERROR`-находка попадёт в общий отчёт и заблокирует стандартный `gate: error`; прошедшая политика не блокирует запуск. CI проверяет это на фикстуре с намеренно отсутствующим файлом.

```yaml
- uses: GhosTnever-lkm/paradox-mod-quality-gate@v1.0.11
  with:
    mod-path: path/to/mod
    config-file: path/to/mod/modrelease.toml
    gate: error
```

```toml
[scan]
required_paths = ["descriptor.mod", "README.md"]
required_paths_severity = "ERROR"
```

## Артефакты и данные

В job summary показываются counts и до 50 findings. JSON/Markdown сохраняются в каталоге отчётов и загружаются даже при блокирующих находках. Отчёты содержат относительные пути, коды и диагностические сообщения. Исходные файлы, архивы, полный manifest и абсолютные локальные пути в artifact не попадают. GitHub сохраняет artifacts согласно настройкам репозитория и сроку хранения Actions.

Не запускайте это действие в `pull_request_target` для непроверенного кода: используйте обычный `pull_request` на GitHub-hosted runner. В action нет токена записи, PR-комментариев или модификации checkout.

## Локальное использование

```powershell
python -m pip install "modrelease-studio @ git+https://github.com/GhosTnever-lkm/modrelease-studio.git@v0.3.7"
python -m pip install "paradox-mod-workbench @ git+https://github.com/GhosTnever-lkm/paradox-mod-workbench.git@v0.2.1"
modrelease scan . --json-out modrelease.json --md-out modrelease.md
pmw scan . --format json --output workbench.json
python runner/aggregate.py --modrelease modrelease.json --workbench workbench.json --json-out report.json --md-out report.md --gate error
```

## Платный Pro-набор

Бесплатная GitHub Action и CLI-режим остаются открытыми. **Pro Edition** — отдельный Windows-пакет с графическим пакетным запуском нескольких папок/ZIP и HTML-сводкой. Он использует те же открытые сканеры; дополнительные game-specific правила не заявляются.

Получить Pro: [Windows-набор на Boosty — 50 ₽](https://boosty.to/azizazimov/posts/761380dd-5d2d-45d1-ad6d-452b123d11b3). Подробнее о бесплатной версии и релизах: [открытый анонс](https://boosty.to/azizazimov/posts/b17a51a0-9dbf-4427-b810-700cfbfef3ab).

## Разработка

```console
python -m unittest discover -s tests -v
```

## Лицензия

MIT. См. [LICENSE](LICENSE).
