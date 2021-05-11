# first line: 58
def light_scores(  # pylint: disable=too-many-locals, too-many-branches, too-many-statements
        text1: Union[List[str], str],
        text2: Union[List[str], str],
        pairs: Optional[int] = None,
        scale: str = "max",  # "max" "maxo" "1"
        # tol: int = 10,
        showplot: bool = True,
        saveplot: bool = True,
        # extra_dict: dict = {},  # bingmdx_tr auto userdict.txt
        extra_dict: Optional[dict] = None,  # bingmdx_tr auto userdict.txt
) -> np.ndarray:
    # fmt: on
    """
    calculate the paras similarity score matrix for given english text and chinese text

    scale: divide this scale_ per row
                'maxoverall': scale_ = matrix max, plt.contourf: levels=10
                'max': scale_ = row max, plt.contourf: vmin,vmax
                'sum': scale_ = row sum, plt.contourf: levels=10
                else: unchanged (scale_=1), plt.contourf: levels=10

    pairs: attempt to collect pairs (default=half of the number of paras) of alignments
    tol: default 10, search along the main diagnal with 2 * tol width
    """
    if extra_dict is None:
        extra_dict = {}

    logger.info("scale: **%s**", scale)

    if isinstance(text1, list):
        len1 = len(text1)
        text1 = "\n".join(elm.replace("\n", " ") for elm in text1)
    else:
        len1 = len(text1.splitlines())
    if isinstance(text2, list):
        len2 = len(text2)
        text2 = "\n".join(elm.replace("\n", " ") for elm in text2)
        # text2 = [eml.strip() for elm in text2.splitlines() if elm.strip()]
    else:
        len2 = len(text2.splitlines())

    # Path("en.txt").write_text(text1, encoding="utf-8")
    # Path("zh.txt").write_text(text2, encoding="utf-8")
    # logger.info(" en.txt zh.txt saved")

    lang1 = Detector(text1).language.code
    lang2 = Detector(text2).language.code

    if lang1 not in ["en", "zh"]:
        logger.warning(" text1 language deteced: **%s**, not English not Chinese", lang1)

    if lang2 not in ["en", "zh"]:
        logger.warning(" Text2 language deteced: **%s**, not English not Chinese", lang2)

    if lang1 == lang2:
        logger.warning(" lang1 **%s** and lang2 **%s** are the same, not sure this is what you want. ", lang1, lang2)

    def text_en_to_paras(text_en):
        text_en = re.sub(r"[^a-zA-Z\d\s—*-]+", "", text_en)

        # paras_en = [elm.strip() for elm in text_en.splitlines() if elm.strip()]

        # do not remove empty lines after processing
        # to avoid line change
        paras_en = [elm.strip() for elm in text_en.splitlines()]

        return paras_en

    def text_zh_to_paras(text_zh):
        text_zh = re.sub(r"[^一-龙\w\s—*-]+", "", text_zh)

        # paras_zh = [elm.strip() for elm in text_zh.splitlines() if elm.strip()]

        paras_zh = [elm.strip() for elm in text_zh.splitlines()]
        return paras_zh

    # process text1
    if lang1 in ["en"]:
        paras_en = text_en_to_paras(text1)
        paras_zh = text_zh_to_paras(text2)
        len_en = len1
        len_zh = len2
    else:
        paras_zh = text_zh_to_paras(text1)
        paras_en = text_en_to_paras(text2)
        len_en = len2
        len_zh = len1

    # make sure lines numbers are not altered
    assert len_en == len(paras_en)
    assert len_zh == len(paras_zh)

    row = len(paras_en)
    col = len(paras_zh)

    # set default pairs
    if pairs is None:
        pairs = min(row // 2, col // 2)

    logger.info(" Removing stopwords ...")

    # remove stopwords
    # _ = remove_stopwords(text_zh)
    # corpus = [remove_stopwords(elm).strip() for elm in paras_zh]
    corpus = []
    len_ = len(paras_zh)
    for idx, elm in enumerate(paras_zh):
        corpus.append(remove_stopwords(elm).strip())
        if not idx % 10:
            logger.info(" %s/%s ", idx + 1, len_)
        elif idx < len_ - 5:
            logger.info(" %s/%s ", idx + 1, len_)

    assert len(corpus) == len(paras_zh)

    logger.info(" Doing some processing...")

    # single char per token, [*doc] same as list(doc)
    tokenized_corpus = [[*doc] for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)

    logger.info(" Done with processing...")

    logger.info(" Gen light_scores matrix...")
    # gen correlation/score matrix
    corr_mat = []
    _ = len(paras_en)
    # for sent in tqdm(paras_en):
    for idx, sent in enumerate(paras_en):
        # sent = "Hello there good man!"
        # return the original if MDXDICT.get return None

        # tr = w4w_to_zh(sent.lower().split())
        sent_tr = bingmdx_tr(sent, extra_dict=extra_dict)

        sent_tr = remove_stopwords(sent_tr)

        # dedup: crucial
        corr = bm25.get_scores([*set("".join(sent_tr))])

        # without dedup, does not work
        # corr = bm25.get_scores([*("".join(tr))])

        corr_mat.append(corr)

        if not idx % 10:
            logger.info(" %s/%s ", idx + 1, _)
        elif idx > len(paras_en) - 4:
            logger.info(" %s/%s ", idx + 1, _)

    logger.debug(" score matrix done ")

    # scale w.r.t next max
    mat2 = np.asarray(corr_mat).copy()

    row, col = mat2.shape
    for idx, elm in enumerate(mat2):
        # if idx > 0: break
        c_row = elm.copy()
        # row_max = c_row[c_row.argmax()]
        c_row[c_row.argmax()] = 0
        # if not row_max: continue

        # mat2[idx] = mat2[idx] / row_max
        if not c_row[c_row.argmax()]:
            continue
        mat2[idx] = mat2[idx] / abs(c_row[c_row.argmax()])  # nex max

        # also divide columns: doesnt work
        # for i in range(row): mat2[idx, i] = mat2[idx, i] / row_max

    # plt.figure(22)
    # plt.contourf(mat2, levels=40, cmap="gist_heat_r")

    # import pandas as pd

    df2 = pd.DataFrame(mat2).copy()
    # procesing columns the same way
    for idx in range(col):
        idx0 = np.asarray(df2[idx]).argmax()
        # col_max = df2[idx][idx0]
        df2[idx][idx0] = 0
        idx0 = np.asarray(df2[idx]).argmax()
        col_max_next = df2[idx][idx0]
        # if not col_max: continue
        for jdx in range(row):
            if col_max_next:
                mat2[jdx, idx] = mat2[jdx, idx] / abs(col_max_next)

    scale_o = 1
    scale = str(scale)
    if scale[:4].lower() in ["maxo"]:
        scale_o = mat2.max()

    # normalize rows to 1
    # for idx in range(len(mat2)):
    # _ = """
    # no scale
    if str(scale) not in ["1"]:
        for idx, elm in enumerate(mat2):
            scale_ = scale_o
            if scale.lower() in ["sum"]:
                scale_ = mat2[idx].sum()
            elif scale.lower() in ["max"]:
                scale_ = mat2[idx].max()

            if scale_ > 0:
                mat2[idx] = mat2[idx] / scale_
    # """

    # damp values at r, c further away from
    # row, col = mat2.shape
    # r_ideal = c * col / row
    # if abs(r - r_ideal) < 3:
    # mat2[r, c] = mat2[r, c]
    # else: mat2[r, c] = mat2[r, c] / (1 + 0.02 * abs(r - r_ideal))

    # damp values further away from c_ideal
    row, col = mat2.shape
    # for idx, _ in enumerate(mat2):
    for idx in range(row):
        c_ideal = idx * col / row
        for jdx in range(col):
            if abs(jdx - c_ideal) > 3:
                mat2[idx, jdx] = mat2[idx, jdx] / (1 + 0.02 * abs(jdx - c_ideal))

    _ = """
    mat2a = mat2.copy()
    for idx in range(len(mat2a)):
        mat2a[idx] = mat2a[idx] / mat2a[idx].sum()
    plt.figure(); plt.contourf(mat2a, levels=40, cmap="gist_heat_r"); plt.colorbar()
    # """

    annot = False
    linewidths = 0
    if max(row, col) < 30:
        annot = True
        linewidths = 0.001 / max(row, col)

    # if showplot:
    if 'IPython' in sys.modules and showplot:
        import seaborn as sns
        # plt.figure()
        # plt.contourf(mat2, levels=10, cmap="gist_heat_r")
        # plt.contourf(mat2, vmin=mat2.mean(), vmax=mat2.max(), cmap="gist_heat_r")
        # plt.contourf(mat2, cmap="gist_heat_r")
        # plt.contourf(mat2, cmap="gist_heat_r", origin="upper")
        # plt.colorbar()

        plt.figure()
        ax = plt.axes()  # pylin: disable=invalid-name

        # sns.heatmap(mat2, ax=ax, cmap="gist_heat_r")
        # sns.heatmap(mat2, linewidth=1/100/mat2.shape[0])
        if str(scale) not in ["1"]:
            sns.heatmap(mat2, ax=ax, cmap="Blues", annot=annot, linewidths=linewidths, vmax=mat2.mean() + 5 * mat2.std())
        else:
            sns.heatmap(mat2, ax=ax, cmap="Blues", annot=annot, linewidths=linewidths, vmax=mat2.mean() + 5 * mat2.std())

        ax.set_title(" similarity scores for en (y-axis) vs zh (x-axis)")

        plt.show()
    # else:  # just save png and show, do not directly display
    elif saveplot:  # just save png and show
        import seaborn as sns
        if str(scale) not in ["1"]:
            snsplot = sns.heatmap(mat2, cmap="Blues", annot=annot, linewidths=linewidths, vmax=mat2.mean() + 5 * mat2.std())
        else:
            snsplot = sns.heatmap(mat2, cmap="Blues", annot=annot, linewidths=linewidths, vmax=mat2.mean() + 5 * mat2.std())
        snsplot.axes.set_title(" similarity scores for en (y-axis) vs zh (x-axis)")
        fig = snsplot.get_figure()
        fig.savefig("score-matrix.png")
        logger.info(" score matrix saved to score-matrix.png")
        if sys.platform == "win32":
            os.startfile("score-matrix.png")

    _ = """
    try:
        import pandas as pd  # pylint: disable=reimported
        # writer = pd.ExcelWriter("temp.xlsx")
        # s_df.to_excel(writer)
        # pd.DataFrame(mat2).to_excel(writer)
        # writer.save()
        color_table_applymap(mat2, file="temp.xlsx")  # commented out
        logger.info(" Saved to temp.xlsx")
    except Exception as exc:
        logger.error(exc)
        # raise
    # """

    return mat2.copy()
