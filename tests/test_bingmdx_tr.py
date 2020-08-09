""" test bingmdx_tr """

from light_aligner.bingmdx_tr import bingmdx_tr


def test_bingmdx_tr_sanity():
    """ test bingmdx_tr sanity. """
    assert bingmdx_tr("test")  # '试验；检测；考试；测验'
    assert "试验" in bingmdx_tr("test")


def test_bingmdx_tr_name():
    """ test bingmdx_tr sanity. """
    res = bingmdx_tr("My Name is Tom")  # '"I" 的所有格形式名称；名字；名声；名誉是汤姆；雄性动物；(特指)雄猫；Thoma s 的爱称'
    assert "名字" in res
    assert "汤姆" in res


def test_bingmdx_tr_place():
    """ test bingmdx_tr sanity. """
    res = bingmdx_tr("I live in Shanghai")
    assert "上海" in res


def test_bingmdx_tr_I():  # modify mdxdict entry
    """ test bingmdx_tr sanity. """
    res = bingmdx_tr("I live in Shanghai")
    assert "我" in res

def test_bingmdx_userdict():
    """ test bingmdx_tr sanity. """
    res = bingmdx_tr("Trump")
    assert "川普" in res
