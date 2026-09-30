# Source record — *Deep Learning* (Goodfellow, Bengio & Courville, 2016)

## Identification

| Field | Value |
| --- | --- |
| Work | *Deep Learning*, Ian Goodfellow, Yoshua Bengio, Aaron Courville, MIT Press, © 2016 |
| Local copy | **Simplified Chinese translation** — 《深度学习》, 人民邮电出版社 (Posts & Telecom Press), 2017 年 8 月第 1 版 / 2017 年 8 月北京第 1 次印刷 |
| Translators | 赵申剑, 黎彧君, 符天凡, 李凯; 审校 张志华 等; 责任编辑 王峰松 |
| File name (as stored) | `TensorFlow深度学习 (Glancarlo Z_ (Z-Library)(5).pdf` |
| Location | `D:\.Myfile\D1s1\学习路径方向\书\` (workspace book folder, next to the Trustworthy ML source) |
| Size / SHA-256 | 41,069,554 bytes / `27b58737d3e81627ef4387b5d40d7a8fd0767a7b7efe5794232350c9bed69bd1` |
| Container | PDF 1.4, produced by `calibre 3.1.1`, container creation date 2019-06-07 |
| Extent | 868 PDF pages; embedded outline with 363 entries; full body + 参考文献 + 索引 |

**File-name warning.** The stored file name is a mislabel from the original download (it names a
different book). The file was identified by its embedded metadata — `title = 深度学习`,
`author = [美]Ian Goodfellow … [加]Aaron Courville … [加]Yoshua Bengio` — and by the copyright page
(PDF p. 3), which names *Deep Learning* © 2016 MIT Press and the 2017 Posts & Telecom Press
Simplified Chinese translation. No other copy of the book exists in this workspace; nothing was
downloaded for this package.

## Pagination convention

This electronic copy carries **no printed folio numbers**: the publisher's page numbers were dropped
in the e-book conversion, and the front-matter fields 印张 / 字数 / 定价 / ISBN are blank. There is
therefore no printed page number to cite and no fixed PDF↔print offset.

Citations in this package use:

1. **Section number as the primary locator** — e.g. `(§8.2.4)`. Section numbering is identical in the
   Chinese translation and the English original, so these citations remain resolvable in either
   edition.
2. **PDF page number of this file as the secondary locator** — e.g. `(§8.2.4, p. 310)`, where `p. 310`
   means the 310th page of *this file*, 1-based. It is not a printed page of any physical edition and
   must not be quoted as one.

Structural map of this file (1-based PDF pages):

| Range | Content |
| --- | --- |
| 1–36 | front matter: 书名页/版权页 (2–4), 中文版推荐语 (5–6), 译者序 (7–9), 中文版致谢 (10–12), 英文原书致谢 (13–14), 数学符号 (15–18), 目录 (19–36) |
| 37–61 | 第 1 章 引言 |
| 62–84 | 第 2 章 线性代数 |
| 85–111 | 第 3 章 概率与信息论 |
| 112–129 | 第 4 章 数值计算 |
| 130–190 | 第 5 章 机器学习基础 |
| 191–251 | 第 6 章 深度前馈网络 |
| 252–296 | 第 7 章 深度学习中的正则化 |
| 297–349 | 第 8 章 深度模型中的优化 |
| 350–390 | 第 9 章 卷积网络 |
| 391–435 | 第 10 章 序列建模：循环和递归网络 |
| 436–454 | 第 11 章 实践方法论 |
| 455–496 | 第 12 章 应用 |
| 497–509 | 第 13 章 线性因子模型 |
| 510–531 | 第 14 章 自编码器 |
| 532–558 | 第 15 章 表示学习 |
| 559–590 | 第 16 章 结构化概率模型 |
| 591–604 | 第 17 章 蒙特卡罗方法 |
| 605–631 | 第 18 章 直面配分函数 |
| 632–653 | 第 19 章 近似推断 |
| 654–718 | 第 20 章 深度生成模型 |
| 719–806 | 参考文献 |
| 807–868 | 索引 |

Part boundaries: 第 1 部分 应用数学与机器学习基础 (from p. 62), 第 2 部分 深度网络：现代实践
(from p. 191), 第 3 部分 深度学习研究 (from p. 495).

## Reading and extraction method

Text was extracted with PyMuPDF 1.27 from the local file, chapter by chapter, into a scratch
directory outside the repository (`D:\tmp\dl2016\body\ch01.txt` … `ch20.txt`), with every page
prefixed by a `[[pN]]` marker so each note can be checked against the locator convention above. A
section→PDF-page map derived from the embedded outline is kept at `D:\tmp\dl2016\sections.tsv`.

**Display equations are images, not text.** The text layer carries running prose, section headings,
figure and table captions, inline symbols and equation *numbers* ("如式（7.43）"), but the display
equations themselves were rasterized during conversion. Verified by image count per page: p. 275
carries 7 images and p. 276 carries 13 (both inside the §7.8 early-stopping ↔ L2 derivation), while
p. 442 (§11.4.1, no display math) carries 0. Consequences for this package:

- Formula-level detail (exact coefficients, exact algebraic conditions) is **not** recoverable from
  extracted text and is never cited here as if it were. Where a formula matters, the citation is to the
  surrounding prose, which states the relationship in words, or the page is rendered as an image and
  read directly.
- Some tables and figures survive only as captions plus partially extracted cell text (Table 11.1 and
  the Algorithm 5.1 / 7.1 / 7.2 / 7.3 blocks did extract as text and are usable).
- Any claim in this package that would require an unextracted formula is marked as prose-level.

Per plan, neither the PDF nor the bulk extracted text is committed. The scratch files are working
material for the notes in `concept_reconstruction.md` and for the source lines of the SOPs and BCs.

## Boundaries that follow from using this copy

- **Language.** Everything read here is the Chinese translation. This package therefore contains no
  verbatim English quotation from the book: any wording shown in an artifact is either a
  translation/paraphrase of the Chinese text or a term that the translation prints in English (model
  and method names such as Dropout, Adam, batch normalization, and citation keys such as
  `Srivastava et al., 2014`). Quoted-looking phrases are marked as translated. Section numbers and
  proper nouns were spot-checked against the translation's own usage.
- **Non-book front matter.** 中文版推荐语, 译者序 and 中文版致谢 (pp. 5–12) are Chinese-edition
  apparatus written by others. They are not evidence of the authors' claims and are never cited as
  such.
- **Historical boundary.** The translation renders the 2016 English first edition; there is no later
  edition of the original. Everything in this package is bounded by 2016 knowledge: empirical
  examples, benchmark scores, framework and hardware details are book-era and are marked historical
  where they appear. Material that post-dates the book (Transformers, AdamW, scaling laws, current
  leaderboards) is deliberately absent and belongs to a future source-update cycle.
- **Terminology drift.** Some 2016-vintage Chinese renderings differ from today's common usage; where
  an artifact needs the English term it uses the term the book itself prints or the standard English
  name of the method, not a modernized re-labelling of the concept.
