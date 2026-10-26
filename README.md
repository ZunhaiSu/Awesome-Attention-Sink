<h1 align="center">🚀 Attention Sink in Transformers: <br> A Survey on Utilization, Interpretation, and Mitigation</h1>

<div align="center">

[![PDF](https://img.shields.io/badge/PDF-Download-red?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](https://arxiv.org/pdf/2604.10098)
[![Status](https://img.shields.io/badge/STATUS-Active-brightgreen?style=for-the-badge)]()
[![arXiv](https://img.shields.io/badge/arXiv-2604.10098-b31b1b?style=for-the-badge)](https://arxiv.org/abs/2604.10098)

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/ZunhaiSu/Awesome-Attention-Sink?style=social)](https://github.com/ZunhaiSu/Awesome-Attention-Sink/stargazers)

</div>

<div align="center">
  ⭐ If you find this repository helpful, please consider giving it a star.
</div>

---

## 📚 Table of Contents

- [Latest News](#-latest-news)
- [Overview](#-overview)
- [Paper List](#-paper-list)
- [Citation](#-citation)
- [Contact](#-contact)

---

## 🔥 Latest News

- **[2026-10-26]** The Feishu export has been migrated into a versioned catalog of **208 records**. Browse the [paper catalog](docs/CATALOG.md), download the [CSV](exports/papers.csv), or inspect the [data and provenance](docs/MIGRATION.md). Original labels and date precision are preserved.
- **[2026-06-05]** 📊 **Paper list migrated!** The surveyed paper list has been migrated to an online spreadsheet for easier querying and continuous updates. Access it here: [AS Paper List](https://bcn7isxnv9g2.feishu.cn/wiki/TWcVw0TmIi9F1ZkyZ3ac3z6onYe)
- **[2026-06-05]** 📚 **Update!** New version released with **50+ new papers** added. Thanks for all the feedback! In addition, due to the growing number of works on Attention Sink in DiTs, a dedicated **subsection** has been introduced. Further feedback and discussion are always welcome.
- **[2026-04-14]** ✨ We thank all related works for their contributions to AS-related research. We are currently fine-tuning the paper for journal submission. For any inquiries or to include your work in the paper list, please contact us at [zh-su23@mails.tsinghua.edu.cn](mailto:zh-su23@mails.tsinghua.edu.cn).
- **[2026-04-14]** 🎉 Our survey paper *"Attention Sink in Transformers: A Survey on Utilization, Interpretation, and Mitigation"* is now available on arXiv! [[Link](https://arxiv.org/abs/2604.10098)]
- **[2026-04-11]** 🚀 Repository launched to track the latest progress in Attention Sink research.

---

## 📖 Overview

This repository organizes research on **Attention Sink (AS)**: recurring attention concentration on a small set of positions. The survey examines how models use these positions, what computations they support, and how architectural or training changes can alter dependence on them.

<div align="center">
  <img src="Figures/paper_overview.png" alt="Survey Framework" width="95%">
  <br>
  <em>Figure 1: Overview of the survey structure.</em>
</div>

<br>

The survey organizes the literature around three complementary research objectives and examines them across Transformer architectures. A study may address several objectives. The figures summarize the survey; they are not recomputed statistics of the live catalog.

<div align="center">
  <img src="Figures/num_research.png" alt="Research Trends" width="80%">
  <br>
  <em>Figure 2: Cumulative publication count and temporal trends in AS research (2023–2026).</em>
</div>

<br>

### Three Research Objectives

**① Fundamental Utilization**
> Empirical exploitation of AS and management of its immediate effects.
> *Approaches include:* Sink Token Preservation, Attention Redistribution, Learnable Prefix Tokens, Sink Token Repurposing.

**② Mechanistic Interpretation**
> Investigation of underlying causes and architectural factors.
> *Theories include:* Softmax Limitations and No-Op Theory, Outlier Circuits, Implicit Attention Bias, Geometric Anchoring, Other Mechanistic Interpretations.

**③ Strategic Mitigation**
> Direct structural mitigation for training stability and deployment robustness.
> *Strategies include:* Gated Attention Mechanisms, Modified Softmax Functions, Learnable Attention Bias, Pre-training Interventions, Other Mitigation Techniques.

---

## 📑 Paper List

The formal catalog contains **208 migrated records**. It preserves three independent method dimensions—**Fundamental Utilization**, **Mechanistic Interpretation**, and **Strategic Mitigation**—alongside architecture and application labels. Labels can overlap.

- [Browse the catalog](docs/CATALOG.md)
- [Download CSV](exports/papers.csv) or [read canonical JSON](data/papers.json)
- [Classification names and legacy mappings](data/taxonomy.json)
- [Source preservation and migration checks](docs/MIGRATION.md)
- [Contribute a paper or correction](CONTRIBUTING.md)
- [Feishu collection and review table](https://bcn7isxnv9g2.feishu.cn/wiki/TWcVw0TmIi9F1ZkyZ3ac3z6onYe)

Publication labels are inherited from the supplied export and marked as not independently reverified. Updates to this online resource do not silently change the literature coverage of a manuscript version.

If you identify any errors or omissions in the list of Attention-Sink-related papers, please contact zh-su23@mails.tsinghua.edu.cn. We greatly appreciate your contributions and feedback.

## 🌟 Citation

If you find this survey or repository useful for your research, please cite:

```bibtex
@article{su2026attention,
  title={Attention Sink in Transformers: A Survey on Utilization, Interpretation, and Mitigation},
  author={Su, Zunhai and Zhang, Hengyuan and Wu, Wei and Zhang, Yifan and Liu, Yaxiu and Xiao, He and Yang, Qingyao and Sun, Yuxuan and Yang, Rui and Zhang, Chao and others},
  journal={arXiv preprint arXiv:2604.10098},
  year={2026}
}
```

## 📧 Contact

Feel free to open an issue or contact us if you have any questions or want to include your work in this list.

Corresponding Author: Zunhai Su (zh-su23@mails.tsinghua.edu.cn)
