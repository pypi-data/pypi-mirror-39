# Hashstate

This is a Python C extension module that forks the ``hashlib`` implementation
from CPython itself to add support for a single feature: the ability to
serialize and deserialize hash objects so that the hash objects do not have
to persist in memory for the whole duration of the hash computation.

## Usage

```bash
pip install hashstate
```

```python
import hashstate

# Contains all the same constructors as hashlib
hash1 = hashstate.sha512()
hash1.update('...')
s = hash1.serialize()  # gives back bytes object

hash2 = hashstate.sha512()
hash2.deserialize(s)
assert hash1.digest() == hash2.digest()
```

## Developers

Build the package:

    python setup.py sdist bdist_wheel

If building a MacOS distribution package, also run:

    delocate-wheel ./dist/*.whl
```
