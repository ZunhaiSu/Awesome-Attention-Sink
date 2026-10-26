# Broad attention-sink and attention-concentration library

**2,258 bibliographic records**, including the unchanged 232-record classified subset and 2,026 additional records. The user-expanded scope includes papers citing StreamingLLM and related attention-concentration work. A title/abstract does not need to contain the exact phrase attention sink.

[Download the complete library CSV](../exports/library.csv) · [Source snapshot and exact queries](../data/library/broad-2026-10-26.json) · [Additional source readings](BROAD_READING.md) · [Original classification subset](CATALOG.md)

## Inclusion evidence

- `seed_citation_index`: OpenAlex indexes a citation edge to StreamingLLM. The index can miss or mismatch references.
- `seed_title_fulltext_index`: an exact-title full-text index query matched the seed title. This is a discovery signal and is not described as a checked citation.
- `citation_in_primary_reference_list`: the seed title or arXiv ID was found in the linked primary paper’s bibliography, with a locator and source hash.
- `attention_concentration_keywords`: arXiv title/abstract retrieval covers concentration, attention/entropy collapse, saturation, and attention entropy. Scientific relevance may still need reading.
- Prior sink/register leads and the previously contextual RATS paper remain available in this broader collection.

## Search completeness and reading depth

All pages returned by the documented queries were retrieved. The source queries yielded 54 citation-edge records and 1,971 exact-title full-text hits in OpenAlex (2,009 unique OpenAlex IDs), plus 198 arXiv concentration records. Identifier/title deduplication and reconciliation with the prior catalog produce the library total above. These are bibliographic records; publication versions without a shared identifier or title may remain separate.

The 60 newest arXiv-linked discovery records were checked for the seed reference: 57 bibliographies confirmed it; 3 HTML versions were unavailable. This convenience batch is not a representative sample. The remaining index hits are not claimed to have been read or citation-verified.

Twenty-eight records have specified key-section checks (24 from the prior update and 4 new concentration readings), and one has a contextual key-section reading. The original 208 classifications remain inherited. Reading a reference list alone does not verify a method classification.

Coverage remains limited by index updates, unavailable full texts, vocabulary, and unresolved publication versions. A citation can be background-only; it does not by itself establish direct sink research. Low-rank/smoothed attention and low per-query entropy also require different interpretations.

The fourteen method categories and nine application names remain intact. Unread or broader related records can have empty method labels. The broad library is a collection of potential resources for the survey, and inclusion does not automatically add a claim or citation to a frozen manuscript.

Primary index documentation: [OpenAlex citations](https://help.openalex.org/data/works/citations/) and [paging](https://help.openalex.org/api/paging/). The seed is [Efficient Streaming Language Models with Attention Sinks](https://arxiv.org/abs/2309.17453).

## Latest 100 records

The complete collection is in the CSV above. Dates below preserve their source basis; an indexed publication date is not necessarily first arXiv submission.

| Paper | Date | Reading status | Relation evidence |
|---|---|---|---|
| [Mixing Matters: Evidence Position Bias Across Sequence Mixers in Long-Context Question Answering](https://arxiv.org/abs/2610.31135) | 2026-10-22 | metadata_only | attention_concentration_keywords |
| [Attention with a Calibrated Off Switch: Causal FIR Key Smoothing, the Score-Shift Pathology, and Selective Silence in Rectified Attention (pn_fir_tau)](https://doi.org/10.21203/rs.3.rs-11435949/v1) | 2026-10-21 | index_metadata_only | seed_title_fulltext_index |
| [Multimodal Audiovisual Learning via Gated Spiking Cross-Attention](https://doi.org/10.21203/rs.3.rs-10733322/v1) | 2026-10-21 | index_metadata_only | seed_title_fulltext_index |
| [HiddenLens: A Multi-Layer LLM Framework for Detecting and Resolving Hidden Assumptions in Software Requirements](https://arxiv.org/abs/2610.29996) | 2026-10-21 | metadata_only | attention_concentration_keywords |
| [SAKURA: Serving Attention Key-Value State Under Rate Adaptation for Private Image Editing on Phones](https://arxiv.org/abs/2610.29733) | 2026-10-21 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Memory-Centric Continual Learning for AI Agents](https://arxiv.org/abs/2610.29357) | 2026-10-21 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Resuming Vision-Language Inference across Onboard Interruptions](https://arxiv.org/abs/2610.29183) | 2026-10-21 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Cache Engineering for Agents](https://arxiv.org/abs/2610.28577) | 2026-10-20 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [RACE: RoPE-Aligned Attention Compression Based on Query-Key Activation Energies](https://arxiv.org/abs/2610.28385) | 2026-10-20 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Offline Makes Online Better: Calibrated Cache Compression for Video Generation](https://arxiv.org/abs/2610.28192) | 2026-10-20 | index_metadata_only | seed_title_fulltext_index |
| [Anatomical Review of TOKENGATE: Adapting LLMs for Fast and Memory-Efficient Prefill with Learned Token Pruning](https://arxiv.org/abs/2610.26754) | 2026-10-19 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [The KV-Surgeon: Compensation-Aware Offline KV-Cache Compaction](https://arxiv.org/abs/2610.25933) | 2026-10-19 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Remember Less, Adapt Longer: Bounded-State In-Context Reinforcement Learning with Recurrent Summary Memory](https://arxiv.org/abs/2610.25758) | 2026-10-19 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Frechet Forcing: Training Long-Horizon Streaming World Models from Short Clips](https://arxiv.org/abs/2610.25666) | 2026-10-19 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [DeepD enables efficient genome modeling and controllable long-context sequence generation across domains of life](https://doi.org/10.64898/2026.10.13.758170) | 2026-10-18 | index_metadata_only | seed_title_fulltext_index |
| [MOSAIC: Multi-Objective Search for Allocating Inference Cache Across LLM Decoder Layers](https://arxiv.org/abs/2610.25431) | 2026-10-18 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Improving the Expressive Power of Hybrid Sequence Models via Multi-Hop Retrieval](https://arxiv.org/abs/2610.25250) | 2026-10-18 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Certified Sparse Attention via Perturbed Retrieval](https://arxiv.org/abs/2610.24991) | 2026-10-18 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [TideKV: Delayed KV eviction via layer-wise chunked prefill for memory-efficient long-context LLM inference](https://arxiv.org/abs/2610.24499) | 2026-10-17 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [A Conditional No-Hair Theorem for Transformers: How Language Models Forget Their Prompt](https://arxiv.org/abs/2610.24133) | 2026-10-16 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Cache2LoRA: Understanding and Improving Context Internalization](https://arxiv.org/abs/2610.24107) | 2026-10-16 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Dynamical Kernel Attention: Estimating the Present from a Record of the Past](https://arxiv.org/abs/2610.24026) | 2026-10-16 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [CoTA++: Understanding the Repeat Curse in dMLLMs from an Information Flow Perspective](https://arxiv.org/abs/2610.23290) | 2026-10-16 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [What LLMs Do in the Shadows: Reading Context Reliance from the Unembedding Dark Space](https://arxiv.org/abs/2610.23182) | 2026-10-16 | metadata_only | prior_sink_keyword_discovery |
| [Sink-Sparse Hybrid Attention for Efficient Inference in T2I/T2V Diffusion Transformers](https://arxiv.org/abs/2610.22975) | 2026-10-16 | key_sections_checked | prior_classified_catalog |
| [Understanding KV Residency in Production-Scale Agentic LLM Workloads](https://arxiv.org/abs/2610.22863) | 2026-10-16 | index_metadata_only | seed_title_fulltext_index |
| [ProV-Mem: Proactive Memory for Streaming Video Question Answering](https://arxiv.org/abs/2610.23998) | 2026-10-15 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [First Passage Attention](https://arxiv.org/abs/2610.22714) | 2026-10-15 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Where Prefill Expert Reduction Hurts MoE Models: A Few Prompt Tokens Carry Most of the Short-Answer F1 Loss](https://arxiv.org/abs/2610.22454) | 2026-10-15 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Attention over noisy examples: generalization and memorization in the exponential Hopfield network](https://arxiv.org/abs/2610.22191) | 2026-10-15 | metadata_only | attention_concentration_keywords |
| [REKI: Registering Knowledge in VLAs](https://arxiv.org/abs/2610.22178) | 2026-10-15 | metadata_only | prior_related_discovery |
| [DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction](https://arxiv.org/abs/2610.22130) | 2026-10-15 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Augment the Cache, Replace the Activation: A 2x2 Study of Internal-State Sharing](https://arxiv.org/abs/2610.22026) | 2026-10-15 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [FlashAttention with Statistics: Low-Overhead Attention Features for Compact Hallucination Detectors](https://arxiv.org/abs/2610.21483) | 2026-10-15 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Calibration Language Shapes Block-Influence Pruning in Multilingual Language Models](https://arxiv.org/abs/2610.21383) | 2026-10-15 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [From Long Context to Selective Memory:A Survey of Memory-Centric Compression for Large Language Models](https://arxiv.org/abs/2610.21165) | 2026-10-15 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Sparse Attention for Video Generation Acceleration via Growing Sparsity and Reduced Search](https://arxiv.org/abs/2610.21129) | 2026-10-15 | metadata_only | attention_concentration_keywords |
| [Long-Context Drafting Does Not Require Long-Context Drafters](https://arxiv.org/abs/2610.20865) | 2026-10-14 | index_metadata_only | seed_title_fulltext_index |
| [RoLaQ: Joint Rotation and Range Calibration for 2-Bit KV Caches in Multi-Head Latent Attention](https://arxiv.org/abs/2610.20686) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Latent Compaction with Test-Time Training](https://arxiv.org/abs/2610.20582) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [FOLD: Position-Free Far Memory with Local Order for Long-Context Speculative Decoding](https://arxiv.org/abs/2610.20392) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [StreamErase: Towards Ultra-Fast Streaming Video Erasing](https://arxiv.org/abs/2610.20137) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; prior_sink_keyword_discovery; citation_in_primary_reference_list |
| [JointServe: Serving Multi-Model Agents on Memory-Constrained GPUs](https://arxiv.org/abs/2610.19822) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference](https://arxiv.org/abs/2610.19605) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Speaking Longer Than Learned: Training-Free Long-Form Generation for Full-Stream Text-to-Speech](https://arxiv.org/abs/2610.19553) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [WinARDet: Compressed Window Auto-Regression for Long-Horizon Vision-Language Grounding](https://arxiv.org/abs/2610.19419) | 2026-10-14 | metadata_only | prior_sink_keyword_discovery |
| [Evaluating Compressed Memory: Dependence, Utility, and Content Benefit](https://arxiv.org/abs/2610.19373) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Asymptotic Behavior of Transformers](https://arxiv.org/abs/2610.19358) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [SonoWorld: Towards Interactive Pose-Controllable Ultrasound World Models](https://arxiv.org/abs/2610.19327) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Why don't Graph Transformers attend to the same token?](https://arxiv.org/abs/2610.19324) | 2026-10-14 | reference_list_checked | seed_title_fulltext_index; attention_concentration_keywords; prior_sink_keyword_discovery; citation_in_primary_reference_list |
| [FrameScout: Scouting Query-Relevant Frames for Long Video Understanding](https://arxiv.org/abs/2610.23975) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [CacheSmith: Accurate RAG Serving under Latency SLOs with Adaptive KV Reuse](https://arxiv.org/abs/2610.18925) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Kwai Summary Attention V2 Technical Report](https://arxiv.org/abs/2610.18654) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [MultiAlloc: Budget-Aware Precision Allocation for KV Cache Quantization](https://arxiv.org/abs/2610.18642) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Not All Drift Is a Mechanism: Tracing Prompt Adaptation in LLMs](https://arxiv.org/abs/2610.18412) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Bifocal: Training-Free Mixed Granularity Visual Token Pruning for Multimodal LLMs](https://arxiv.org/abs/2610.18399) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [SparPR: Runtime KV-Cache Recovery for Resource-Constrained LLM Inference on Consumer Hardware](https://arxiv.org/abs/2610.18140) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [ChampionKV: Head-Wise Adaptive Budget Allocation for KV Cache Compression](https://arxiv.org/abs/2610.18026) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; attention_concentration_keywords; citation_in_primary_reference_list |
| [Neural Dimensional Analysis: Foundations of Dimensionless and Scale-Consistent Computation](https://arxiv.org/abs/2610.17969) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Prefilling-dLLM v2: Learned Chunk Routing for Long-Context Diffusion Language Models](https://arxiv.org/abs/2610.17868) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [TwinPrune: Density-Aware Two-Phase Token Pruning for Vision-Language Models](https://arxiv.org/abs/2610.17530) | 2026-10-13 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Speculative Decoding Shortcuts Can Undermine Language Model Safety Guarantees](https://doi.org/10.21203/rs.3.rs-10796407/v1) | 2026-10-12 | index_metadata_only | seed_title_fulltext_index |
| [Efficient Long-Context Reasoning in Large Language Models: Hierarchical Token Compression with Sparse Attention and Dynamic Memory Management](https://doi.org/10.21203/rs.3.rs-11124879/v1) | 2026-10-12 | index_metadata_only | seed_title_fulltext_index |
| [WIRE: Weight Space Implicit Representation Encoding of Frozen Video LLMs](https://arxiv.org/abs/2610.17355) | 2026-10-12 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [FreeSolo: Linear-time Sparse Attention with Zero-Shot Length Extrapolation](https://arxiv.org/abs/2610.17191) | 2026-10-12 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [FORGE: Procedural Weight Generation for Sparse MoE Inference](https://arxiv.org/abs/2610.16890) | 2026-10-12 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Before Attention Sinks Form: Hidden-State Geometry Reveals and Modulates Their Formation](https://arxiv.org/abs/2610.16745) | 2026-10-12 | key_sections_checked | prior_classified_catalog; seed_title_fulltext_index; citation_in_primary_reference_list |
| [FoveaTree: Information-Density Trees for Query-Guided Visual Token Pruning in Video Large Language Models](https://arxiv.org/abs/2610.16744) | 2026-10-12 | metadata_only | prior_sink_keyword_discovery |
| [RIFT: Token Influence Follows the Path of Least Resistance](https://arxiv.org/abs/2610.16349) | 2026-10-12 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Softmax-Free Attention in Spiking Transformers as the Zero-Temperature Limit of Two-Level Systems](https://arxiv.org/abs/2610.15968) | 2026-10-11 | metadata_only | attention_concentration_keywords |
| [Attention Sinks in VLMs Are Borrowed, Not Seen](https://arxiv.org/abs/2610.15855) | 2026-10-11 | key_sections_checked | prior_classified_catalog; seed_title_fulltext_index; citation_in_primary_reference_list |
| [Sori: Streamable and Controllable Model for Non-musical Audio to Symbolic Music Transformation](https://arxiv.org/abs/2610.15474) | 2026-10-11 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [E8 Lattice Key Quantization for Low-Bit KV-Cache Compression](https://arxiv.org/abs/2610.15384) | 2026-10-11 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [Enterprise Latency Optimization, Streaming Infrastructure, and Retrieval-Augmented Generation Architectures: Research Innovations in Enterprise Conversational AI Performance](https://ijisae.org/index.php/IJISAE/article/view/8571) | 2026-10-10 | index_metadata_only | seed_title_fulltext_index |
| [SAFE-KV: Causal Suffix Repair for Behavior-Preserving Non-Prefix KV Cache Reuse in RAG](https://arxiv.org/abs/2610.15186) | 2026-10-10 | index_metadata_only | seed_title_fulltext_index |
| [MORE: Learning Motion-Oriented Registers for Driving World Models and Planning](https://arxiv.org/abs/2610.14871) | 2026-10-10 | metadata_only | prior_related_discovery |
| [Align-VAE: Aligning Attention and Geometry in VecSet VAEs for 3D Reconstruction](https://arxiv.org/abs/2610.14734) | 2026-10-10 | metadata_only | prior_sink_keyword_discovery |
| [Accelerating Cross-Model LLM Inference via Attention Map Reuse](https://arxiv.org/abs/2610.14688) | 2026-10-10 | index_metadata_only | seed_title_fulltext_index |
| [Vesta: Queueing-Aware LLM Scheduling for Real-World Workloads](https://arxiv.org/abs/2610.14686) | 2026-10-10 | reference_list_checked | seed_title_fulltext_index; citation_in_primary_reference_list |
| [FrameFold: Response-Guided KV Cache Consolidation for Autoregressive Long Video Generation](https://arxiv.org/abs/2610.14568) | 2026-10-10 | index_metadata_only | seed_title_fulltext_index |
| [KV4-RL: Unlocking Faster Asynchronous Rollouts for RLVR with INT4 KV Cache Quantization](https://arxiv.org/abs/2610.14448) | 2026-10-10 | reference_list_checked | seed_title_fulltext_index; prior_sink_keyword_discovery; citation_in_primary_reference_list |
| [C$^2$LUE: Clinically Aligned Patient-Level Ultrasound Diagnosis via Evidence-Aware Multi-Instance Learning](https://arxiv.org/abs/2610.14143) | 2026-10-09 | metadata_only | attention_concentration_keywords |
| [SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices](https://arxiv.org/abs/2610.13740) | 2026-10-09 | index_metadata_only | seed_title_fulltext_index; prior_sink_keyword_discovery |
| [Not All Dimensions Are Equal: Outlier-Aware Attention Linearization with Grouped Quadratic Kernels](https://arxiv.org/abs/2610.13674) | 2026-10-09 | index_metadata_only | seed_title_fulltext_index |
| [Exploring Attention Sinks in Text-to-Image Transformers from Diffusion and Autoregressive Models](https://arxiv.org/abs/2610.13337) | 2026-10-09 | index_metadata_only | seed_title_fulltext_index; prior_sink_keyword_discovery |
| [Decoding Register Tokens Preserves Global Scene Details](https://arxiv.org/abs/2610.13299) | 2026-10-09 | metadata_only | prior_related_discovery |
| [PeekKV: The First Content Token Already Knows Which Heads Matter](https://arxiv.org/abs/2610.23939) | 2026-10-08 | index_metadata_only | seed_title_fulltext_index |
| [Kronecker Product Attention: Memory-Efficient KV Compression via Structured Factorization](https://arxiv.org/abs/2610.12657) | 2026-10-08 | index_metadata_only | seed_title_fulltext_index |
| [VFold: Symmetry-Aware Cross-Layer Value Cache Compression](https://arxiv.org/abs/2610.12338) | 2026-10-08 | index_metadata_only | seed_title_fulltext_index |
| [Rehearse Everything, Remember Nothing: Attic-KV Rehearses What Will Be Read](https://arxiv.org/abs/2610.12133) | 2026-10-08 | index_metadata_only | seed_title_fulltext_index |
| [GRPODropout: Less is More for Online Reinforcement Learning Rollouts](https://arxiv.org/abs/2610.11854) | 2026-10-08 | metadata_only | attention_concentration_keywords |
| [SAGE: Sink-Aware Guided Emphasis for Visual Grounding in Vision-Language Decoders](https://arxiv.org/abs/2610.11469) | 2026-10-08 | index_metadata_only | seed_title_fulltext_index; attention_concentration_keywords; prior_sink_keyword_discovery |
| [QUILT: Rethinking Sparse-Attention Prefill through Shared Query Execution](https://arxiv.org/abs/2610.11134) | 2026-10-08 | index_metadata_only | seed_title_fulltext_index |
| [Lapras: Latent Reasoning for Time Series Language Models](https://arxiv.org/abs/2610.11111) | 2026-10-08 | index_metadata_only | seed_title_fulltext_index |
| [LaMAR: Latent Multi-agent Collaboration via KV-Cache Communication for Automated Program Repair](https://doi.org/10.1145/3832783.3837423) | 2026-10-07 | index_metadata_only | seed_title_fulltext_index |
| [AbridgeKV: Compressing Long Reasoning into the KV Cache of Learned Pause Tokens](https://arxiv.org/abs/2610.20641) | 2026-10-07 | index_metadata_only | seed_title_fulltext_index |
| [Omni-Diffusion-Distill: Few-Step Distillation of Unified Multimodal Diffusion Large Language Models](https://arxiv.org/abs/2610.10990) | 2026-10-07 | metadata_only | attention_concentration_keywords |
| [Sparse Attention Is Matrix Approximation, Not Choosing from a Bag of Values](https://arxiv.org/abs/2610.10871) | 2026-10-07 | index_metadata_only | seed_title_fulltext_index |
| [Attention via Black-Box Vector Search](https://arxiv.org/abs/2610.10135) | 2026-10-07 | index_metadata_only | seed_title_fulltext_index |
| [Mechanics of Long-Context Hybrid Models Part 1.1: From Hybrid Attention to Hybrid Position](https://arxiv.org/abs/2610.10114) | 2026-10-07 | index_metadata_only | seed_title_fulltext_index |
