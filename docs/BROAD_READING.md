# Additional attention-concentration readings

AI-assisted reading of the named primary-source sections. Empirical results are reported by the papers and were not independently reproduced.

## [One QK Channel, Many Sources: Tracing Low-Precision Attention Collapse](https://arxiv.org/html/2608.02091v2)

**Checked sections:** §§3.1–3.3, 4.2, 5.1–5.4, 6.

**Finding.** Low-precision errors injected at several sites can produce QK spectral runaway. QK-local interventions and direction-matched controls support a shared failure channel; QK-Guard activates per-head normalization after a monitored logit threshold.

**Relevance.** Connects attention saturation, QK geometry, numerical precision, and training stability to the survey's discussion of architectural interventions.

**Limits.** The tested failures are controlled low-precision training faults. The study does not establish persistent semantic-independent sink positions in all models, and a large QK norm alone is not a sufficient failure detector.

**Taxonomy.** Retained as broader concentration/stability evidence. Existing attention-sink method categories are not inferred from QK normalization alone.

## [SpecFormer: Mitigating Embedding and Attention Collapse via Spectral-Aware Transformer for Recommendation](https://arxiv.org/html/2607.24025v2)

**Checked sections:** §§II-C, IV-A–IV-C, V-D, VII.

**Finding.** SpecFormer softens input singular values, computes Q/K from softened features, and adds a learned spectral residual term for recommendation. Effective-rank measurements characterize its collapse criterion.

**Relevance.** Useful related evidence on how embedding spectra and attention-map degeneration interact, including interventions beyond language and vision models.

**Limits.** Its attention-collapse definition includes overly smoothed as well as sparse maps. Low rank is not by itself proof of a query-independent sink or low per-query entropy.

**Taxonomy.** Retained in the broad library with its own collapse definition. Spectral terminology does not automatically imply Geometric Anchoring.

## [Surgical Repair of Collapsed Attention Heads in ALiBi Transformers](https://arxiv.org/html/2603.09616v1)

**Checked sections:** §§3.1–3.4, 5.5, 6.

**Finding.** The paper diagnoses BLOOM heads with BOS mass and attention entropy, then reinitializes selected Q/K/V projections, zeroes their output projections, and trains them while masking gradients of the remaining parameters.

**Relevance.** Directly relevant to BOS concentration and post-training repair. A concrete example of model adaptation that reduces a learned attention pathology.

**Limits.** Full repair is evaluated only on BLOOM-1b7. Head-recovery thresholds are architecture-dependent, corpus effects remain confounded, and generation evaluation is limited.

**Taxonomy.** Relevant to Other Mitigation Techniques and Model Tuning; any future formal row should retain that training is required rather than describe it as a training-free edit.

## [TQL: Scaling Q-Functions with Transformers by Preventing Attention Collapse](https://arxiv.org/html/2602.01439v1)

**Checked sections:** §§4.1–4.3, 5.2–5.5, 6.

**Finding.** TQL measures increasingly concentrated attention in larger Transformer Q-functions and trains with attention-entropy losses using adaptive layer-wise and VALUE-token coefficients.

**Relevance.** Broadens the concentration discussion to reinforcement-learning value networks and provides evidence on entropy-guided training interventions.

**Limits.** The experiments concern small offline-RL critics and do not show that their concentrated tokens implement the same mechanisms as LLM sinks. Entropy regularization, modality embeddings, and policy extraction contribute to the evaluated system.

**Taxonomy.** Retained as related entropy-control evidence. The learnable entropy coefficient is not an attention-logit bias and is not a learnable sink token.

