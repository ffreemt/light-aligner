""" test light_scores. """

from pathlib import Path

from light_aligner.light_scores import light_scores
from light_aligner.read_text import read_text


def test_light_scores_sanity():
    """ test_light_scores_sanity. """
    # res = light_scores(["test", 'try'] * 5, ["测试", '测验'] * 6)
    res = light_scores(["test", "try"], ["测试", "测验"], showplot=False, saveplot=False,)
    assert res.size == 4


def test_wu_ch3():
    """ test wu ch3"""
    dest = r"c:\dl\Dropbox\mat-dir\myapps\data"
    path_en = Path(dest) / "wu_ch3_en.txt"
    path_zh = Path(dest) / "wu_ch3_zh.txt"

    text_en = "\n".join(
        elm.strip() for elm in read_text(path_en).splitlines() if elm.strip()
    )
    text_zh = "\n".join(
        elm.strip() for elm in read_text(path_zh).splitlines() if elm.strip()
    )

    mat2 = light_scores(text_en, text_zh, showplot=False, saveplot=False,)

    # plt.figure(26); plt.contourf(mat2, levels=40, cmap="gist_heat_r")
    # sns.heatmap(mat2, linewidth=0.01)
    # plt.show()

    assert mat2.mean() > 0.2


def test_lover_ch10():
    """ test lover ch 10"""
    # dest = r"c:\dl\Dropbox\mat-dir\myapps\data"
    dest = r"data"
    path_en = Path(dest) / "lover-ch10_en.txt"
    path_zh = Path(dest) / "lover-ch10_zh.txt"
    text_en = "\n".join(
        elm.strip() for elm in read_text(Path(path_en)).splitlines() if elm.strip()
    )
    text_zh = "\n".join(
        elm.strip() for elm in read_text(Path(path_zh)).splitlines() if elm.strip()
    )

    mat10 = light_scores(text_en, text_zh, showplot=False, saveplot=False,)

    # plt.figure(26); plt.contourf(mat2, levels=40, cmap="gist_heat_r")
    # sns.heatmap(mat10, linewidth=0.01)
    # sns.heatmap(mat2, linewidth=1/100/mat2.shape[0])
    # plt.show()

    # assert mat10.mean() > 0.15
    assert mat10.mean() > 0.05


def test_hlm_ch1():
    """ test hlm ch 1"""
    # dest = r"bumblebee-aligner\data"
    dest = r"data"
    path_en = Path(dest) / "hlm-ch1-en.txt"
    path_zh = Path(dest) / "hlm-ch1-zh.txt"
    text_en = "\n".join(
        elm.strip() for elm in read_text(Path(path_en)).splitlines() if elm.strip()
    )
    text_zh = "\n".join(
        elm.strip() for elm in read_text(Path(path_zh)).splitlines() if elm.strip()
    )

    paras_en = text_en.splitlines()
    paras_zh = text_zh.splitlines()

    mat_hlm = light_scores(text_en, text_zh, showplot=False, saveplot=False,)

    # plt.figure(26); plt.contourf(mat2, levels=40, cmap="gist_heat_r")

    # plt.imshow(mat2, origin="lower", cmap='PuOr', interpolation='lanczos')  # not too good

    # sns.heatmap(mat2, vmin=0.89, cmap='viridis_r')
    # linewidth=0.01

    # sns.heatmap(mat2, cmap="binary", vmin=0.99)


def test_00test():
    """ test 00test"""
    dest = r"data"
    path_en = Path(dest) / "0test_en.txt"
    path_zh = Path(dest) / "0test_zh.txt"

    text_en = "\n".join(
        elm.strip() for elm in read_text(path_en).splitlines() if elm.strip()
    )
    text_zh = "\n".join(
        elm.strip() for elm in read_text(path_zh).splitlines() if elm.strip()
    )

    mat2 = light_scores(text_en, text_zh, showplot=False, saveplot=False,)

    # plt.figure(26); plt.contourf(mat2, levels=40, cmap="gist_heat_r")
    # sns.heatmap(mat2, linewidth=0.01)
    # plt.show()

    assert mat2.mean() > 0.2


"""
corr_mat = np.asarray(mat2).copy()
count = 0
r_len, c_len = mat2.shape

count += 1
print(" count: ", count)
r, c = divmod(np.argmax(corr_mat), c_len)
if abs(r * c_len/r_len - c) < 10:
    # print(paras_en[r],"\n", corpus[c])
    print(paras_en[r],"\n", paras_zh[c])
    print(r, c, count)
    for idx in range(c_len):
        corr_mat[r][idx] = 0
    for idx in range(r_len):
        corr_mat[idx][c] = 0
    plt.figure(5); plt.contourf(np.asarray(corr_mat), levels=20, cmap="gist_heat_r")
else:
    corr_mat[r][c] = 0
print(r, c, count)

plt.figure(); plt.contourf(corr_mat, levels=40, cmap="gist_heat_r")
"""
