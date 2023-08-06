import attr
import pytest
def test_attrs_decorator(uncached):
    from tests.samples import attrs0

    @attrs0.cls
    class TestAttrs:
        pass

    assert attr.has(TestAttrs)

def test_getattribute_attribute_exists(uncached):
    from tests.samples import attrs1
    assert attrs1.test == 1

def test_getattribute_attribute_not_exists(uncached):
    with pytest.raises(AttributeError):
        from tests.samples import attrs2