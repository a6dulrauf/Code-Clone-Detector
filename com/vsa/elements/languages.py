# -*- coding: utf-8 -*-
"""Language registry for the clone detector.

The detector fingerprints code by keeping only structural tokens (keywords,
operators, type names) and comparing their n-gram frequencies. That vocabulary
is the *only* language-specific part of the pipeline — everything downstream
(n-grams -> frequency vectors -> cosine/euclidean) is language-agnostic.

Every language — the shipped ones and any you add — is defined the same way: a
JSON file in ./langdefs/ (loaded at import) or a definition uploaded at runtime.
There is no hardcoded, special-cased language; it's all data.
"""

import glob
import json
import os
import re

# A definition's vocabulary is capped so permutations() downstream can't blow up.
MAX_VOCAB = 250
_NAME_RE = re.compile(r'^[a-z0-9][a-z0-9_+.\-]*$')
DEFAULT = 'java'


class Language:
    """A programming language the detector can fingerprint."""

    def __init__(self, name, extensions, vocabulary, operators, label=None, aliases=None):
        self.name = name
        self.label = label or name.capitalize()
        self.extensions = tuple(extensions)
        # De-duplicate while preserving order — permutations() downstream must
        # not see the same token twice or feature columns would collide.
        seen = set()
        self.vocabulary = [t for t in vocabulary if not (t in seen or seen.add(t))]
        self.aliases = tuple(aliases or ())
        # Tokens treated as operators by the Halstead metric (everything else in
        # a line is counted as an operand).
        self.operators = list(operators or [])

    def __repr__(self):
        return "Language(%r, %r)" % (self.name, self.extensions)

    @classmethod
    def from_definition(cls, d):
        """Build a Language from a definition dict (see validate_definition).

        NGram vocabulary is keywords + operands + operators; the Halstead
        operator set is operators + keywords (operands are counted as operands).
        """
        keywords = list(d.get('keywords') or [])
        operators = list(d.get('operators') or [])
        operands = list(d.get('operands') or [])
        return cls(
            name=str(d['name']).strip().lower(),
            extensions=d['extensions'],
            vocabulary=keywords + operands + operators,
            operators=operators + keywords,
            label=d.get('label'),
            aliases=[str(a).strip().lower() for a in (d.get('aliases') or [])],
        )


_LANGUAGES = []
_BY_KEY = {}
# Names/aliases of the shipped (bundled) languages — frozen after load so an
# uploaded definition can't silently override a built-in.
_BUILTIN_NAMES = set()


def _reindex():
    _BY_KEY.clear()
    for lang in _LANGUAGES:
        _BY_KEY[lang.name] = lang
        for alias in lang.aliases:
            _BY_KEY.setdefault(alias, lang)


def validate_definition(d):
    """Return a list of human-readable problems with a language definition dict
    (empty list == valid). Used for both bundled files and user uploads."""
    if not isinstance(d, dict):
        return ['Definition must be a JSON object.']
    errors = []

    name = d.get('name')
    if not isinstance(name, str) or not name.strip():
        errors.append('"name" is required (e.g. "javascript").')
    else:
        n = name.strip().lower()
        if not _NAME_RE.match(n):
            errors.append('"name" may contain only letters, digits and _ + . -')
        if n in _BUILTIN_NAMES:
            errors.append('"%s" is a built-in language; choose a different name.' % n)

    exts = d.get('extensions')
    if not isinstance(exts, list) or not exts:
        errors.append('"extensions" must be a non-empty list, e.g. [".js", ".jsx"].')
    elif any((not isinstance(e, str) or not e.startswith('.') or len(e) < 2) for e in exts):
        errors.append('each extension must be a string like ".js".')

    for field in ('keywords', 'operators'):
        v = d.get(field)
        if not isinstance(v, list) or not v:
            errors.append('"%s" must be a non-empty list of strings.' % field)
        elif any((not isinstance(t, str) or t == '') for t in v):
            errors.append('"%s" must contain only non-empty strings.' % field)

    operands = d.get('operands', [])
    if not isinstance(operands, list) or any(not isinstance(t, str) for t in operands):
        errors.append('"operands" must be a list of strings (or omitted).')

    vocab = [t for t in (list(d.get('keywords') or []) + list(d.get('operators') or [])
                         + list(operands or [])) if isinstance(t, str)]
    if len(set(vocab)) > MAX_VOCAB:
        errors.append('too many tokens (%d distinct); keep it under %d.' % (len(set(vocab)), MAX_VOCAB))
    return errors


def register(language):
    """Add or replace a Language in the registry (in place, preserving order)."""
    for i, lang in enumerate(_LANGUAGES):
        if lang.name == language.name:
            _LANGUAGES[i] = language
            _reindex()
            return language
    _LANGUAGES.append(language)
    _reindex()
    return language


def register_definition(d):
    """Validate a definition dict and register it. Raises ValueError if invalid."""
    errors = validate_definition(d)
    if errors:
        raise ValueError('; '.join(errors))
    return register(Language.from_definition(d))


def _load_bundled():
    """Load every JSON language definition in ./langdefs/ at import time."""
    dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'langdefs')
    for path in sorted(glob.glob(os.path.join(dirpath, '*.json'))):
        try:
            with open(path) as f:
                register_definition(json.load(f))
        except Exception as e:   # a bad bundled file must not break startup
            print('languages: skipped %s (%s)' % (os.path.basename(path), e))


_load_bundled()

# Freeze the set of shipped names so runtime uploads can't override them.
for _lang in _LANGUAGES:
    _BUILTIN_NAMES.add(_lang.name)
    _BUILTIN_NAMES.update(_lang.aliases)


def get(name):
    """Return the Language for a name/alias (case-insensitive); DEFAULT by default."""
    key = str(name).strip().lower() if name else DEFAULT
    return _BY_KEY.get(key) or _BY_KEY.get(DEFAULT) or (_LANGUAGES[0] if _LANGUAGES else None)


def extensions(name):
    """File extensions (tuple) for the given language name/alias."""
    return get(name).extensions


def is_builtin(name):
    return str(name).strip().lower() in _BUILTIN_NAMES


def _ordered_names():
    names = [lang.name for lang in _LANGUAGES]
    rest = sorted(n for n in names if n != DEFAULT)
    return ([DEFAULT] if DEFAULT in names else []) + rest


def choices():
    """Canonical language names — the default language first, then alphabetical."""
    return _ordered_names()


def options():
    """(name, label) pairs for UI selectors — default first, then alphabetical."""
    return [(n, _BY_KEY[n].label) for n in _ordered_names()]


def template():
    """A blank definition users can fill in — powers the upload help/template.
    Uses a name that isn't shipped so it can be submitted as-is to try it out."""
    return {
        "name": "swift",
        "label": "Swift",
        "extensions": [".swift"],
        "keywords": ["func", "let", "var", "class", "struct", "enum", "if", "else",
                     "for", "while", "return", "guard", "switch", "case", "import",
                     "init", "self", "nil", "true", "false"],
        "operators": ["{", "}", "(", ")", "[", "]", "+", "-", "*", "/", "=", "==",
                      "!=", "<", ">", "<=", ">=", "&&", "||", "->", ".", ",", ":", ";"],
        "operands": ["Int", "String", "Bool", "Double", "Float", "Array", "Dictionary"]
    }
