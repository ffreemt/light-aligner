# Light-Aligner
<!-- based on README.txt in myapps\dlb_aligner -->
<!---![This image won't be a figure](manual/tmx_docx_icon.png){width=50%}-->

* Version 0.1.1 (2020.08.15)

清凉版命令行对齐工具（目前仅支持英中）

## 特点

* 轻量
* 快速
* 无需联网
* 无需机器翻译辅助
* 可添加定制字典提高对齐质量

## 功能

* 输入两个`txt`文件，输出段段对齐、句句对齐的`xlsx`

* 输入含中英两种语言的单一`txt` 文件（段段或几段对一段，可带只有单一语言的前言或后语等等），例如sample-data目录里的 `Gatsby-200lines-dual.txt`

## 特别包安装
`light aligner` 用了 `polyglot`, 而 `polyglot` 依赖 `libicu`

安装`libicu`
###### Linux/OSX

例如
* Ubuntu: `sudo apt install libicu-dev`
* Centos: `yum install libicu`
* OSX: `brew install icu4c`

然后在用 `poetry` 或 `pip` 安装 ` PyICU pycld2 Morfessor`, 例如
```
poetry add PyICU pycld2 Morfessor
```
或
```
pip install PyICU pycld2 Morfessor
```
###### Windows
从 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu 和 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2 (可能需要 Morfessor https://www.lfd.uci.edu/~gohlke/pythonlibs/)
下载安装对应的 `pyicu` 和 `pycld2` (以及可能 `Morfessor`) whl 包。安装`whl`的命令为
``` pip install file.whl ```

### 安装
```pip install light-aligner```

或从`github`拉项目用 `pip`安装:
```
git clone git@github.com:ffreemt/light-aligner.git
cd light-aigner
pip install -r requirements.txt
```
或从`github`拉项目用 `poetry`安装:
```
git clone git@github.com:ffreemt/light-aligner.git
cd light-aigner
poetry install -v
```

`light aligner` 也可以装在`Linux/OSX`里. 项目在 `github`的成功构造 (题头的 github workflow 徽章 ![build](https://github.com/ffreemt/light-aligner/workflows/build/badge.svg)显示的事实）其实是在Linux里完成的.


## 使用
* 启动终端（例如`cmd`， `powershell`，`conemu`等等。如果不想用conemu、cmder等第三方程序，建议用Windows自带的 `powershell`）

* 换到含该文件的目录里。例如 `cd path-to-light-aligner`

* 运行<br/>
`
python -m light_aligner
`
  * 帮助文档<br/>
`
python -m light_aligner --shorthelp
`

* 当前目录里或系统包（路径为`light_aligner\userdict.txt`）里可添加用户定制字典文件 `userdict.txt` 提高对齐质量。`userdict.txt`的格式
<center>
<table>
   <tbody>
<tr><td>i:   我<br/>
I:   我<br/>
you:  你<br/>
Trump:  川普<br/>
xxx: <br/>
Chen:  甄士隐<br/>
Shih-yin:  甄士隐</td></tr>
   </tbody>
</table>
</center>
请注意英文以单词而不是以词组为单位，**Chen Shih-yin: 甄士隐** 是不起作用的。但**Chen: 甄** 和 **Chen: 甄士隐** 的效果则差不多。

`userdict.txt`里的冒号也可以用TAB代替。因此可以从 `xlsx` 文件导出`tsv`文件作为 `userdict.txt`。


## 建议和反馈

* mu@qq41947782/交流释疑qq群 316287378 [https://jq.qq.com/?_wv=1027&k=5e7BThu](https://jq.qq.com/?_wv=1027&k=5e7BThu)
