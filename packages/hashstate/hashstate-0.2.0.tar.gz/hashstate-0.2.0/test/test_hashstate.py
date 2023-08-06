import hashstate
import pytest

ALGS = {'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'}


@pytest.mark.parametrize('alg', ALGS)
def test_serialization(alg):
    ctor = getattr(hashstate, alg)
    h1 = ctor()
    h2 = ctor()
    assert h1.serialize() == h2.serialize()
    h1.update(b'abc')
    h2.update(b'abc')
    assert h1.serialize() == h2.serialize()

    h1.update(b'hello')
    assert h1.serialize() != h2.serialize()

    assert h2.deserialize(h1.serialize()) is None
    assert h1.digest() == h2.digest()

    h1.update(b'foo')
    h2.update(b'foo')
    assert h1.digest() == h2.digest()


def test_bad_deserialization_type():
    with pytest.raises(TypeError) as e:
        hashstate.sha1().deserialize(1234)
    assert 'Invalid state, must be a bytes object' == str(e.value)


def test_bad_deserialize_length():
    with pytest.raises(ValueError) as e:
        hashstate.sha512().deserialize(b'foo')
    assert 'Invalid state length' == str(e.value)
