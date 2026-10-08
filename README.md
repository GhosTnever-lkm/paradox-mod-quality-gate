# Paradox Mod Quality Gate

**Открытый preflight-набор для модов Paradox:** запускает ModRelease Studio и Paradox Mod Workbench в GitHub Actions, сводит результаты в один отчёт и показывает находки рядом с pull request.

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
      - uses: GhosTnever-lkm/paradox-mod-quality-gate@v1.0.0
        with:
          mod-path: .
          gate: error
```

Папка `mod-path` передаётся обоим сканерам. Для Workbench можно задать `workbench-paths` — несколько папок или ZIP, по одному пути на строку. Пути должны существовать внутри workspace.

## Входы

| Input | По умолчанию | Описание |
|---|---|---|
| `mod-path` | `.` | Папка/ZIP для ModRelease Studio и путь Workbench, если список ниже пуст. |
| `workbench-paths` | пусто | Список папок/ZIP Workbench, каждый путь с новой строки. |
| `gate` | `error` | `error`, `warning` или `never`. Ошибки сканера/входа всегда завершают action с ошибкой. |
| `python-version` | `3.12` | Версия Python. |
| `artifact-name` | `paradox-mod-quality-report` | Название отчётного artifact. |

## Артефакты и данные

В job summary показываются counts и до 50 findings. JSON/Markdown сохраняются в каталоге отчётов и загружаются даже при блокирующих находках. Отчёты содержат относительные пути, коды и диагностические сообщения. Исходные файлы, архивы, полный manifest и абсолютные локальные пути в artifact не попадают. GitHub сохраняет artifacts согласно настройкам репозитория и сроку хранения Actions.

Не запускайте это действие в `pull_request_target` для непроверенного кода: используйте обычный `pull_request` на GitHub-hosted runner. В action нет токена записи, PR-комментариев или модификации checkout.

## Локальное использование

```powershell
python -m pip install "modrelease-studio @ git+https://github.com/GhosTnever-lkm/modrelease-studio.git@v0.2.1"
python -m pip install "paradox-mod-workbench @ git+https://github.com/GhosTnever-lkm/paradox-mod-workbench.git@v0.2.1"
modrelease scan . --json-out modrelease.json --md-out modrelease.md
pmw scan . --format json --output workbench.json
python runner/aggregate.py --modrelease modrelease.json --workbench workbench.json --json-out report.json --md-out report.md --gate error
```

## Платный Pro-набор

Бесплатная GitHub Action и CLI-режим остаются открытыми. **Pro Edition** — отдельный Windows-пакет с графическим пакетным запуском нескольких папок/ZIP и HTML-сводкой. Он использует те же открытые сканеры; дополнительные game-specific правила не заявляются.

Получить Pro: [Boosty — ссылка появится после публикации набора](https://boosty.to/azizazimov).

## Разработка

```console
python -m unittest discover -s tests -v
```

## Лицензия

MIT. См. [LICENSE](LICENSE).
