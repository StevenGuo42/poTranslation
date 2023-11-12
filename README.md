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

### CLI Examples

#### Translate a `.po` file

```bash
potranslate ./messages.po                       # translate untranslated text from 'en' to language specified in the .po file, save to ./messages.po
potranslate ./messages.po -s en -l zh           # translate from 'en' to 'zh'
potranslate ./messages.po -o ./translated.po    # translated .po file, save to ./translated.po
potranslate ./messages.po -F                    # force translation of all entries
potranslate ./messages.po -w                    # translate and NOT write to the file
```

#### Translate a directory of `.po` files

This would work with the `.po` files compiled by `pybabel`

```bash
potranslate -d app/translations                 # translate app/translations/<locale>/LC_MESSAGES/<domain>.mo
potranslate -d app/translations -l zh           # translate app/translations/zh/LC_MESSAGES/<domain>.mo
potranslate -d app/translations -D messages     # translate app/translations/<locale>/LC_MESSAGES/messages.mo
```
#### CLI Usage

```text
Usage: potranslate [OPTIONS] [PO_FILE_PATH]
Options:
  -s, --source_language TEXT  Translate from (language).  [default: en]
  -l, --locale TEXT           Translate to (language).  [default: (load from .po file)]
  -L, --lang TEXT             Programming langrage of formatted string.  [default: python]
  -o, --output PATH           Path to the output file.  [default: {po_file_path}]
  -e, --env PATH              Path to the env file.  [default: (load from cwd and parent dir)]
  -d, --directory PATH        Directory of the PO files.
  -D, --domain TEXT           Domain of the PO file.
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