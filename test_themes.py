import style


def test_updating_simple_style_adds_missing_entries():
    t = style.Style(a=2, b=2)

    t.update(style.Style(c=3))

    assert t.a == 2
    assert t.b == 2
    assert t.c == 3


def test_updating_simple_style_replaces_entries():
    t = style.Style(a=2, b=2)

    t.update(style.Style(a=45))

    assert t.a == 45
    assert t.b == 2


def test_updating_nested_style_adds_missing_entries():
    t = style.Style(a=style.Style(b=2, c=3))

    t.update(style.Style(a=style.Style(d=4)))

    assert t.a.b == 2
    assert t.a.c == 3
    assert t.a.d == 4


def test_updating_nested_style_replaces_entries():
    t = style.Style(a=style.Style(b=2, c=3))

    t.update(style.Style(a=style.Style(c=34)))

    assert t.a.b == 2
    assert t.a.c == 34
