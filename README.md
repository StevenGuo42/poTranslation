# poTranslation

## Description

This is a simple python library/CLI tool to translate `.po` files using various APIs.

## Installation

Install and update using [pip][PIP]:

```bash
pip install -U poTranslation
```

## Usage

Create a `.env` file in your working directory or parent directory with the following content for the API you want to use:   

```properties
TRANSLATOR_SERVICE=YOUR_TRANSLATOR_SERVICE
MS_API_KEY=YOUR_MS_API_KEY
MS_API_REGION=YOUR_MS_API_REGION
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

### Command Line Interface Example

```bash
potranslate --help
poTranslate ./messages.po -s en -d zh -f
```

```text
Options:
  -s, --source-language TEXT  Source language for translation.  [default: en]
  -d, --dest-language TEXT    Destination language for translation.  [default: (load from .po file)]
  -l, --lang TEXT             Programming langrage of formatted string.  [default: python]
  -f, --file PATH             Path to the output file.  [default: {po_file_path}]
  -e, --env PATH              Path to the env file.  [default: (load from cwd and parent dir)]
  -F, --force                 Force translation of all entries.
  -v, --verbose               Enable verbose output.
  -q, --quiet                 Suppress output.
  -w, --write                 Write to the file.  [default: True]
  -h, --help                  Show this message and exit.
```

## Roadmap

- [ ] Multiple translation services support
  - [x] [Microsoft Translate API][MS-API]
  - [x] [OpenAI API][OPENAI-API]
  - [ ] [Google Translate API][GOOGLE-API]
  - [ ] [DeepL API][DEEPL-API]

> **_Challenge:_**  Some services require an glossary to be created before translation for formatted strings with placeholders. 

## License
Distributed under the BSD 3-Clause License. See `LICENSE` for more information.

## Links

Source Code: [https://github.com/StevenGuo42/poTranslation](https://github.com/StevenGuo42/poTranslation)  
Issue Tracker: [https://github.com/StevenGuo42/poTranslation/issues](https://github.com/StevenGuo42/poTranslation/issues)
PyPI: [https://pypi.org/project/poTranslation/](https://pypi.org/project/poTranslation/)

[//]: # (Links)
[PIP]: https://pip.pypa.io/en/stable/getting-started/
[MS-API]: https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/v3-0-reference
[OPENAI-API]: https://platform.openai.com/docs/guides/text-generation/chat-completions-api
[GOOGLE-API]: https://cloud.google.com/translate/docs/reference/api-overview
[DEEPL-API]: https://www.deepl.com/docs-api/translate-text