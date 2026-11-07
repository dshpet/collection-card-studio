# Academic image generation and style

**Reference-conditioned image creation and selective appearance control are established research capabilities; a universal system of independently calibrated artistic axes is not.** The literature offers several routes to useful control: statistical style transfer, learned adaptations, spatial conditioning, inversion and feature reuse, explicit graphics, physically informed proxies, and agents that search among tools and candidates. These routes expose different variables and preserve different information. Their demonstrations do not justify treating a prompt adjective, adapter weight, embedding coordinate, rendered roughness, and human gloss judgment as interchangeable quantities. For the proposed reference → specification → generation → diagnosis → targeted-correction process, the strongest opportunity is to connect a small, meaningful vocabulary to observable evidence and backend-specific interventions, then test target improvement and protected-property survival independently. The generic loop and many components already have substantial prior art. Its reliability for collectible-card artwork, rather than the mere presence of an agent or a style vector, remains the substantive research question.

**Evidence cutoff: 2026-10-31. Status: research synthesis, not an adopted architecture, implemented feature extractor, deployment recommendation, or benchmark result.** This volume synthesizes twelve saved academic notes. The direct-control and correction-strategy audits refine earlier claims, and the record-reconciliation audit takes priority for bibliographic and artifact corrections. All original notes remain dated research snapshots. This writing phase conducted no new searches, external source retrieval, generation, training, installation, or hardware experiments.

The companion [*Measuring and controlling visual style*](measuring-visual-style.md) develops the image-axis vocabulary, preprocessing contracts, formulas, and tool-level measurement cautions. This volume instead explains the academic mechanisms that create, transfer, constrain, and edit appearance; the evidence behind their controls; and the experiments needed before relying on them. Neither volume claims measurements of the project’s artwork or calibrated acceptance thresholds. Reduced references constrain fine-scale empirical conclusions, but do not prevent investigating mechanisms or designing sound experiments.

## Reader map

| Chapter | Question answered |
|---|---|
| [1. Generation families expose different contracts](#1-generation-families-expose-different-contracts) | How do objectives, representations, factorization, and conditioning differ? |
| [2. Style representations transfer appearance without identifying pure style](#2-style-representations-transfer-appearance-without-identifying-pure-style) | What do statistics, tokens, adapters, and attention actually represent? |
| [3. Direct axis control is real but locally qualified](#3-direct-axis-control-is-real-but-locally-qualified) | How strong is the closest evidence for the proposed artistic controls? |
| [4. Adaptation learns correlations as well as intended invariants](#4-adaptation-learns-correlations-as-well-as-intended-invariants) | When do personalization and fine-tuning help or interfere? |
| [5. Structured conditions improve binding without guaranteeing independence](#5-structured-conditions-improve-binding-without-guaranteeing-independence) | What do layouts, graphs, maps, and multi-condition systems establish? |
| [6. Editing requires a preservation contract](#6-editing-requires-a-preservation-contract) | Why are reconstruction, inversion, and successful minimal editing different? |
| [7. Physical and 3D assistance supply useful scaffolds](#7-physical-and-3d-assistance-supply-useful-scaffolds) | When can geometry and transport help without recovering the true scene? |
| [8. NPR makes depiction decisions explicit](#8-npr-makes-depiction-decisions-explicit) | What controls exist for strokes, vectors, shading, abstraction, and asset collections? |
| [9. Agentic creation spans several different search problems](#9-agentic-creation-spans-several-different-search-problems) | Which loops, optimizers, and learned policies have image-domain evidence? |
| [10. Correction policy depends on what must survive](#10-correction-policy-depends-on-what-must-survive) | How should apparently conflicting sequential/parallel results be reconciled? |
| [11. Evaluation must distinguish ranking from release acceptance](#11-evaluation-must-distinguish-ranking-from-release-acceptance) | Which constructs, benchmarks, human protocols, and errors matter? |
| [12. Artifact readiness is separate from scientific relevance](#12-artifact-readiness-is-separate-from-scientific-relevance) | What can be reused, what needs training, and what remains uncleared? |
| [13. A research program should isolate information and intervention value](#13-a-research-program-should-isolate-information-and-intervention-value) | What would test the proposed workflow without presupposing its success? |
| [Conclusion](#conclusion) | What is the defensible contribution? |
| [Curated paper index](#curated-paper-index) | Which primary works should be read, and in what order? |
| [Source notes and evidence limits](#source-notes-and-evidence-limits) | Where are the broader ledgers, corrections, and research accounting? |

## 1. Generation families expose different contracts

### Representation, objective, factorization, and conditions are separate choices

Dividing image generation into “diffusion versus autoregression” hides important combinations. A system chooses a representation—pixels, continuous compressed latents, discrete visual codes, semantic features, or explicit scene variables. It chooses an objective, such as adversarial learning, score/noise prediction, velocity regression, consistency, or categorical likelihood. It also chooses how decisions depend on previous decisions: raster order, scale hierarchy, masked parallel refinement, or whole-image dynamics. Finally, the training tasks and conditioning interfaces determine whether text, reference images, structural maps, instructions, and edit histories have supported meanings. These dimensions are related but not equivalent. MAR predicts continuous tokens with a diffusion loss; NextStep-1 combines autoregressive context with visual flow matching; UniAR uses discrete shared context and a diffusion decoder. ([MAR](https://arxiv.org/abs/2406.11838); [NextStep-1](https://arxiv.org/abs/2508.10711); [UniAR](https://proceedings.mlr.press/v306/peng26k.html))

| Dimension | Representative alternatives | Consequence for an artistic-control investigation |
|---|---|---|
| Representation | Pixels; VAE latents; quantized codes; strokes; geometry and buffers | Determines which detail is retained and which variables can be directly constrained. |
| Objective | Adversarial; score/noise; flow matching; consistency; token prediction | Determines what is learned, not automatically what semantic attributes are independent. |
| Factorization | Raster tokens; next scale; masked tokens; global denoising | Changes scheduling and dependencies, not the definition of style. |
| Conditioning | Text; instances; maps; image references; edit instructions | Determines available information and intervention interfaces. |
| Access | Black-box service; exposed model internals; authored graphics program | Determines whether feature injection, gradients, or exact source copying are possible. |

The practical question is therefore not which family is universally best. It is which formulation can express the required change, retain the necessary information, and expose a testable preservation contract. A model can have excellent broad synthesis quality and lack the interface needed to retain a tiny emblem. Conversely, an explicit vector or renderer parameter can precisely implement one operation while covering only a narrow part of the desired visual repertoire. The historical foundations and contemporary hybrids support this distinction; they do not establish a portable architecture leaderboard. ([Latent diffusion](https://arxiv.org/abs/2112.10752); [Mitsuba 2](https://rgl.epfl.ch/publications/NimierDavidVicini2019Mitsuba2))

### Diffusion and score models learn conditional distributions, not scene decompositions

A common diffusion construction corrupts an image through

\[
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,
\qquad
\mathcal L_\epsilon=\mathbb E\|\epsilon-\epsilon_\theta(x_t,t,c)\|^2.
\]

Here the condition \(c\) influences the learned reverse process. Score-based formulations instead emphasize \(s_\theta(x,t,c)\approx\nabla_x\log p_t(x\mid c)\), with reverse stochastic dynamics and an associated probability-flow ODE under ideal conditions. These formulations explain why several samplers can use related learned information, and why deterministic sampling is not a separate semantic representation. They do not imply that the resulting image carries recoverable original light, camera, or material variables. ([DDPM](https://arxiv.org/abs/2006.11239); [Score-SDE](https://arxiv.org/abs/2011.13456))

Latent diffusion adds an encoder and decoder, \(z=E(x)\) and \(\hat x=D(z)\), before learning repeated synthesis in the compressed space. This reduces the repeated generative workload but introduces a distinct reconstruction question. An outline, small marking, or letter that changes during the source round trip cannot be diagnosed solely as a prompt-following failure. The appropriate research baseline separates autoencoding, generation, and editing. An autoencoder round trip is an operational baseline for that encoder, not a proof that no other latent could reconstruct the pixels better. ([Latent diffusion](https://arxiv.org/abs/2112.10752); [EDICT](https://arxiv.org/abs/2211.12446))

Classifier-free guidance illustrates another necessary distinction. In one convention, \(s_g=s_u+w(s_c-s_u)\). Increasing \(w\) changes the sampling field and its quality/diversity operating point. It is not a calibrated increase in painterliness, gloss, contrast, or semantic correctness. Likewise, a negative prompt is a conditional intervention rather than a guarantee that one factor is removed without compensating changes. Guidance, reference strength, adapter strength, and an artist’s intended attribute magnitude must remain different variables. ([Classifier-free guidance](https://arxiv.org/abs/2207.12598))

### Transformers, flow models, and acceleration change computation rather than certify control

DiT replaces a conventional denoising backbone with a transformer operating on latent patches. Its original scaling evidence concerns class-conditional ImageNet generation. The SD3 research instead combines rectified-flow training and multimodal transformer interactions for text-conditioned synthesis. Those are distinct experimental settings: improvements on class-conditional distribution metrics do not establish counting, reference fidelity, or protected-region preservation in an instruction editor. Attention enables interactions; it does not by itself enforce correct binding. ([DiT](https://arxiv.org/abs/2212.09748); [Scaling rectified-flow transformers](https://arxiv.org/abs/2403.03206))

Recent pixel-space work also prevents treating the VAE bottleneck as mandatory. JiT predicts clean images using pixel transformers, while PixelDiT combines patch-level semantics with pixel-level detail and includes text-to-image experiments. PixelDiT2 adds representation grounding during sampling; its September 2026 record reports NeurIPS acceptance, but proceedings and complete checkpoint availability were not established in the saved audit. These developments support the narrower conclusion that transformer generation need not use a pretrained lossy autoencoder. They do not establish that pixel-space systems are invariably cheaper, more editable, or better for collectible cards. ([JiT](https://arxiv.org/abs/2511.13720); [PixelDiT](https://arxiv.org/abs/2511.20645); [PixelDiT2](https://arxiv.org/abs/2609.24919))

For a simple flow-matching path from noise \(x_0\) to data \(x_1\), one writes \(x_t=(1-t)x_0+tx_1\) and trains a velocity field toward \(x_1-x_0\). Sampling integrates the learned field. Flow matching supports more general paths, while rectified flow uses straight interpolations and reflow to improve transport trajectories. Straight conditional training paths do not guarantee straight marginal sampling paths. Nor does a velocity vector mean “reduce background detail while preserving the object.” Normalizing flows are different again: their invertible change-of-variables likelihood objective should not be conflated with velocity regression. STARFlow2 is a current preprint combining autoregressive VLM context with a normalizing-flow stream, not evidence that all “flow” models share one algorithm. ([Flow matching](https://arxiv.org/abs/2210.02747); [Rectified flow](https://arxiv.org/abs/2209.03003); [STARFlow2](https://arxiv.org/abs/2605.08029))

Consistency models, latent consistency, distribution-matching distillation, and MeanFlow pursue fewer evaluations through different targets. Consistency maps states on a trajectory toward a common endpoint; DMD2 matches generated distributions without requiring teacher-path correspondence; MeanFlow models average velocity and supports one-step training without a pretrained teacher in its reported setting. Reduced evaluation count can make exploration more practical, but does not establish equal editing behavior, identical seed-wise outputs, lower memory, or a lower complete-system cost. Accelerated backends require their own control and preservation validation. ([Consistency models](https://arxiv.org/abs/2303.01469); [LCM](https://arxiv.org/abs/2310.04378); [DMD2](https://arxiv.org/abs/2405.14867); [MeanFlow](https://arxiv.org/abs/2505.13447))

### Visual tokens and unified models broaden interfaces without removing reconstruction limits

Discrete autoregression models \(p(z\mid c)=\prod_i p(z_i\mid z_{<i},c)\). VQGAN-style compression makes image tokens available to transformers, while MaskGIT recovers masked tokens bidirectionally and refines them in parallel. VAR predicts a hierarchy of scales rather than a raster sequence; Infinity extends next-scale generation through bitwise prediction. Spatial codes and coarse-to-fine schedules provide useful intervention surfaces, but a code is not a named artistic variable. Unchanged tokens also do not automatically imply identical decoded pixels outside a fine boundary. ([Taming transformers](https://arxiv.org/abs/2012.09841); [MaskGIT](https://arxiv.org/abs/2202.04200); [VAR](https://arxiv.org/abs/2404.02905); [Infinity](https://arxiv.org/abs/2412.04431))

Continuous-token MAR and NextStep-1 demonstrate that autoregression does not require quantization. Emu3 demonstrates discrete multimodal next-token modeling, while UniAR combines shared discrete context with a generative visual decoder. A shared understanding/generation representation can support introspection without exposing every artifact subsequently introduced by pixel decoding. That last concern is a testable inference, not an observed failure of every shared-token system. ([MAR](https://arxiv.org/abs/2406.11838); [NextStep-1](https://arxiv.org/abs/2508.10711); [Emu3](https://arxiv.org/abs/2409.18869); [UniAR](https://proceedings.mlr.press/v306/peng26k.html))

InstructPix2Pix established instruction-native editing through synthetic source/instruction/target training. OmniGen, BAGEL, Show-o2, Qwen-Image, and UniReason broaden unified or reasoning-enabled interfaces, but do not use one identical mechanism. Qwen-Image’s semantic and VAE processing makes the difference between understanding and reconstruction especially explicit. BAGEL’s repository corrections also show why reported evaluations need version provenance. A conversational interface or visually convincing output cannot reveal an undisclosed commercial model’s architecture; this synthesis makes no such inference. ([InstructPix2Pix](https://arxiv.org/abs/2211.09800); [OmniGen](https://arxiv.org/abs/2409.11340); [BAGEL](https://arxiv.org/abs/2505.14683); [Show-o2](https://arxiv.org/abs/2506.15564); [Qwen-Image](https://arxiv.org/abs/2508.02324); [UniReason](https://arxiv.org/abs/2602.02437))

GANs remain important rather than obsolete precedents. StyleGAN’s mapped latent, layer-wise modulation, and stochastic inputs enable useful restricted-domain controls and informed later work on appearance spaces. However, “style” in that architecture names a modulation mechanism, not an identified vocabulary of artistic factors. Explicit rendering and constructive NPR provide another lineage: known authored inputs can have operational meanings even while their visible effects remain coupled. ([GAN](https://arxiv.org/abs/1406.2661); [StyleGAN](https://arxiv.org/abs/1812.04948))

## 2. Style representations transfer appearance without identifying pure style

### The statistical genealogy supplies explicit but incomplete definitions

Gatys-style transfer represents content through selected feature activations and style through channel correlations, often written \(G_l=F_lF_l^\top\). Pooling removes explicit arrangement of feature-map locations; it does not remove semantic dependence from the features themselves. The statistic is invariant to permutation of feature columns, not arbitrary input pixels. This explains why such losses can reproduce recurring marks while misplacing texture or importing a visually compatible but semantically wrong pattern. Convincing transfer is evidence that the representation captures useful appearance, not that it exhausts artistic style. ([Gatys](https://arxiv.org/abs/1508.06576))

Conditional normalization made styles reusable learned parameter settings. AdaIN then matched channel means and standard deviations, \(\mathrm{AdaIN}(x,y)=\sigma(y)(x-\mu(x))/\sigma(x)+\mu(y)\), supporting arbitrary-reference transfer through a learned decoder. WCT extends matching to covariance through whitening and coloring. These are unusually interpretable operational definitions compared with an opaque “style score,” yet means, covariance, and correlations do not uniquely specify a composition, semantic abstraction, material convention, or brush allocation. Decoder reconstruction introduces another source of unintended change. ([Learned style representation](https://arxiv.org/abs/1610.07629); [AdaIN](https://arxiv.org/abs/1703.06868); [WCT](https://arxiv.org/abs/1705.08086))

MUNIT’s domain-invariant content and domain-specific style codes, and StyTr²’s separate encoders, are useful inductive biases. Their branch names are not proofs of pure compartments. Learned retrieval spaces such as ALADIN and CSD define similarity through groupings and labels; those labels can correlate with artists’ preferred subjects or compositions. StyleTokenizer and learned image tokens create effective conditioning interfaces without automatically exposing measurable palette, lighting, contour, and shape coordinates. ([MUNIT](https://arxiv.org/abs/1804.04732); [StyTr²](https://arxiv.org/abs/2105.14576); [ALADIN](https://arxiv.org/abs/2103.09776); [CSD](https://arxiv.org/abs/2404.01292); [StyleTokenizer](https://arxiv.org/abs/2409.02543))

### Adapters and attention localize interventions, not necessarily semantics

IP-Adapter separates image- and text-conditioned attention pathways. An image embedding still contains subject, pose, layout, palette, and rendering information; architectural separation of inputs is not semantic separation of their contents. ArtAdapter and DEADiff add explicit content handling or paired supervision precisely because reference leakage is a real problem. The appropriate question is what unwanted information remains after conditioning, not whether an implementation calls one branch “style.” ([IP-Adapter](https://arxiv.org/abs/2308.06721); [ArtAdapter](https://openaccess.thecvf.com/content/CVPR2024/html/Chen_ArtAdapter_Text-to-Image_Style_Transfer_using_Multi-Level_Style_Encoder_and_Explicit_CVPR_2024_paper.html); [DEADiff](https://arxiv.org/abs/2403.06951))

StyleAligned shares attention to coordinate outputs; StyleID combines content queries with style keys and values; InstantStyle uses content subtraction and selected SDXL blocks; B-LoRA jointly learns selected parameter blocks. These mechanisms provide meaningful handles, but remain backbone-, layer-, schedule-, and optimization-dependent. Stronger query preservation or teacher influence can weaken style. Sharing features can import reference geometry. A block empirically useful for style in one architecture is not a universal anatomical location of style in all generators. ([StyleAligned](https://arxiv.org/abs/2312.02133); [StyleID](https://arxiv.org/abs/2312.09008); [InstantStyle](https://arxiv.org/abs/2404.02733); [B-LoRA](https://arxiv.org/abs/2403.14572))

Structured supervision is consequential. CSGO’s synthetic content/style triplets, OmniStyle’s generated and filtered pairs, StyleShot’s staged encoding, and SCFlow’s crossed content/style construction offer more evidence than isolated reference reconstructions. They also inherit teacher decisions, filtering biases, finite taxonomies, and imperfect release coverage. A dataset reported at one scale is not necessarily the publicly released subset. StyleShot’s training dataset **StyleGallery** is a different entity from the **StyleGallery method published at CVPR 2026**. The latter uses regional matching, whose clustering can itself combine semantically inappropriate regions. ([CSGO](https://arxiv.org/abs/2408.16766); [OmniStyle](https://arxiv.org/abs/2505.14028); [StyleShot](https://arxiv.org/abs/2407.01414); [SCFlow](https://arxiv.org/abs/2508.03402); [StyleGallery proceedings](https://openaccess.thecvf.com/content/CVPR2026/html/He_StyleGallery_Training-free_and_Semantic-aware_Personalized_Style_Transfer_from_Arbitrary_Image_CVPR_2026_paper.html))

### Identifiability theory supports structured evidence rather than purity claims

Unsupervised disentanglement is not uniquely identifiable without suitable inductive biases or supervision under Locatello and colleagues’ assumptions. This does not forbid useful learned controls. It forbids treating reconstruction or smooth interpolation alone as identification of the correct semantic factors. Augmentation-based theory can identify invariant content blocks up to invertible mappings under additional assumptions; the augmentation defines what is permitted to vary. Declaring color jitter to be “style” is a task choice, not discovery that color can never carry identity. ([Locatello et al.](https://proceedings.mlr.press/v97/locatello19a.html); [Content/style isolation](https://proceedings.neurips.cc/paper/2021/hash/8929c70f8d710e412d38da624b21c3c8-Abstract.html); [Structured augmentations](https://arxiv.org/abs/2311.08815))

CLeaR makes the leakage–degradation dilemma explicit: projecting estimated content out of features can also erase legitimate style. Its September 2026 preprint reports sparse-style failures including blank or copied anchors. Its ensemble analysis depends on conditions such as local identifiability and limited error dependence; it is not an unconditional guarantee for the implemented optimizer. UniCSG’s semantic/frequency interventions similarly offer a useful bias, not a universal partition where low frequency means content and high frequency means style. Small markings can carry identity, and broad color masses can carry style. ([CLeaR](https://arxiv.org/abs/2609.38136); [UniCSG](https://arxiv.org/abs/2604.17850))

The defensible research claim is therefore conditional: a representation retains specified appearance while suppressing specified content variation under a declared task, dataset, and preservation criterion. This is stronger and more actionable than calling an embedding “pure style,” because it makes the missing counterexamples and tests visible.

## 3. Direct axis control is real but locally qualified

### Concept Sliders learns specified directions, not attribute units

Concept Sliders is close prior art for reusable corrections. It trains low-rank parameter changes from textual contrasts or paired images, giving an intervention of the form \(W(\alpha)=W_0+\alpha BA\). Preservation concepts discourage selected unwanted associations. A scalar controls sign and strength, but is not the quantity named by the slider: neither age in years nor rust coverage follows from its coefficient. Paired artist-created examples can define difficult visual contrasts better than unrelated images labeled with opposing adjectives, but the examples must isolate the intended difference. If gloss, light direction, and contour all change together, the learner receives evidence for a bundle. ([Concept Sliders §4](https://arxiv.org/html/2311.12092#S4))

The age ablation supplies concrete selectivity evidence. The full method reports ΔCLIP 3.93, LPIPS 0.06, and interference 0.10, against interference 0.36 without its disentanglement formulation and 0.19 without its low-rank constraint. This supports **reduced measured interference, not zero interference**. LPIPS also includes the desired change and cannot certify every protected emblem, part, or color assignment. Scheduling sliders later preserves structure more strongly while limiting edit strength. This is an operating trade-off, not a separate guarantee. ([Concept Sliders Table 3 and limitations](https://arxiv.org/html/2311.12092#S7))

Its human checks concern hands and repair, not a broad inventory of independent artistic axes. Matched-prompt/seed hand examples produce majority-labeled problems in 62% of base outputs versus 22% of slider outputs. The repair study reports approximately 80.39% preference, with main-text and appendix aggregation descriptions that the audit does not treat as a universal correction rate. Weather examples also reveal semantic bundles: snow, vegetation, brightness, and decorative elements can accompany a named direction. These are useful effects when desired, leakage when prohibited, and neither category is settled by the slider name. ([Concept Sliders human evaluation](https://arxiv.org/html/2311.12092))

### SliderSpace discovers what a generator varies, then learns to reproduce it

SliderSpace samples outputs, embeds them, applies PCA, and trains LoRA adapters aligned with principal variations. Its objective relates induced embedding change to a principal direction, for example \(\sum_i[1-\cos(\Delta\phi_i,v_i)]\). The paper suggests roughly 5,000 samples for stable decomposition, while its implementation offers smaller sets. Language-model descriptions are assigned after discovery. **New discovery requires sampling and training**; a promotional “no training” phrase elsewhere cannot supersede the method and its training scripts. ([SliderSpace §4.2](https://arxiv.org/html/2502.01639#S4.SS2); [official repository](https://github.com/rohitgandikota/sliderspace))

Orthogonal encoder directions are not independent human-perceptual factors. Changing the embedding changes which variation becomes prominent; the paper finds more color/texture/shape variation when using diffusion-output space instead of the semantic encoder. Its human experiment compares nine-image grids for diversity, usefulness, and creativity, not one-factor preservation. Reported wins over artist-name prompting are 54% for diversity and 63% for usefulness in that protocol. Generated names can be ambiguous, and delayed slider application again trades structural preservation against strength. This is valuable actuator discovery, but not automatic recovery of the user’s reference taxonomy. ([SliderSpace experiments and appendices](https://arxiv.org/html/2502.01639))

### Gatys, StyleBlend, and StyleStudio expose different kinds of selectivity

Gatys’s 2017 perceptual-factor work already provides regional, color, and scale interventions. Masks constrain corresponding regions, luminance-only or distribution-matching operations handle color, and staged synthesis combines scales. The paper explicitly states that simply combining Gram matrices across scales does not provide independent scale control; it constructs an intermediate image instead. Receptive-field overlap can leak texture across naive masks, and luminance-only transfer can disrupt luminance/chroma relationships. This is strong operational prior art, not a proof that scale, color, and spatial appearance are independent perceptual axes. ([Controlling perceptual factors §§4–6](https://arxiv.org/html/1611.07865))

StyleBlend learns complementary composition and texture pathways from one or three references. Texture learning tunes an embedding and denoiser LoRA, while composition learning uses SDEdit variants and text-encoder adaptations; branches exchange attention information. Evaluation uses style similarity and text alignment, including maximum similarity to any reference in its multi-reference setting. That maximum is not consistency with every reference. The audited study lacks a human test isolating composition-versus-texture invariance and reports weaker one-shot text alignment, a black-and-white palette failure, and dual-branch inference cost. Its decomposition is real engineering prior art, but not a full lighting/palette/material/shape factorization. ([StyleBlend methods and failures](https://arxiv.org/html/2502.09064))

StyleStudio adds cross-modal AdaIN, early teacher guidance, and negative-style-image guidance. A negative reference acts as a constructed counterexample: retain relevant structure while removing the influence to be transferred. Examples suppress snow, night, and leaves. The human study of 49 participants and 12 reference/prompt pairs supports text/style preference for tested outputs, while negative-reference selectivity is chiefly demonstrated by examples. Longer teacher participation stabilizes layout but weakens style, and preparing meaningful negatives requires expertise. This is an inference-time experiment candidate over pretrained components, not an independently calibrated continuous scale. ([StyleStudio](https://arxiv.org/html/2412.08503); [implementation guidance](https://github.com/Westlake-AGI-Lab/StyleStudio))

### Controlled stylized objects provide the strongest narrow appearance-axis case

Artist-Inator’s 2025 project reports 1,336,272 stylized images with automatically generated appearance descriptions and a structure-conditioned SDXL ControlNet. The descriptions cover objects, color, medium, and gloss category. That is direct painterly-object prior art, not merely transfer from portraits or photographs. However, the later gloss study identifies a confound: separately painted spheres at different gloss levels also change brushstroke patterns, so a learner can cluster strokes instead of the intended gloss. A larger corpus does not by itself break an unwanted correlation. Details of Artist-Inator’s original full evaluation remain partly inaccessible in the saved research, and are not invented here. ([Artist-Inator project](https://graphics.unizar.es/projects/artist-inator_2025/); [later gloss analysis](https://arxiv.org/html/2602.16611v3))

*Style-Aware Gloss Control for Generative Non-Photorealistic Rendering* constructs 10,080 images from **three styles, twenty geometries, four illuminations, seven gloss levels, and six colors**. Charcoal, ink pen, and oil painting form the style vocabulary. Rendered spheres vary Disney Principled BSDF roughness, but a brushstroke map is reused before StyLit transfer to reduce brushstroke/gloss confounding. This is a deliberately restricted factor design, not discovery of unconstrained artistic factors from arbitrary images. ([Gloss v3 §3.2](https://arxiv.org/html/2602.16611v3#S3.SS2))

The learned representation uses StyleGAN2-ADA and a pSp encoder producing **sixteen layer codes, each 512-dimensional**. The finding that layer 6 is informative about gloss is not a native one-dimensional physical scalar. Factor labels are used for conditional mutual information, clustering, regression, and permutation tests. Five-fold sample-level cross-validation gives gloss MSE 0.1224 ± 0.0229 and Spearman 0.97. These are strong ordered-label prediction results within the constructed distribution, not arbitrary-artwork roughness recovery or leave-object-out generalization. Labels are absent from generator/encoder training but essential to identifying and evaluating what the representation learned. ([Gloss v3 §4.4](https://arxiv.org/html/2602.16611v3#S4.SS4))

A trained W+ adapter conditions SDXL; structural conditioning and optional albedo guidance support geometry and color. The inspected notebook interpolates matte/glossy reference embeddings and obtains a layer interval through checkpoint configuration. It contains author-local paths, checkpoint/configuration placeholders, and CUDA assumptions. This is substantive implementation, but not proof of a universal “layer 6 scalar” actuator or a turnkey package. Illumination control is bounded by the four trained conditions. ([Gloss v3 §5](https://arxiv.org/html/2602.16611v3#S5); [official notebook](https://github.com/SantiagoJN/npr_gloss_disent/blob/main/notebooks/Wplus_demo.ipynb))

The **v3 human study has 21 participants**. One experiment ranks seven methods for reference-style matching across twelve examples; another orders five outputs from matte to glossy across five examples. The latter reports MAE 0.26, RMSE 0.37, and exact-rank fraction 0.79 for the proposed method, versus 0.90, 1.18, and 0.48 for its ConceptSliders comparison. This supports more recoverable **ordinal progression in these stimuli**, not equal perceptual spacing, absolute roughness calibration, overall aesthetic superiority, or absence of non-target changes. The authors say the study does not support statistically robust factor-by-factor conclusions. ([Gloss v3 §5.3](https://arxiv.org/html/2602.16611v3#S5.SS3))

Version identity is essential: the accessible v1 supplement has **22 participants** and an older protocol. Those details must not be combined with v3’s 21-person, two-experiment study. Unseen watercolor and soft-crayon styles require training or fine-tuning; graphic ellipses and crosshatching may require different synthesis or supervision. Qualitative geometry examples do not constitute systematic leave-object-out evidence. The public dataset describes 10,080 **unlabeled** images with only an image feature; public factor-to-image mappings and exact renderer labels were not established. These limitations narrow the result without negating its importance as a direct stylized-object control case. ([v1](https://arxiv.org/html/2602.16611v1); [v3 limitations](https://arxiv.org/html/2602.16611v3#S6.SS1); [dataset](https://huggingface.co/datasets/SantiagoJN/NPR_gloss_dataset))

### The evidence ladder must remain visible

| Claim | Assessment supported by the audited sources |
|---|---|
| A reusable direction can change a named appearance property | Established for particular trained directions and tasks. |
| Several conditioning inputs can be satisfied together | Supported by multiple methods, but depends on inputs and evaluation. |
| One requested property can change with reduced interference | Supported locally in selected ablations and restricted domains. |
| A coefficient equals a calibrated perceptual attribute value | Not established generically; requires external calibration. |
| Orthogonal learned features imply independent human axes | Not established. |
| Arbitrary references yield universally independent controls | Not established by this corpus. |

This ladder avoids two mistakes: dismissing substantial control research because it is imperfect, and overstating local evidence as a solved general artistic-control problem. The specific experiments in audit 10 are the controlling evidence for this chapter.

## 4. Adaptation learns correlations as well as intended invariants

Subject, style, concept, and preference adaptation have different targets. DreamBooth binds a particular instance to an identifier and class description; Textual Inversion learns conditioning embeddings with a frozen generator; whole-style adaptation seeks appearance across changing content. A token named “style” does not receive a reliable semantic type merely from its spelling. If every example shares a view, backdrop, object family, and palette, reconstructing them rewards the combination. ([DreamBooth](https://arxiv.org/abs/2208.12242); [Textual Inversion](https://arxiv.org/abs/2208.01618))

LoRA parameterizes an update as \(W'=W+\lambda BA\). Its rank controls capacity, not the number of interpretable artistic dimensions. DreamBooth-style supervision can use LoRA storage; these are not competing definitions of one operation. Custom Diffusion restricts cross-attention updates, Perfusion uses gated rank-one edits with category key-locking, and OFT constrains orthogonal transformations. DoRA separates magnitude and low-rank direction, while LyCORIS variants alter update structure. Their efficiency and parameter geometry do not establish independent image attributes. Original language-model LoRA memory savings must not be relabeled as image-personalization measurements. ([LoRA](https://arxiv.org/abs/2106.09685); [Custom Diffusion](https://arxiv.org/abs/2212.04488); [Perfusion](https://arxiv.org/abs/2305.01644); [OFT](https://arxiv.org/abs/2306.07280); [DoRA](https://arxiv.org/abs/2402.09353); [LyCORIS](https://arxiv.org/html/2309.14859v2))

### There is no universal example count or caption recipe

Few-shot claims need their task and exposure conditions. DreamBench’s subject images, Custom Diffusion’s examples and regularization images, and single-image style-separation tests estimate different generalization problems. Extra near-duplicate crops are not equivalent to new object families. Repeats, balanced sampling, total presentations, resolution, caption quality, and adaptation capacity change what a nominal epoch means. LyCORIS reports overtraining of small classes under some repetition schedules and undertraining without balancing; raw file count cannot summarize that interaction. ([DreamBooth dataset](https://github.com/google/dreambooth); [Custom Diffusion](https://github.com/adobe-research/custom-diffusion); [LyCORIS](https://arxiv.org/html/2309.14859v2))

Captions can assign variable object, viewpoint, and background information to separate conditions rather than one trigger. But captioning a constant property does not create a counterexample; automatic captions can add confounds; and describing every attribute can change what the adaptation learns. DreamBooth’s autogenous class prior regularizes the original class distribution, not necessarily the desired illustration domain. Class-prior preservation is a training mechanism, whereas classifier-free guidance changes sampling. They should not be combined under an undifferentiated “preservation strength.” ([DreamBooth](https://arxiv.org/abs/2208.12242); [Classifier-free guidance](https://arxiv.org/abs/2207.12598))

### Compatibility and overfitting require different tests

ZipLoRA learns how to combine independently trained subject/style adaptations; UnZipLoRA jointly separates them from a mixed reference; B-LoRA exploits selected blocks; QR-LoRA constrains a QR-derived update basis. These approaches corroborate interference as a real problem. They do not show that arbitrary adapters can be summed without interaction. QR-LoRA’s repository explicitly warns that disentanglement does not guarantee good merging. T-LoRA addresses timestep-dependent overfitting, yet its human study favors its overall output while favoring ordinary LoRA for concept preservation. A nearly unchanged embedding similarity can conceal a perceived identity trade-off. ([ZipLoRA](https://arxiv.org/abs/2311.13600); [UnZipLoRA](https://arxiv.org/abs/2412.04465); [QR-LoRA repository](https://github.com/luna-ai-lab/QR-LoRA); [T-LoRA](https://arxiv.org/html/2507.05964v2))

Overfitting means poor generalization; entanglement means a requested change drags other properties; memorization means reproduction of examples or fragments. They overlap but are not synonyms. Diffusion training-image extraction establishes that memorization can occur, not a numerical copying risk for a particular small style adaptation. A credible experiment needs held-out object families, combinations, and views, plus diversity and nearest-example inspection—not only trigger reconstruction. ([Training-data extraction](https://arxiv.org/abs/2301.13188); [DreamBench++](https://arxiv.org/abs/2406.16855))

“Training-free” must describe a stage. A pretrained adapter requires upstream training; inversion can require per-image optimization; hypernetwork prediction amortizes training rather than removing it; fusion can be training-free after separate adapters already exist. CRAFT-LoRA includes preparatory training and routing despite training-free fusion, and current TextBoost differs materially from its initial preprint. Version-specific recipes and dependencies belong in the experiment record. The research question is whether adaptation improves the held-out consistency/control frontier, not which trainer name is intrinsically best. ([IP-Adapter](https://arxiv.org/abs/2308.06721); [CRAFT-LoRA](https://arxiv.org/html/2602.18936v3); [TextBoost repository](https://github.com/nahyeonkaty/textboost))

## 5. Structured conditions improve binding without guaranteeing independence

### Conditions differ in the information they actually supply

A scene graph encodes instances and relations; a layout adds coordinates; dense maps encode selected structure; references carry appearance and identity together. sg2im explicitly constructs layouts from graphs, whereas a graph converted back into prose loses a direct coordinate constraint. A box does not specify internal pose or silhouette. A Canny map includes texture, shading boundaries, and compression artifacts unless curated. A depth map needs relative/metric and coordinate conventions; normals need their frame and orientation. Multiple maps derived from one estimate do not become independent evidence merely because they have different channel counts. ([sg2im](https://github.com/google/sg2im); [SimGraph](https://arxiv.org/html/2601.21498v1); [InstanceDiffusion](https://github.com/frank-xwang/InstanceDiffusion))

ControlNet, T2I-Adapter, GLIGEN, MultiDiffusion, BoxDiff, and FreeControl offer different learned or inference-time routes to conditioning. Residual injection, attention routing, gradient guidance, and merging conditioned paths are not interchangeable computations. Several require internal model access unavailable through an ordinary black-box image service. Avoiding new controller training can move work into inference-time optimization rather than eliminating it. ([ControlNet](https://arxiv.org/abs/2302.05543); [GLIGEN](https://github.com/gligen/GLIGEN); [T2I-Adapter](https://github.com/TencentARC/T2I-Adapter); [BoxDiff](https://openaccess.thecvf.com/content/ICCV2023/html/Xie_BoxDiff_Text-to-Image_Synthesis_with_Training-Free_Box-Constrained_Diffusion_ICCV_2023_paper.html); [FreeControl](https://arxiv.org/html/2312.07536))

InstanceDiffusion binds descriptions to instance locations and addresses information leakage. DreamRenderer isolates selected cross-instance communication; its ablations show that completely separating instances can degrade results. UniCombine composes pretrained condition adaptations, and its stronger trained configuration improves some adherence measures while slightly reducing text scores. Accepting several conditions, matching them jointly, and changing one without affecting the others are progressively stronger claims. None follows automatically from adding more inputs. ([InstanceDiffusion](https://github.com/frank-xwang/InstanceDiffusion); [DreamRenderer](https://arxiv.org/html/2503.12885); [UniCombine](https://arxiv.org/html/2503.09277))

### Density, overlap, and fair inputs expose the difficult cases

CountGen improves counting but still fails many examples; its learned ReLayout component makes it more than prompt engineering. OverLayBench and InstanceAssemble identify overlap and dense layouts as stress regimes hidden by sparse examples. Similar-category objects make binding harder because semantic categories no longer supply easy identity cues. ConsistCompose addresses coordinate and identity consistency, while InstanceControl separates settings with and without instance labels. Oracle masks or labels are extra information, not an automatic pipeline’s equivalent input. Comparisons must retain that distinction. ([CountGen](https://openaccess.thecvf.com/content/CVPR2025/papers/Binyamin_Make_It_Count_Text-to-Image_Generation_with_an_Accurate_Number_of_CVPR_2025_paper.pdf); [OverLayBench](https://arxiv.org/html/2509.19282v1); [InstanceAssemble](https://arxiv.org/html/2509.16691v2); [ConsistCompose](https://github.com/opensensenova/consistcompose); [InstanceControl](https://arxiv.org/html/2606.31924))

Fairness also requires matching semantic information. A method given a style label and reference has more information than a reference-only method. Selecting the best among several outputs changes the comparison with single-shot sampling. Backbones, prompt rewriting, detector versions, preprocessing, and count of candidates often change together in published tables. Such comparisons can establish useful system performance without identifying which architectural mechanism caused the difference. ([RB-Modulation](https://arxiv.org/abs/2405.17401); [DiLightNet](https://arxiv.org/html/2402.11929v2))

### Incompatible conditions require priorities, not more guidance

An edge map can preserve a handle the prompt asks to remove. A normal map can describe a different camera view from the supplied projection. A monochrome style request can contradict explicit red/blue instance colors. Camera changes legitimately affect silhouette, occlusion, and shadows; material changes legitimately affect highlight shape. A useful specification distinguishes protected properties from permitted consequences rather than treating every changed pixel as collateral damage. These are feasibility questions before they are optimization questions.

The relevant research progression is input support → joint fidelity → paired selective intervention → robustness across content, seeds, magnitudes, and conflicting combinations. Much of the literature establishes the first two, with bounded evidence toward the third. A matched-noise pair reduces variance but does not prove factor independence. The structured-control note proposes explicit instance IDs, scopes, units, provenance, priorities, and uncertainty to make those distinctions testable; this synthesis does not adopt that proposal as an implementation architecture.

## 6. Editing requires a preservation contract

### Successful reconstruction does not imply a successful minimal edit

An edit has at least six possible preservation targets: pixels, geometry, identity, semantic content, perceptual appearance, and specifically protected non-target attributes. These targets disagree. Recoloring should change pixels while retaining shape; pose changes should alter projected geometry while retaining identity; relighting should alter shadows and reflections outside an object-only mask. A candidate that changes nothing can maximize similarity and fail the instruction completely. MasaCtrl and UniEdit-Flow directly demonstrate the trade-off between preservation and successful modification. ([MasaCtrl](https://arxiv.org/abs/2304.08465); [UniEdit-Flow](https://arxiv.org/abs/2504.13109))

The research contract should identify the requested change, protected information, direct action region, permitted secondary effects, and the precision of each guarantee. “Change only lighting” is not a sufficient contract: a global exposure operation, moved light, softened shadow, and illustrated rim convention are different actions. A moved object can require filling its old location, revealing background, and moving shadows. The complete influence region is not automatically its original silhouette. These distinctions are supported by the different tasks of EditBench, PIE-Bench, and GEditBench v2, rather than one interchangeable editing score. ([EditBench](https://arxiv.org/abs/2212.06909); [PnP Inversion/PIE-Bench](https://arxiv.org/abs/2310.01506); [GEditBench v2](https://arxiv.org/abs/2603.28547))

DDIM provides deterministic sampling and approximate finite-step reversal. SDEdit instead destroys some source information with noise and regenerates under a prior; greater freedom trades against faithfulness. Neither is exact recovery of a photograph’s historical generating noise. Null-text inversion improves reconstruction by optimizing unconditional embeddings around a pivot trajectory with fixed model weights. It is not network training, but it is per-image computation. Autoencoder artifacts, imperfect localization, and structural-edit difficulty remain. ([DDIM](https://arxiv.org/abs/2010.02502); [SDEdit](https://arxiv.org/abs/2108.01073); [Null-text inversion](https://arxiv.org/abs/2211.09794))

EDICT makes coupled transformations algebraically invertible in an enlarged state. Its exactness is not lossless original-pixel reconstruction through a lossy autoencoder, nor a proof of minimal change under a new prompt. ReNoise spends additional evaluations to improve numerical inversion estimates. PnP Inversion separates source reconstruction correction from target editing rather than constraining both branches identically. **PnP Inversion is the ICLR 2024 publication of the work circulated as Direct Inversion, arXiv:2310.01506; it is not an additional independent paper.** Plug-and-Play Diffusion Features, arXiv:2211.12572, is a different feature-injection work. The author-project BibTeX discrepancy identified in audit 12 is not propagated here. ([EDICT](https://arxiv.org/abs/2211.12446); [ReNoise](https://arxiv.org/abs/2403.14602); [PnP Inversion proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/661caac7729aa7d8c6b8ac0d39ccbc6a-Abstract-Conference.html); [Plug-and-Play features](https://arxiv.org/abs/2211.12572))

### Feature preservation and flow transport expose different trade-offs

Prompt-to-Prompt reuses cross-attention associated with text; Plug-and-Play reuses source spatial features and self-attention; MasaCtrl retrieves source information through attention while allowing target queries to evolve. These are stronger mechanisms than retaining a random seed, but copied features can contain the very color, geometry, or material to be changed. Overly extensive copying can reproduce the source instead of executing the edit. Localization, timestep, layer, and strength are therefore preservation–editability controls, not universal invariant switches. ([Prompt-to-Prompt](https://arxiv.org/abs/2208.01626); [Plug-and-Play features](https://arxiv.org/abs/2211.12572); [MasaCtrl](https://arxiv.org/abs/2304.08465))

RF-Inversion formulates controlled dynamics; RF-Solver improves numerical approximation and RF-Edit adds source feature reuse; FireFlow reuses velocity estimates and injects source information. FlowEdit avoids explicit source-to-noise inversion through direct source/target-conditioned transport. Its key insight is that an exactly reconstructing source→noise→target pairing can still be a poor edit pairing. UniEdit-Flow combines predictor–corrector inversion with region-adaptive editing. These advances address different errors; solver precision alone does not identify the correct semantic correspondence or complete preservation footprint. ([RF-Inversion](https://arxiv.org/abs/2410.10792); [RF-Solver](https://arxiv.org/abs/2411.04746); [FireFlow](https://arxiv.org/abs/2412.07517); [FlowEdit](https://arxiv.org/abs/2412.08629); [UniEdit-Flow](https://arxiv.org/abs/2504.13109))

Instruction-native editors learn a different input contract. InstructPix2Pix, Emu Edit, Kontext, and Qwen-Image can accept source context and instructions without asking the user to reconstruct a complete original prompt. That does not make source conditioning equivalent to inversion, or prove multi-turn stability. Autoregressive editors also retain reconstruction questions: VARIN pseudo-inverts discrete sampling to compatible noises, while VAREdit trains scale-aligned source conditioning. Perfect token reconstruction is not perfect raster reconstruction. The October 2026 ECT preprint’s “one evaluation” packs two conditions into one denoiser batch at one temporal support; it does not remove all branches, encoding, decoding, or architecture-specific assumptions. ([Emu Edit](https://arxiv.org/abs/2311.10089); [Kontext](https://arxiv.org/abs/2506.15742); [VARIN](https://arxiv.org/abs/2509.01984); [VAREdit](https://arxiv.org/abs/2508.15772); [ECT](https://arxiv.org/abs/2610.30827))

Explicit blending or final source compositing can guarantee equality outside its actual replacement support, subject to subsequent processing and encoding. A feathered mask expands that support, and a semantically incomplete mask can preserve the wrong information. A prompt, latent mask, or copied token is not the same guarantee. Blended Diffusion is important historical evidence that generative editing combined with explicit copying can offer stronger spatial guarantees than model-only preservation. ([Blended Diffusion](https://arxiv.org/abs/2111.14818))

### Repeated-edit failure has several supported causes

REED-VAE studies repeated autoencoding; FreqEdit preserves high-frequency information; VAE-LFA studies low-frequency latent drift; MT-OPSD adapts an editor to its own imperfect recursive inputs. These explanations concern different components, representations, and protocols. They are not interchangeable diagnoses of one universal failure. Strong historical alignment can suppress a legitimate global transformation; preserved fine detail can conflict with broad restyling; a no-op loop can expose drift without testing actual editing success. Teacher-forced clean-source tests, recursive sequences, inverse cycles, and persistent-constraint tasks must be reported separately. The targeted policy and transfer evidence in chapter 10 governs conclusions about which correction source to use. ([REED-VAE](https://arxiv.org/abs/2504.18989); [FreqEdit](https://arxiv.org/abs/2512.01755); [VAE-LFA](https://arxiv.org/abs/2605.08250); [MT-OPSD](https://arxiv.org/abs/2609.35611))

## 7. Physical and 3D assistance supply useful scaffolds

### An authored forward control is not a recovered physical fact

For a renderer, one can write \(I=\mathcal T(\mathcal R(G,M,L,C))\), where geometry, materials, lights, camera, and output processing are explicit. Inverse rendering instead fits explanations, typically through image loss plus a prior. Differentiability provides gradients; it does not establish uniqueness. The generalized bas-relief result proves nonuniqueness under its Lambertian, orthographic, illumination assumptions. Even \(I=A\odot S\) admits \((cA)\odot(S/c)\). More detailed residual layers do not uniquely identify reflectance, shading, specularity, emission, or grading from arbitrary stylized RGB. ([Bas-relief ambiguity](https://vision.ucsd.edu/publications/1999/bas-relief-ambiguity); [Mitsuba 2](https://rgl.epfl.ch/publications/NimierDavidVicini2019Mitsuba2))

Single-view estimates, posed multiview images, known-light captures, and calibrated transport bases supply different information. Different object cards are not multiview observations of one scene. Synthetic novel views generated from one illustration are additional hypotheses, not independent measurements of hidden surfaces. NeRFactor, TensoIR, and relightable Gaussian methods exploit inputs and priors absent from a single flattened card. Ordinary NeRF or 3D Gaussian radiance fitting is not automatically a factorized, relightable scene. ([NeRFactor](https://arxiv.org/abs/2106.01970); [TensoIR](https://arxiv.org/abs/2304.12461); [GS-IR](https://arxiv.org/abs/2311.16473); [IRGS](https://arxiv.org/abs/2412.15867))

Physical transport is linear in incident illumination for fixed geometry/materials before nonlinear output transforms; this supports OLAT combinations and physically informed data construction. It is not linear in light position, roughness, geometry, or tone-mapped RGB. LightLab and IC-Light use transport structure differently from a learned surrogate renderer. Claims of “physics” should specify whether they concern acquisition, loss constraints, synthetic training targets, explicit simulation, or the actual inference computation. ([LightLab](https://arxiv.org/abs/2505.09608); [IC-Light](https://github.com/lllyasviel/IC-Light); [DiffusionRenderer](https://arxiv.org/html/2501.18590))

### Intrinsic maps and proxies can structure an intervention despite errors

Intrinsic decomposition, normal/depth estimation, material buffers, and a coarse receiver plane can help organize shadows or highlights without being true scene recovery. A depth mesh is usually a visible-surface 2.5D proxy. It needs camera assumptions and cannot reveal unseen backsides or off-camera occluders. Normal and depth estimates can disagree or share errors. Marigold’s original CVPR2024 depth paper is separate from its 2025 expanded analysis preprint; the latter adds depth, normal, and intrinsic tasks without a verified journal venue in the saved record. ([Ordinal intrinsic decomposition](https://yaksoy.github.io/intrinsic/); [Original Marigold](https://arxiv.org/abs/2312.02145); [Expanded Marigold](https://arxiv.org/abs/2505.09358); [DSINE](https://github.com/baegwangbin/DSINE))

DiLightNet explicitly treats radiance hints as guidance rather than exact final rendering. RGB↔X and DiffusionRenderer expose appearance buffers, while PIXLRelight combines reconstruction, rendering, and learned compensation. Approximate geometry can therefore be useful because it structures the action, not because its dimensions are correct. But a fused object/background boundary can produce a semantically misplaced shadow, and a learned renderer cannot be assumed to repair any bad hint. PIXLRelight’s paper/card mismatch about the Marigold appearance checkpoint is preserved: the card documents albedo, roughness, and metallicity, not normals. An intended normal source must be resolved, not guessed. ([DiLightNet](https://arxiv.org/html/2402.11929v2); [RGB↔X](https://github.com/zheng95z/rgbx); [PIXLRelight](https://arxiv.org/abs/2605.18735); [checkpoint card](https://huggingface.co/prs-eth/marigold-iid-appearance-v1-1))

Material interventions are likewise operational rather than forensic. Alchemist trains relative material changes; Materialist uses physical optimization with priors; DiffReg-PBIR uses predicted material similarities as a regularizer rather than demanding that predictions be exact material targets. Roughness/source-size, reflectance/light-intensity, and geometry/material compensation remain coupled. A correct material change should alter highlights; requiring unchanged RGB would reject the intended physical response. ([Alchemist](https://arxiv.org/abs/2312.02970); [Materialist](https://arxiv.org/abs/2501.03717); [DiffReg-PBIR](https://arxiv.org/abs/2606.31065))

The useful project question is whether a primitive, corrected proxy, or richer reconstruction resolves an observed lighting/material failure better than simpler image-space controls. Floating-object cards may not need a receiver; environmental cards may need contact and occlusion. Authored geometry can amortize repeated variants, but one-off exaggerated objects can make cleanup more expensive than a localized correction. DiLightNet explicitly excludes some depiction regimes such as cel shading: physical light–matter assumptions are not automatically appropriate for graphic highlight conventions. This supports **selective scaffolding, not mandatory 3D conversion**. ([DiLightNet](https://arxiv.org/html/2402.11929v2))

## 8. NPR makes depiction decisions explicit

### Choosing a representation determines which artistic operations exist

NPR contributes more than filters resembling paint. Stroke systems expose count, path, width, opacity, placement, and layering; vectors expose region geometry and negative space; layered rasters can separate contours, shading, highlights, and texture; shaders expose tone ramps and view-dependent accents. Neural synthesis can generate rich appearance but need not expose those structures. Conversely, a learned method can output explicit strokes. “AI versus deterministic” is less useful than asking which decisions are represented, constrained, and editable. ([Hertzmann](https://mrl.cs.nyu.edu/publications/painterly98/hertzmann-siggraph98.pdf); [diffvg](https://people.csail.mit.edu/tzumao/diffvg/); [Stylized Neural Painting](https://openaccess.thecvf.com/content/CVPR2021/html/Zou_Stylized_Neural_Painting_CVPR_2021_paper.html))

Painterly construction separates mark appearance, directional field, allocation, and scale hierarchy. Hertzmann’s coarse-to-fine spline strokes expose approximation tolerances rather than simulate paint physically. A textured stamp cannot decide where a diagnostic accent belongs. Stylized Neural Painting retains parameterized marks while optimizing through a learned rendering surrogate; interpretable stroke parameters still do not recover an artist’s actual process. Watercolor simulation, by contrast, can model glazes, fluid behavior, and compositing, while a learned watercolor-like image need represent none of those causes. Both can be useful, with different controls and evidence requirements. ([Painterly rendering](https://mrl.cs.nyu.edu/publications/painterly98/hertzmann-siggraph98.pdf); [Watercolor](https://grail.cs.washington.edu/projects/watercolor/))

Hatching organizes lines around tone, form, and scale; halftoning distributes marks to encode tone; indication selectively depicts recurring texture instead of drawing it everywhere. Praun’s tonal art maps address viewing-scale coherence, while structure-aware halftoning optimizes a particular tone/structure objective. These are not interchangeable ways to “add texture.” Generic blur, noise, or uniform density reduction does not reproduce selective omission. Texture synthesis from finite exemplars also relies on local structure and coverage assumptions; matching a texture distribution on the wrong region remains wrong. ([Hatching](https://hhoppe.com/proj/hatching/); [Structure-aware halftoning](https://ttwong12.github.io/papers/structurehalftone/structurehalftone.html); [Pen-and-ink](https://grail.cs.washington.edu/projects/cg-illus/); [Efros–Leung](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/papers/efros-iccv99.pdf))

Cel/toon shading is not just color quantization. Tone-transition placement, contour policy, creases, highlight conventions, and motion emphasis contribute separately. Gooch shading deliberately prioritizes shape communication over exact albedo perception. Lit-sphere methods capture artistic shading through orientation; StyLit uses illumination guides to distinguish appearance contexts. Simulating media, using physical rendering as guidance, and producing material-like appearance are three different meanings of physically informed stylization. A convincing glossy painted highlight need not behave like a BRDF parameter. ([Lake et al.](https://markmark.net/npar/npar2000_lake_et_al.pdf); [Gooch](https://www.cs.princeton.edu/courses/archive/fall00/cs597b/papers/gooch98.pdf); [Lit Sphere](https://graphicsinterface.org/proceedings/gi2001/gi2001-17/); [StyLit](https://dcgi.fel.cvut.cz/publications/2016/fiser-tog-stylit))

### Abstraction and collection consistency need task-level evidence

Removing strokes, smoothing a contour, enlarging a handle opening, merging shading regions, and suppressing nondiagnostic texture are different abstraction operations. CLIPasso and CLIPascene supply semantic/geometric sketch optimization and separate simplicity/fidelity controls, but an icon can need fewer marks and stronger diagnostic shape simultaneously. XDoG exposes reproducible edge/tone transformations without knowing which contour identifies the collectible. Cole’s shape-interpretation studies do not establish that silhouette alone is universally sufficient; object and depiction type matter. ([CLIPasso](https://clipasso.github.io/clipasso/); [CLIPascene](https://clipascene.github.io/CLIPascene/); [XDoG](https://www.kyprianidis.com/p/cag2012/); [Shape interpretation](https://www.cs.princeton.edu/gfx/pubs/Cole_2009_HWD/cole_2009_hwd.pdf))

Recognition, local shape interpretation, visual search, memory, style fidelity, and attractiveness require different human tasks. A high-frequency background can attract an algorithm while a low-contrast subject is simplified away. McDougall’s icon norms distinguish complexity, familiarity, meaningfulness, and semantic distance. Neither an image-detail scalar nor a preference rank substitutes for finding and distinguishing assets at actual interface size. Enlarged inspections diagnose defects; they do not establish thumbnail usability. ([Winnemöller](https://cs.colby.edu/courses/S19/cs365/papers/winnemoller-videoAbstraction-SIG06.pdf); [Icon characteristics](https://pubmed.ncbi.nlm.nih.gov/10502873/))

Team Fortress 2’s production account coordinates silhouette, proportions, painterly texture, lighting warps, rim accents, and distance simplification. Its transferable principle is joint design of geometry, texture, and shading, not adoption of its look or a universal recognition threshold. IconGAN/AppIcon and GameTileNet offer genuine domain-relevant work, but application icons and top-down tiles differ from painted object cards. StyleAligned’s set studies and StyleShot’s benchmarks establish collection/reference precedents without validating gameplay recognition. Strong set similarity can reward duplicates or leaked reference motifs; a successful collection must remain consistent **and** content-diverse, identifiable, and discriminable. ([TF2 production paper](https://steamcdn-a.akamaihd.net/apps/valve/2007/NPAR07_IllustrativeRenderingInTeamFortress2.pdf); [IconGAN](https://github.com/architect-road/IconGAN); [GameTileNet](https://arxiv.org/abs/2507.02941); [StyleAligned](https://arxiv.org/abs/2312.02133); [StyleShot](https://arxiv.org/abs/2407.01414))

## 9. Agentic creation spans several different search problems

### Prompt search, image editing, programs, sampling, and training are distinct

Idea2Img supplies early generate/select/critique/revise prior art. Promptist learns prompt adaptations through training; VisualPrompter revises descriptions using observed omissions; preference elicitation asks people to clarify a target. Regenerating from revised text can improve alignment without retaining an earlier successful image detail. Keeping a sentence unchanged is weaker than keeping its corresponding pixels, shape, or identity unchanged. DPO-Diff is discrete prompt optimization, not direct preference optimization: its ability to improve or adversarially worsen outputs demonstrates dependence on the chosen objective rather than an intrinsic art-quality guarantee. ([Idea2Img](https://arxiv.org/html/2310.08541v2); [Promptist](https://papers.nips.cc/paper_files/paper/2023/hash/d346d91999074dd8d6073d4c3b13733b-Abstract-Conference.html); [VisualPrompter](https://arxiv.org/html/2506.23138v1); [DPO-Diff](https://arxiv.org/html/2407.01606v1))

GenArtist, CoSTA*, and RefineEdit-Agent provide tool decomposition, planning, verification, and replanning precedents. MIRA instead trains an atomic editing/termination policy through supervised and reward-based learning. The reconciled citation is **CVPR Findings 2026**, with a 2025 preprint; a zero-shot reimplementation in another paper is not the released or trained policy. MIRA’s own metrics are mixed, with some semantic/alignment gains and a perceptual-quality decline in the audited table. Learned stopping or a deeper reasoning trace is not automatic convergence. ([GenArtist](https://arxiv.org/html/2407.05600); [CoSTA*](https://arxiv.org/html/2503.10613); [RefineEdit-Agent](https://arxiv.org/html/2508.17435); [MIRA proceedings](https://openaccess.thecvf.com/content/CVPR2026F/html/Zeng_MIRA_Multimodal_Iterative_Reasoning_Agent_for_Image_Editing_CVPRF_2026_paper.html))

Procedural editing is different again. MonetGPT and IEA predict interpretable retouching operations; JarvisEvo mixes generative editing and professional operations. Changing a program and rerendering the same source can avoid recursively damaging a raster, but only within the operation vocabulary. IEA’s sixteen-operation global environment does not solve arbitrary local semantic editing. Its leave-one-operation-out usefulness objective is direct intervention evidence for that environment, not proof of a general controller over artistic concepts. JarvisEvo’s internal evaluator is grounded through human scores; “self-evaluation” does not mean independent truth emerges from self-approval. ([MonetGPT](https://arxiv.org/html/2505.06176); [IEA](https://arxiv.org/html/2606.08016); [JarvisEvo](https://arxiv.org/html/2511.23002))

### Optimization evidence must actually concern images and the available action space

BayesGenie applies Bayesian optimization to image/text guidance scales while an LLM helps instructions and evaluation. Optimize Your Sampling tunes diffusion schedules; EvoSearch selects and mutates denoising states; verifier-threshold work allocates inference computation. These are demonstrated image-domain applications, but optimize different variables with different access requirements. If prompts change while BO models only two guidance coefficients, the objective can become nonstationary. This is an analytical caution about the formulation, not a measured failure or proof that BO cannot help. ([BayesGenie](https://arxiv.org/html/2502.18116v1); [Optimize Your Sampling](https://arxiv.org/html/2608.18040v1); [EvoSearch](https://arxiv.org/html/2505.17618); [Verifier-Threshold](https://arxiv.org/html/2512.08985v2))

BanditRewriter is an actual image-prompt publication, but the saved inspection did not establish enough full-text detail for numerical claims. Generative active learning for image personalization selects informative queries for learning, not necessarily the next corrective edit. The multiobjective prompt-bandit paper discussed in note 08 evaluates summarization and is not counted as image validation. A finite-difference response matrix or coordinate-wise search over explicit continuous operations is a plausible research baseline; it is not automatically meaningful for discrete prompt substitutions, changing masks, or different seeds. No inspected source establishes a globally convergent Jacobian controller for the proposed style ontology. ([BanditRewriter record](https://ieeexplore.ieee.org/document/11209841); [Image personalization active learning](https://arxiv.org/abs/2403.14987); note 08)

## 10. Correction policy depends on what must survive

### Four task regimes explain the apparent sequential-versus-parallel conflict

From-scratch composition has no approved raster to preserve. Faithful editing begins with one. Dependent accepted edits create a legitimate new state that later steps must retain. Parameter-program editing can rerender the original source instead of processing the latest raster. These are different problems, and their budgets and preservation objectives cannot be collapsed into “iteration works” or “parallel always wins.” The targeted correction-strategy audit supplies the controlling comparison.

| Study and regime | Reported result | What was actually controlled |
|---|---|---|
| Iterative Refinement, difficult ConceptMix generation | At seven bindings, parallel 49.6%, pure iterative 64.3%, mixed 66.5% all-correct | Declared sixteen image calls; not demonstrated equality of complete judge and wall-clock cost. |
| EditAgent, faithful source editing | 102 parallel preferences,28 sequential preferences,14 ties across 144 requests | At most four image candidates; different feedback schedules and judge-call ceilings. |
| IEA, procedural retouching | Operation programs rerender the same source | A restricted global editing environment, not arbitrary image regeneration. |
| MT-OPSD, recursive robustness | Learned adaptation substantially improves cumulative success in its benchmark | Changes editor weights through training; not an untuned orchestrator comparison. |

The Iterative Refinement mixed-versus-parallel difference is **16.9 percentage points**, not a relative percentage gain. Its strongest action space includes backtracking, restarting, stopping, and continuing, not compulsory use of the latest image. Its human-study and implementation descriptions contain budget/model-name ambiguities retained in audit 11. Gains support compositional correction in tested settings, not a universal best recursive policy. ([Iterative Refinement results](https://arxiv.org/html/2601.15286#S4))

EditAgent’s 102/130 decided comparisons yield **78.5%**; 102/144 yields **70.8% of all requests**. Its sequential baseline can select an earlier candidate, so its loss is not simply returning a final damaged image. Nevertheless, the experiment changes source conditioning, feedback schedule, batch comparison, and acceptance-dependent termination together. The entire difference cannot be causally assigned to anchoring alone. That is this synthesis’s design assessment, not a quoted author concession. ([EditAgent policy comparison](https://arxiv.org/html/2610.39664#S2a))

Production EditAgent is a hybrid: an accepted step becomes the source for the next dependent step; retries branch from that step’s source; a version graph retains accepted history and can trigger repair. It is not globally reset to the original and not universally parallel. A best-accepted-checkpoint branch is a meaningful additional baseline not isolated in that particular comparison. Visual Jenga’s feedback-guided removal retries also show that faithful editing can benefit from better instructions without requiring repeated damage to a failed raster. ([EditAgent workflow](https://arxiv.org/html/2610.39664#S4a); [Visual Jenga](https://arxiv.org/html/2601.15286#S4))

### Numerical records help as a bundle; their isolated causal value remains open

EditAgent’s records include pixel-change statistics, difference maps, matched close-ups, color/lightness summaries, structure/framing checks, and construction assertions. Its ΔE threshold and clipping rules are implementation definitions, not universal perceptual or release thresholds. For fixed candidate sets, Qwen3.8-27B selection accuracy changes from 71.6% pointwise to 73.6% listwise without records and 81.3% with records. The evaluated denominator is 515 usable sets, after exclusions, not all 600. Expert labels are one joint consensus by five professionals, not five independent annotations. ([EditAgent diagnostic evaluation](https://arxiv.org/html/2610.39664#S4); [record definitions](https://arxiv.org/html/2610.39664#S6a))

This is direct evidence that an enriched record package can improve judgment, especially on subtle photometric and enhancement differences. It is not evidence that numbers alone cause the gain. **No number-only, map-only, crop-only, shuffled-number, or counterfactual-record ablation was established.** Candidate-order shuffling is a different control. Some records include verified/to-judge statements, and failed construction checks can remove candidates before judgment. An appearance statistic does not identify the physical cause or guarantee coverage of brushwork, shape language, expression, or hierarchy. ([EditAgent appendices](https://arxiv.org/html/2610.39664#S3a))

Some complete-system comparisons reuse a judge family internally and externally. Changing the internal judge while leaving final scoring fixed is not a wholly independent external replication. Likewise, fewer judge calls in the small policy comparison do not make the complete agent cheaper than a standalone editor: reported aggregate H100 GPU-hours are substantially higher. Total image calls, actual candidates, judge calls, tokens, preprocessing, wall time, memory, and upstream training belong in separate cost fields. ([EditAgent evaluation and cost](https://arxiv.org/html/2610.39664#S5); [judge ablation](https://arxiv.org/html/2610.39664#S7))

### Drift interventions transfer unevenly

FreqEdit’s original results improve some preservation/quality measures while slightly reducing instruction following. MT-OPSD later reports lower long-horizon success after adding FreqEdit on its mixed global/local benchmark. This is consequential negative transfer evidence, not an audited exact reproduction of the original checkpoint/settings: tasks, backbones, and some hyperparameters differ. VAE-LFA improves some consistency measurements while suppressing intended global edits or lowering another composite score. Multiple causes of drift and task-dependent trade-offs are therefore better supported than a single fundamental cause with a universal cure. ([FreqEdit](https://arxiv.org/html/2512.01755v2#S5); [MT-OPSD](https://arxiv.org/html/2609.35611#S4); [VAE-LFA](https://arxiv.org/html/2605.08250#S5))

## 11. Evaluation must distinguish ranking from release acceptance

### Correctness, style, preservation, defects, appeal, and usability are different constructs

A beautiful output can have the wrong count; a faithful style match can be less attractive; a preserved source can fail to change; a good preview can be unusable at card size. Holistic evaluation such as HEIM supplies established multidimensional precedent. For reference transfer, the relevant input is often content/reference/output together. For editing it is source/instruction/candidate, plus protected properties and history. A global CLIP or style embedding score cannot stand in for all of these observations. ([HEIM](https://arxiv.org/abs/2311.04287); [ASTRA](https://arxiv.org/html/2610.10003v1); [EdiVal](https://arxiv.org/html/2509.13399v3))

GenEval tests explicit object properties; TIFA uses prompt-derived questions; DSG adds semantic dependencies; CompBench and its expanded journal version combine several categories and evaluators. Their question sets, detectors, relation rules, and aggregation all define what is measured. A missing object can invalidate dependent questions, but a better dependency graph does not cure VQA perception errors. The original conference and expanded CompBench++ records are related versions with different scope, not one invariant benchmark configuration. ([GenEval](https://arxiv.org/abs/2310.11513); [TIFA](https://arxiv.org/abs/2303.11897); [DSG](https://arxiv.org/abs/2310.18235); [CompBench++](https://arxiv.org/abs/2307.06350v3))

GenEval 2 provides direct drift evidence: its audit collected 23,226 human annotations and found automatic/human deviations up to 17.7 percentage points. Valid holes, perspective, and “under a table” relations can confuse color masks or box rules. This need not mean contamination or deliberate gaming; the generated distribution changed while the evaluator’s assumptions did not. Strong atom-level performance also coexists with much lower complete-prompt success. Soft-TIFA probabilities and geometric means are not calibrated release probabilities. The verified GenEval 2 record is **December 2025 v1**, not a new 2026 revision inferred from rendered-document dates. ([GenEval 2](https://arxiv.org/html/2512.16853v1); [submission record](https://arxiv.org/abs/2512.16853))

### Human-aligned metrics remain protocol- and population-dependent

ASTRA’s triplet evaluation is unusually relevant to style transfer, but its 864 outputs derive from six contents and twelve styles, not 864 independent source families. Leave-one-method-out tests familiar references with new methods; leave-content/style-out tests different generalization. Its style agreement is imperfect, and ranking correlations do not establish low false acceptance for card production. CSD is a style-retrieval representation with an unresolved official released-weight discrepancy warning. MIT code, CC BY 4.0 checkpoint metadata, and a performance warning are compatible facts about different components; none should be silently discarded. ([ASTRA](https://arxiv.org/html/2610.10003v1); [CSD repository](https://github.com/learn2phoenix/CSD); [checkpoint](https://huggingface.co/tomg-group-umd/CSD-ViT-L))

PickScore, HPS, and ImageReward model preferences from particular populations and collection processes. A model that predicts those choices well has not demonstrated superior art direction or compliance with a client’s style brief. LPIPS measures validated perceptual similarities in its studied tasks, not survival of every tiny protected marking. RichHF’s localized feedback is diagnostically valuable, but its public reproduction differs from the original implementation. Gecko and human-evaluation methodology show that holistic, word-level, question-based, absolute, and pairwise protocols can yield different agreement. The question posed to raters is part of the target, not an incidental interface choice. ([Pick-a-Pic](https://arxiv.org/abs/2305.01569); [HPSv2](https://github.com/tgxs002/HPSv2); [ImageReward](https://arxiv.org/abs/2304.05977); [LPIPS](https://openaccess.thecvf.com/content_cvpr_2018/html/Zhang_The_Unreasonable_Effectiveness_CVPR_2018_paper.html); [RichHF](https://github.com/youweiliang/RichHF); [Gecko](https://arxiv.org/abs/2404.16820); [human-evaluation methodology](https://arxiv.org/abs/2304.01816))

PIE-Bench, EditBench, MagicBrush, ImgEdit, GEditBench v2, and EdiVal cover different editing units and targets. Human-assisted targets are not necessarily hand-painted unique ground truth, and one valid edit can differ from the selected target. EdiVal’s object-centric consistency is not comprehensive style validation. Multi-turn SR@k can mean every turn through k passes, not simply a satisfactory final image. Source counts, prompts, generated candidates, turns, annotators, votes, and regions must remain separate sample units. ImgEdit’s one-million versus 1.2-million training-pair statements remain attributed source/version differences, not harmonized benchmark test counts. ([MagicBrush](https://arxiv.org/abs/2306.10012); [ImgEdit](https://arxiv.org/abs/2505.20275); [GEditBench v2](https://arxiv.org/abs/2603.28547); [LME-Bench](https://huggingface.co/datasets/metazlb/LME-Bench))

### Release decisions require error rates and independent evidence

If \(Y=1\) denotes human-adjudicated acceptability and \(A=1\) automatic acceptance, then \(P(A=1\mid Y=0)\), \(P(A=0\mid Y=1)\), and \(P(Y=0\mid A=1)\) answer different questions. The last depends on deployment prevalence. Spearman correlation, AUROC, inter-rater agreement, and model-level ranking do not supply these operating-point errors. An abstention/review policy must report coverage as well as mistakes. No numerical acceptance cutoff or universal agreement threshold is justified by this corpus for the project. These are analysis principles developed explicitly in note 07, not measured project results.

Independent source families should define splits, not near-duplicate crops or turns. Preserve paired comparisons and asset/annotator dependence; retain ties and disagreements. Calibration and final evaluation must remain separate. Judge audits should swap order, change equivalent rubrics, hide model identities, remove evidence, and test deliberately wrong bindings or protected details. These are proposed card-domain controls, not assertions that every bias is measured identically in existing studies. Multimodal-judge studies motivate them, while reward-hacking evidence shows why optimizing one score can damage other dimensions. Required outcomes do not mandate restricted or uncleared named evaluators. ([MM-JudgeBias](https://aclanthology.org/2026.acl-long.1162/); [Reward hacking](https://arxiv.org/html/2601.03468v2); record reconciliation)

## 12. Artifact readiness is separate from scientific relevance

### Reuse, new training, and complete reproduction are different commitments

| Evidence category | Examples and bounded reuse opportunity | Unresolved obligation |
|---|---|---|
| Explicit operations without new learned weights | Mask geometry, color-managed statistics, paths, constructive shading or texture | Validate region definitions, perceptual meaning, and intervention suitability. |
| Inference over pretrained components | StyleStudio, StyleAligned, image adapters, some inversion/feature methods | Pin compatible base models, dependencies, references, and settings; check terms. |
| Existing learned actuator | Released Concept Sliders or particular prepared adaptations | Verify its actual effect, surrounding interference, and checkpoint rights. |
| New task/style adaptation | DreamBooth/LoRA, custom Concept Sliders, StyleBlend | Prepare examples, supervision, regularization, training, and held-out tests. |
| Discovery with upstream computation | New SliderSpace directions | Sampling, embedding analysis, adapter training, naming, and local calibration. |
| Specialized appearance system | Artist-Inator and NPR gloss pipeline | Checkpoints, local-path/configuration repair, data mappings, dependency and rights review. |
| Research method without complete verified release | Original StyleDrop stack; some recent agent/control methods | Do not treat a project page or promised release as an executable reproduction. |
| Evaluator with artifact caveat | CSD warning; RichHF reproduction; GenEval 2 restriction | Separate scientific evidence from actual checkpoint behavior and permitted use. |

The table describes research options, not selected software. Artifact evidence ranges from an existing repository, through an inspected inference path and checkpoint listing, to a reproduced paper result. Those are separate milestones. ArtAdapter’s forthcoming status, incomplete UniCSG task releases, public-subset/full-corpus differences, and author reimplementations illustrate why availability must be stated precisely. “Not verified” is not equivalent to nonexistent. ([ArtAdapter](https://github.com/cardinalblue/ArtAdapter); [UniCSG](https://github.com/Jankinwei/UniCSG); [OmniStyle](https://github.com/StyleX-Research/OmniStyle); [InstanceDiffusion](https://github.com/frank-xwang/InstanceDiffusion))

Code, base weights, task weights, data annotations, source imagery, and third-party dependencies require separate permission records. CSD’s component distinctions are resolved bibliographically but its weight-performance warning is not. StyleShot and DEADiff retain scope ambiguities between permissive metadata and restrictive language. GPLv3 normally permits commercial use subject to its terms; the Zaragoza repositories’ additional commercial-contact wording requires clarification, not automatic reclassification as noncommercial. RAIL is not a synonym for noncommercial. Unknown rights are **not cleared**, not proof of a particular restriction. Mandatory correctness or style outcomes do not mandate running a restricted evaluator. ([CSD](https://github.com/learn2phoenix/CSD); [StyleShot](https://github.com/open-mmlab/StyleShot); [DEADiff](https://github.com/bytedance/DEADiff); [NPR gloss code](https://github.com/SantiagoJN/npr_gloss_disent); record audit)

### CPU and consumer AMD feasibility remain an empirical gap

No reviewed complete learned pipeline was demonstrated here on the RX 7900 XTX 24 GB, ROCm, and CachyOS environment. NVIDIA timings and VRAM figures are not transferable benchmarks; small adapter files do not imply small training memory. Activations, optimizer state, multiple contexts, auxiliary models, precision, attention implementations, and concurrency matter. A CUDA-oriented example neither proves incompatibility nor certifies ROCm operation. Verifier-Threshold’s AMD MI300X result is genuine AMD evidence but not consumer-card validation. ([Verifier-Threshold](https://arxiv.org/html/2512.08985v2); hardware boundaries in note 04)

Blender documents CPU rendering and Linux HIP support for Radeon RX 7000 hardware; Mitsuba’s documented CPU and NVIDIA GPU backends are different. CPU support for one renderer or estimator does not establish useful complete-pipeline latency. Proxy preparation, model loading, intrinsic estimation, rendering, selection, and manual corrections must accompany any future runtime claim. A fast learned relighting forward pass is not a fast cold-start reconstruction/relighting workflow. No installation or software-selection decision follows from this report. ([Blender GPU documentation](https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html); [Mitsuba3](https://github.com/mitsuba-renderer/mitsuba3))

## 13. A research program should isolate information and intervention value

### Begin with observable appearance and explicit nuisance controls

The immediate objective should be an interpretable experiment, not a universal style engine. A small initial vocabulary can include reviewed subject occupancy and margins, regional lightness/chroma, an explicit palette assignment, background detail allocation, and suitable boundary-transition measurements. These are candidates because their image evidence can be specified; they are not universally sufficient style descriptors. Masks, crop, profile, scale, and uncertainty belong to each measurement. Learned segmentation followed by exact area calculation remains a learned estimate followed by conditional arithmetic. The companion [measurement volume](measuring-visual-style.md) provides the fuller axis-specific contracts rather than duplicating every formula here.

Controlled fixtures should have known masks, layers, operation histories, or authored scene parameters. Their purpose is to test whether a measurement detects the intended manipulation and rejects nuisance changes. Palette transfer with a fixed mask, occupancy changes with recorded transforms, and controlled tone/edge perturbations create different tests from arbitrary generated failures. Include resampling, noise, compression, contrast, and object-content changes to expose false interpretations. A texture statistic that mostly tracks mask boundary or scale is not yet a useful rendering-style diagnostic. These experiments are proposals from the source notes, not completed benchmarks.

The real-artwork arm must then test transfer. Hold out object families and reference sources, distinguish floating from grounded/environmental categories, and separate same-content appearance comparisons from cross-content style comparisons. A reference can provide palette, material depiction, contour, identity, or layout; those roles should be explicit. An unrelated object copying the reference silhouette is not a success simply because whole-image similarity rose. Original-resolution references remain necessary for fine stroke, texture, and small-detail claims, but their pending availability is not a reason to postpone conceptual definitions or controlled tests. (Style/representation evidence; reference applicability)

### Calibrate actuator response before asking a controller to invert it

For explicit continuous controls, a local response estimate can be written

\[
J_{ij}(I,u)\approx
\frac{m_i(F(I,u+\delta e_j))-m_i(F(I,u))}{\delta}.
\]

This is a **proposed empirical diagnostic**, not a validated universal style Jacobian. Its diagonal asks whether the actuator affects the intended measurement; off-diagonal terms expose collateral response. Repeat across contents, seeds, magnitudes, categories, and processing scales. Nonmonotonicity, saturation, hysteresis across edit histories, and uncertainty are results to record rather than nuisances to hide. A text replacement or changing mask is a discrete intervention, not automatically a differentiable coordinate. There is no presumption that the matrix is invertible or that diagonalization yields artistically coherent combinations. ([Concept Sliders](https://arxiv.org/html/2311.12092); [SliderSpace](https://arxiv.org/html/2502.01639); control proposals in note 04)

Separate diagnosis from action. First ask whether the named property is actually outside the target, then whether the selected tool can affect it, then whether the resulting change preserves protected requirements. A good final image does not prove correct causal diagnosis. Fix critique while varying tools, fix tools while varying critique, and remove the allegedly useful operation. For numeric actions compare simple sweeps, random search, coordinate-wise search, and BO where their assumptions fit. Added complexity should be justified by measured information or intervention value, not its resemblance to control theory.

### Compare correction sources and feedback packages under complete budgets

The policy experiment should separate from-scratch composition, subtle appearance correction, local semantic edits, and broad global transformations. Compare one-shot generation, best-of-N selection, prompt revision without visual feedback, feedback-guided regeneration, latest-output sequential editing, preserved-source candidates, best-accepted-checkpoint branching, and source-rerendered parameter programs where the same task is expressible. Report image-call ceilings and realized calls separately; include generator evaluations, critic/judge tokens, auxiliary inference, end-to-end latency, peak memory, human effort, and any training. Equal image counts alone cannot establish equal expenditure. ([Iterative Refinement](https://arxiv.org/html/2601.15286); [EditAgent](https://arxiv.org/html/2610.39664); [IEA](https://arxiv.org/html/2606.08016))

Feedback ablations should distinguish images alone, matched crops, maps, numbers, construction checks, and the full record. Add shuffled, sign-reversed, or otherwise counterfactual numbers while holding images, presentation, text length, and candidate order fixed. Do not confuse candidate-order shuffling with evidence-correctness shuffling. If the policy ignores changed measurements, the numbers can be decorative; if false numbers redirect actions, their influence is real but their trust calibration still needs examination. Measure independent target success and protected-property failure, not only the policy’s explanation or internal score. This is the principal causal gap identified by audit 11, not an experiment already performed by EditAgent.

Adapted editors and orchestration policies should also be crossed rather than conflated. A robustness-trained backend can make a weak strategy appear stronger; a better tool can rescue an inaccurate critic. Conversely, an accurate diagnosis cannot reach an unavailable edit. This distinction makes negative results useful: failure can identify an unobservable property, an unreachable constraint combination, or an evaluator mismatch rather than merely “the agent needs more reasoning.”

### Acceptance, abstention, and stopping are separate research outcomes

Human evaluation should separately ask about required content, protected identity/parts, reference-family membership, release-relevant defects, and actual-size recognition. Keep general appeal as another question. Some judgments should remain unavailable to the optimizer. Include wrong-count/right-style cases, excellent-preservation/no-edit cases, leaked reference content, tiny protected-detail loss, valid nonphotorealistic deformation, and already-correct images that should not be edited. The latter tests unnecessary action and stopping rather than rewarding perpetual activity. (Evaluation design)

Predeclare what constitutes accepted progress, protected regression, oscillation, insufficient observable evidence, contradictory requirements, unavailable controls, and budget exhaustion. Preserve the original and accepted states, but do not anchor every property to the original after valid dependent edits. Stopping is justified when evidence no longer shows progress, the request is infeasible, protected failures recur, or the budget ends—not because a judge says “looks good” without independent checks. Practical margins and thresholds require art-direction decisions and calibration; none is supplied here.

The contribution would be a documented control/evaluation frontier: which appearance changes are detectable, which actions realize them, which invariants survive, and at what total cost. Generic agents, decomposition, reference conditioning, measurement-rich records, and rollback are established prior art. A category-conditioned benchmark and calibrated production method can still be valuable engineering or research. Novelty and effectiveness of the particular combination remain open until demonstrated against those precedents.

## Conclusion

The useful shift is from a universal latent-style hypothesis to an **evidence-bearing intervention contract**. Artistic language supplies intent; reviewed pixels and annotations supply observations; models supply conditional proposals; explicit programs supply narrower guarantees; and independent human tasks decide whether the result serves its purpose. None of these channels should inherit the authority of another merely because they share an attribute name.

The proposed approach remains worth investigating because the gap is concrete: reliable reference-compatible changes that preserve important content under realistic cost and ambiguity. The literature supplies enough machinery to test that gap, but not enough evidence to preselect an architecture or claim it solved. The decisive advance would be measured selectivity and constrained acceptance on meaningful assets, with failures, uncertainty, and artifact limits left visible.

## Curated paper index

This index is a reading route, not a new search result or leaderboard. **Priority A** means central to the control/validity argument; **B** broadens mechanisms or supplies a useful comparator; **C** is specialized or current work to read after its prerequisites. Priorities are editorial, not quality scores. Each row identifies one work; aliases are merged, while genuinely separate publications remain distinct. The broader ledgers and artifact qualifications remain in the source notes. Publication status is bounded by what those notes verified, not inferred from present-day badges.

The curated index contains **110 distinct works**. This is an editorial selection from overlapping note ledgers, not a count of independent replications, unique URLs, or all papers consulted.


### Generation foundations

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P001 | B | [Generative Adversarial Nets](https://arxiv.org/abs/1406.2661); 2014; NeurIPS 2014, peer-reviewed |
| P002 | B | [A Style-Based Generator Architecture for Generative Adversarial Networks](https://arxiv.org/abs/1812.04948); 2019; preprint 2018; CVPR 2019, peer-reviewed |
| P003 | A | [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239); 2020; NeurIPS 2020, peer-reviewed |
| P004 | B | [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456); 2021; preprint 2020; ICLR 2021, peer-reviewed |
| P005 | A | [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752); 2022; preprint 2021; CVPR 2022, peer-reviewed |
| P006 | B | [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598); 2022; workshop version 2021; NeurIPS workshop/preprint, not main-conference evidence |
| P007 | B | [Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748); 2023; preprint 2022; ICCV 2023, peer-reviewed |
| P008 | A | [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747); 2023; preprint 2022; ICLR 2023, peer-reviewed |
| P009 | B | [Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003); 2023; preprint 2022; ICLR 2023, peer-reviewed |
| P010 | B | [Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206); 2024; ICML 2024, peer-reviewed |
| P011 | B | [Consistency Models](https://arxiv.org/abs/2303.01469); 2023; ICML 2023, peer-reviewed |
| P012 | B | [Improved Distribution Matching Distillation for Fast Image Synthesis](https://arxiv.org/abs/2405.14867); 2024; NeurIPS 2024, peer-reviewed |
| P013 | B | [Mean Flows for One-step Generative Modeling](https://arxiv.org/abs/2505.13447); 2025; NeurIPS 2025, peer-reviewed |
| P014 | B | [Taming Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2012.09841); 2021; preprint 2020; CVPR 2021, peer-reviewed |
| P015 | B | [MaskGIT: Masked Generative Image Transformer](https://arxiv.org/abs/2202.04200); 2022; CVPR 2022, peer-reviewed |
| P016 | B | [Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction](https://arxiv.org/abs/2404.02905); 2024; NeurIPS 2024, peer-reviewed |
| P017 | A | [Autoregressive Image Generation without Vector Quantization](https://arxiv.org/abs/2406.11838); 2024; NeurIPS 2024, peer-reviewed |
| P018 | B | [NextStep-1: Toward Autoregressive Image Generation with Continuous Tokens at Scale](https://arxiv.org/abs/2508.10711); 2026; preprint 2025; ICLR 2026, peer-reviewed |
| P019 | B | [Qwen-Image Technical Report](https://arxiv.org/abs/2508.02324); 2025; Technical report/preprint |
| P020 | B | [UniReason 1.0: A Unified Reasoning Framework for World Knowledge Aligned Image Generation and Editing](https://arxiv.org/abs/2602.02437); 2026; Preprint |

### Style representation and transfer

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P021 | B | [A Neural Algorithm of Artistic Style](https://arxiv.org/abs/1508.06576), 2015-08-26; preprint, preceding the CVPR 2016 development |
| P022 | A | [Controlling Perceptual Factors in Neural Style Transfer](https://openaccess.thecvf.com/content_cvpr_2017/html/Gatys_Controlling_Perceptual_Factors_CVPR_2017_paper.html), 2017; CVPR |
| P023 | B | [Arbitrary Style Transfer in Real-time with Adaptive Instance Normalization](https://arxiv.org/abs/1703.06868), 2017-03-20; ICCV 2017 |
| P024 | B | [Universal Style Transfer via Feature Transforms](https://arxiv.org/abs/1705.08086), 2017-05-23; NeurIPS 2017 |
| P025 | B | [ALADIN: All Layer Adaptive Instance Normalization for Fine-grained Style Similarity](https://arxiv.org/abs/2103.09776), 2021-03-17; ICCV 2021 |
| P026 | B | [Measuring Style Similarity in Diffusion Models](https://arxiv.org/abs/2404.01292), 2024-04-01; ECCV 2024 |
| P027 | A | [Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations](https://proceedings.mlr.press/v97/locatello19a.html), 2019; ICML |
| P028 | B | [Self-Supervised Learning with Data Augmentations Provably Isolates Content from Style](https://proceedings.neurips.cc/paper/2021/hash/8929c70f8d710e412d38da624b21c3c8-Abstract.html), 2021; NeurIPS |
| P029 | A | [IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models](https://arxiv.org/abs/2308.06721), 2023-08-13; preprint/released method |
| P030 | B | [StyleDrop: Text-to-Image Synthesis of Any Style](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d33b177b69425e7685b0b1c05bd2a5e4-Abstract-Conference.html), 2023; NeurIPS |
| P031 | B | [Style Aligned Image Generation via Shared Attention](https://arxiv.org/abs/2312.02133), 2023-12-04; CVPR 2024 |
| P032 | B | [Style Injection in Diffusion: A Training-free Approach for Adapting Large-scale Diffusion Models for Style Transfer](https://arxiv.org/abs/2312.09008), 2023-12-11; CVPR 2024 |
| P033 | B | [InstantStyle: Free Lunch towards Style-Preserving in Text-to-Image Generation](https://arxiv.org/abs/2404.02733), 2024-04-03; preprint |
| P034 | B | [Implicit Style-Content Separation using B-LoRA](https://arxiv.org/abs/2403.14572), 2024-03-21; ECCV 2024 |
| P035 | A | [StyleBlend: Enhancing Style-Specific Content Creation in Text-to-Image Diffusion Models](https://arxiv.org/abs/2502.09064), 2025-02-13; Eurographics/Computer Graphics Forum 2025 |
| P036 | A | [StyleStudio: Text-Driven Style Transfer with Selective Control of Style Elements](https://arxiv.org/abs/2412.08503), 2024-12-11; CVPR 2025 |
| P037 | B | [StyleShot: A Snapshot on Any Style](https://doi.org/10.1109/TPAMI.2025.3610614); 2024 preprint, 2025 revision; TPAMI 48(2), February 2026. First-online date unverified. |
| P038 | B | [StyleGallery: Training-free and Semantic-aware Personalized Style Transfer from Arbitrary Image References](https://openaccess.thecvf.com/content/CVPR2026/html/He_StyleGallery_Training-free_and_Semantic-aware_Personalized_Style_Transfer_from_Arbitrary_Image_CVPR_2026_paper.html); CVPR 2026, proceedings-confirmed. Not StyleShot’s dataset. |
| P039 | B | [SCFlow: Implicitly Learning Style and Content Disentanglement with Flow Models](https://arxiv.org/abs/2508.03402), 2025-08-05; ICCV 2025 |
| P040 | B | [UniCSG: Unified High-Fidelity Content-Constrained Style-Driven Generation via Staged Semantic and Frequency Disentanglement](https://arxiv.org/abs/2604.17850), 2026-04-20; [ECCV 2026](https://eccv.ecva.net/virtual/2026/poster/4742) |
| P041 | B | [CLeaR: A Unified Framework for Resolving the Leakage–Degradation Dilemma in Style Transfer](https://arxiv.org/abs/2609.38136), 2026-09-29; preprint, repository conference claim unverified |

### Adaptation and learned actuators

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P042 | B | [An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion](https://arxiv.org/abs/2208.01618); 2022, ICLR 2023 |
| P043 | A | [DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242); 2022/2023, CVPR |
| P044 | B | [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685); 2021/2022, ICLR |
| P045 | B | [Multi-Concept Customization of Text-to-Image Diffusion](https://arxiv.org/abs/2212.04488); 2022/2023, CVPR |
| P046 | B | [Key-Locked Rank One Editing for Text-to-Image Personalization](https://arxiv.org/abs/2305.01644); 2023, SIGGRAPH |
| P047 | B | [Controlling Text-to-Image Diffusion by Orthogonal Finetuning](https://arxiv.org/abs/2306.07280); 2023, NeurIPS |
| P048 | B | [ZipLoRA: Any Subject in Any Style by Effectively Merging LoRAs](https://arxiv.org/abs/2311.13600); 2023/2024, ECCV |
| P049 | B | [UnZipLoRA: Separating Content and Style from a Single Image](https://arxiv.org/abs/2412.04465); 2024/2025, ICCV Highlight |
| P050 | A | [Concept Sliders: LoRA Adaptors for Precise Control in Diffusion Models](https://arxiv.org/abs/2311.12092); 2023/2024, ECCV |
| P051 | A | [SliderSpace: Decomposing the Visual Capabilities of Diffusion Models](https://arxiv.org/abs/2502.01639); 2025, ICCV |

### Structural control and binding

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P052 | B | [Image Generation from Scene Graphs](https://github.com/google/sg2im); CVPR 2018 |
| P053 | A | [Adding Conditional Control to Text-to-Image Diffusion Models](https://github.com/lllyasviel/ControlNet); ICCV 2023 |
| P054 | B | [GLIGEN: Open-Set Grounded Text-to-Image Generation](https://github.com/gligen/GLIGEN); CVPR 2023 |
| P055 | A | [InstanceDiffusion: Instance-level Control for Image Generation](https://github.com/frank-xwang/InstanceDiffusion); CVPR 2024 |
| P056 | A | [DreamRenderer: Taming Multi-Instance Attribute Control in Large-Scale Text-to-Image Models](https://arxiv.org/html/2503.12885); ICCV 2025 |
| P057 | B | [UniCombine: Unified Multi-Conditional Combination with Diffusion Transformer](https://arxiv.org/html/2503.09277); ICCV 2025 |
| P058 | B | [Make It Count: Text-to-Image Generation with an Accurate Number of Objects](https://openaccess.thecvf.com/content/CVPR2025/papers/Binyamin_Make_It_Count_Text-to-Image_Generation_with_an_Accurate_Number_of_CVPR_2025_paper.pdf); CVPR 2025; preprint 2024 |
| P059 | B | [OverLayBench: A Benchmark for Layout-to-Image Generation with Dense Overlaps](https://arxiv.org/html/2509.19282v1); 2025 preprint |

### Editing, inversion, and drift

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P060 | A | [Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502); 2020 preprint; ICLR 2021 |
| P061 | B | [SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations](https://arxiv.org/abs/2108.01073); 2021 preprint; ICLR 2022 |
| P062 | B | [Prompt-to-Prompt Image Editing with Cross Attention Control](https://arxiv.org/abs/2208.01626); 2022 preprint; ICLR 2023 |
| P063 | A | [Null-text Inversion for Editing Real Images using Guided Diffusion Models](https://arxiv.org/abs/2211.09794); 2022 preprint; CVPR 2023 |
| P064 | A | [EDICT: Exact Diffusion Inversion via Coupled Transformations](https://arxiv.org/abs/2211.12446); 2022 preprint; CVPR 2023 |
| P065 | B | [Plug-and-Play Diffusion Features for Text-Driven Image-to-Image Translation](https://arxiv.org/abs/2211.12572); 2022 preprint; CVPR 2023 |
| P066 | B | [Semantic Image Inversion and Editing using Rectified Stochastic Differential Equations](https://arxiv.org/abs/2410.10792); 2024 preprint; ICLR 2025 |
| P067 | A | [FlowEdit: Inversion-Free Text-Based Editing Using Pre-Trained Flow Models](https://arxiv.org/abs/2412.08629); 2024 preprint; ICCV 2025 |
| P068 | A | [On-Policy Self-Distillation for Multi-Turn Image Editing](https://arxiv.org/abs/2609.35611); 2026 arXiv preprint |
| P069 | B | [FreqEdit: Preserving High-Frequency Features for Robust Multi-Turn Image Editing](https://arxiv.org/abs/2512.01755); 2025 preprint; CVPR 2026 |
| P070 | B | [Why Do DiT Editors Drift? Plug-and-Play Low Frequency Alignment in VAE Latent Space](https://arxiv.org/abs/2605.08250); 2026 arXiv preprint |
| P071 | A | [PnP Inversion: Boosting Diffusion-based Editing with 3 Lines of Code](https://proceedings.iclr.cc/paper_files/paper/2024/hash/661caac7729aa7d8c6b8ac0d39ccbc6a-Abstract-Conference.html); ICLR 2024; circulated as Direct Inversion, 2023. One work, not two. |

### Physical control and assistance

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P072 | A | [The Bas-Relief Ambiguity](https://link.springer.com/article/10.1023/A:1008154927611); 1999, IJCV, peer-reviewed. |
| P073 | A | [Mitsuba 2: A Retargetable Forward and Inverse Renderer](https://rgl.epfl.ch/publications/NimierDavidVicini2019Mitsuba2); 2019, TOG/SIGGRAPH Asia, peer-reviewed. |
| P074 | A | [NeRFactor: Neural Factorization of Shape and Reflectance Under an Unknown Illumination](https://arxiv.org/abs/2106.01970); 2021, TOG/SIGGRAPH Asia, peer-reviewed. |
| P075 | A | [Marigold: Affordable Adaptation of Diffusion-Based Image Generators for Image Analysis](https://arxiv.org/abs/2505.09358); 2025 expanded preprint. |
| P076 | A | [DiLightNet: Fine-grained Lighting Control for Diffusion-based Image Generation](https://arxiv.org/abs/2402.11929); 2024, SIGGRAPH Conference Papers, peer-reviewed. |
| P077 | A | [Alchemist: Parametric Control of Material Properties with Diffusion Models](https://arxiv.org/abs/2312.02970); 2024, CVPR, peer-reviewed. |
| P078 | A | [DiffusionRenderer: Neural Inverse and Forward Rendering with Video Diffusion Models](https://arxiv.org/abs/2501.18590); 2025, CVPR, peer-reviewed. |
| P079 | B | [Repurposing Diffusion-Based Image Generators for Monocular Depth Estimation](https://arxiv.org/abs/2312.02145); CVPR 2024; 2023 preprint. Separate from expanded 2025 analysis work. |

### Evaluation and human evidence

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P080 | B | The Unreasonable Effectiveness of Deep Features as a Perceptual Metric. CVPR 2018, peer-reviewed. [Paper](https://openaccess.thecvf.com/content_cvpr_2018/html/Zhang_The_Unreasonable_Effectiveness_CVPR_2018_paper.html). |
| P081 | B | TIFA: Accurate and Interpretable Text-to-Image Faithfulness Evaluation with Question Answering. ICCV 2023. [Paper](https://arxiv.org/abs/2303.11897). |
| P082 | B | Davidsonian Scene Graph: Improving Reliability in Fine-grained Evaluation for Text-to-Image Generation. ICLR 2024. [Paper](https://arxiv.org/abs/2310.18235). |
| P083 | B | GenEval: An Object-Focused Framework for Evaluating Text-to-Image Alignment. NeurIPS 2023. [Paper](https://arxiv.org/abs/2310.11513). |
| P084 | A | GenEval 2: Addressing Benchmark Drift in Text-to-Image Evaluation. First posted December 18, 2025; preprint status verified. [Paper](https://arxiv.org/abs/2512.16853). |
| P085 | B | T2I-CompBench++: An Enhanced and Comprehensive Benchmark for Compositional Text-to-image Generation. TPAMI 2025. [Journal version](https://arxiv.org/abs/2307.06350v3). |
| P086 | B | Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation. NeurIPS 2023. [Paper](https://arxiv.org/abs/2305.01569). |
| P087 | B | Rich Human Feedback for Text-to-Image Generation. CVPR 2024. [Paper](https://openaccess.thecvf.com/content/CVPR2024/html/Liang_Rich_Human_Feedback_for_Text-to-Image_Generation_CVPR_2024_paper.html). |
| P088 | B | DreamBench++: A Human-Aligned Benchmark for Personalized Image Generation. ICLR 2025; 2024 preprint. [Paper](https://arxiv.org/abs/2406.16855). |
| P089 | A | EdiVal-Agent: An Object-Centric Framework for Automated, Fine-Grained Evaluation of Multi-Turn Editing. ICLR 2026 per official release; 2025 preprint. [Paper](https://arxiv.org/abs/2509.13399). |
| P090 | A | Perceptually Aligned Evaluation of Style Transfer. October 7, 2026 preprint. [Paper](https://arxiv.org/abs/2610.10003). |

### Agents, policy, and search

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P091 | B | [Idea2Img: Iterative Self-Refinement with GPT-4V(ision) for Automatic Image Design and Generation](https://arxiv.org/html/2310.08541v2); 2023 preprint. |
| P092 | B | [GenArtist: Multimodal LLM as an Agent for Unified Image Generation and Editing](https://arxiv.org/html/2407.05600); NeurIPS 2024. |
| P093 | B | [MIRA: Multimodal Iterative Reasoning Agent for Image Editing](https://arxiv.org/html/2511.21087v2); 2025 preprint; CVPR 2026 Findings. |
| P094 | A | [Amateur-Friendly Conversational Image Editing Agent via Three Stages of Multitask Alignment](https://arxiv.org/html/2606.08016); CVPR 2026 Findings. |
| P095 | B | [MonetGPT: Solving Puzzles Enhances MLLMs’ Image Retouching Skills](https://arxiv.org/html/2505.06176); ACM TOG 2025. |
| P096 | A | [Iterative Refinement Improves Compositional Image Generation](https://arxiv.org/html/2601.15286); 2026 preprint. |
| P097 | A | [EditAgent: Rethinking Agentic Image Editing](https://arxiv.org/abs/2610.39664); Preprint submitted 2026-10-29. |
| P098 | B | [Bayesian Optimization for Controlled Image Editing via LLMs](https://arxiv.org/html/2502.18116v1); 2025 preprint. |
| P099 | B | [Scaling Image and Video Generation via Test-Time Evolutionary Search](https://arxiv.org/html/2505.17618); 2025 preprint. |
| P100 | B | [Optimize Your Sampling: Tuned Diffusion Sampling with Bayesian Optimization](https://arxiv.org/html/2608.18040v1); 2026 preprint. |

### NPR and asset construction

| ID | Priority | Exact work and verified publication status |
|---|---|---|
| P101 | A | [Painterly Rendering with Curved Brush Strokes of Multiple Sizes](https://mrl.cs.nyu.edu/publications/painterly98/hertzmann-siggraph98.pdf); SIGGRAPH 1998. |
| P102 | B | [A Non-Photorealistic Lighting Model For Automatic Technical Illustration](https://www.cs.princeton.edu/courses/archive/fall00/cs597b/papers/gooch98.pdf); SIGGRAPH 1998. |
| P103 | B | [Computer-Generated Watercolor](https://grail.cs.washington.edu/projects/watercolor/); SIGGRAPH 1997. |
| P104 | B | [Real-time hatching](https://hhoppe.com/proj/hatching/); SIGGRAPH 2001. |
| P105 | B | [The Lit Sphere: A Model for Capturing NPR Shading from Art](https://graphicsinterface.org/proceedings/gi2001/gi2001-17/); Graphics Interface 2001. |
| P106 | A | [StyLit: Illumination-Guided Example-Based Stylization of 3D Renderings](https://dcgi.fel.cvut.cz/publications/2016/fiser-tog-stylit); SIGGRAPH/TOG 2016. |
| P107 | B | [Differentiable Vector Graphics Rasterization for Editing and Learning](https://people.csail.mit.edu/tzumao/diffvg/); SIGGRAPH Asia/TOG 2020. |
| P108 | B | [Illustrative Rendering in Team Fortress 2](https://steamcdn-a.akamaihd.net/apps/valve/2007/NPAR07_IllustrativeRenderingInTeamFortress2.pdf); NPAR 2007. |
| P109 | B | [Artist-Inator: Text-based, Gloss-aware Non-photorealistic Stylization](https://graphics.unizar.es/projects/artist-inator_2025/); Computer Graphics Forum / EGSR 2025. |
| P110 | A | [Style-Aware Gloss Control for Generative Non-Photorealistic Rendering](https://arxiv.org/html/2602.16611v3); Computers & Graphics 2026. |

## Source notes and evidence limits

### The audits take priority; the notes remain research snapshots

The first nine academic notes supply the broad landscape. **Audit 10 refines direct-control and NPR-gloss claims; audit 11 refines correction-policy, numerical-record, and cost interpretations; audit 12 supplies canonical record and artifact reconciliation.** Their findings are incorporated in this volume without rewriting the saved notes. The companion first volume remains an earlier synthesis rather than an automatically amended publication.

| Saved note | Role in this synthesis |
|---|---|
| 01 — Generative foundations | Objectives, representations, architectural hybrids, reconstruction limits. |
| 02 — Style representation and transfer | Statistical genealogy, learned conditioning, leakage, theory, crossed supervision. |
| 03 — Personalization and adaptation | Concept targets, data/exposure, regularization, composition and generalization. |
| 04 — Structured control and conditioning | Instances, graphs, layouts, dense maps, conflicts and fair inputs. |
| 05 — Editing, inversion, and preservation | Reconstruction/editability distinctions, feature copying, flow/AR editing, drift. |
| 06 — Physical control and 3D assistance | Forward/inverse problems, intrinsic layers, proxies, transport, deployment boundaries. |
| 07 — Evaluation, benchmarks, and human evidence | Constructs, benchmark drift, human protocols, statistical operating points. |
| 08 — Agentic creation and adaptive search | Prompt/image/program/denoising search, learned policies, stopping, prior art. |
| 09 — Stylized art and asset production | NPR techniques, perception, explicit representations and collection production. |
| 10 — Direct axis control audit | Method-specific selectivity, human evidence, v3 gloss results and artifact gaps. |
| 11 — Correction strategy audit | Matched-budget qualifications, hybrid source policies, bundled diagnostic evidence. |
| 12 — Evidence and record reconciliation | Corrected identities, titles, venues, dates, component terms and unresolved conflicts. |

The local academic-note index provides a shorter navigation route. The [first volume](measuring-visual-style.md) and its thirteen-note index cover the detailed observable axes and reference-resolution limits. The corpus is linked rather than appended wholesale: a reader can inspect the full scholarly ledgers and methodological qualifications without mistaking overlapping citations for independent confirmations.

### Search accounting belongs to the original research, not this writing phase

The saved notes document discovery, citation tracing, selected paper/appendix reading, official documentation and artifact checks. Primary-source inspection was preferred over promotional summaries. Some verification used focused extraction, so uninspected supplemental evidence is not declared nonexistent. The following counts are the notes’ own accounting, with different units and approximation levels; **they should not be summed into unique queries, unique works, or a new review budget**.

| Note | Recorded discovery/inspection accounting |
|---|---|
| 01 | Approximately 26 successful Kagi queries, one additional failure; one Exa search and five batch retrievals. |
| 02 | Approximately 49 Kagi discovery queries and nine Exa batch fetches, plus primary/artifact checks. |
| 03 | Twenty-nine Kagi query attempts, with timeouts recorded; direct paper and artifact inspection. |
| 04 | Thirty-two Kagi queries and eight Exa batch fetches, plus targeted table/release checks. |
| 05 | Approximately 50 Kagi queries, citation tracing, selected PDF/HTML and artifact inspection. |
| 06 | Thirty-six Kagi queries, two Exa batch fetches, and direct physical-control/artifact checks. |
| 07 | Thirty-five Kagi queries including a timeout; evaluation, human-protocol and artifact checks. |
| 08 | Thirty-eight Kagi queries; three Exa batch fetches requesting 28 URLs; direct source inspection. |
| 09 | Forty-nine Kagi queries; historical/current NPR source and dataset checks. |
| 10 | Four focused Kagi queries; six primary-paper HTML texts and targeted repositories/notebooks. |
| 11 | Thirteen targeted public HTTP inspections across seven papers; no broad new discovery. |
| 12 | Seven Kagi discovery queries and targeted bibliographic/project metadata reconciliation. |

This is an intensive, purposive landscape review with broad historical and recent coverage, **not an exhaustive registered systematic review**. The 110 index rows are a curated set of bibliographic works, not the complete number consulted. A preprint and its renamed conference publication are merged where identity is established; distinct Marigold publications remain separate. A dataset, project page, checkpoint, or duplicate URL is not another scholarly work. Independent replication is not inferred from several papers using the same pretrained model, benchmark, or authors’ artifacts.

### Remaining uncertainty is consequential

No method was installed, trained, generated with, or benchmarked in this synthesis. No original reference was measured, and no approved card-domain threshold, sample requirement, or complete acceptance classifier exists here. Much recent empirical evidence is author-reported, sometimes supported by cross-paper evaluation but rarely by an audited exact independent replication. Domain transfer from photographs, portraits, icons, tiles, or restricted painterly objects to collectible cards remains to be tested.

Artifact access failures, rate limits, incomplete releases, source/version discrepancies, and ambiguous component terms remain visible in the notes. This writing phase did not recheck external URL reachability or resolve missing licenses. StyleShot’s exact first-online date, the expanded Marigold work’s journal venue, CSD’s released-weight discrepancy, current gloss annotation mappings/supplement, Artist-Inator’s complete original evaluation, and full consumer-AMD compatibility remain unresolved. No unavailable detail is converted into a claim of impossibility, and no unknown permission is converted into clearance.

The report’s proposals are experimental questions and analysis principles. They authorize neither software adoption nor a production architecture. Scientific review, bibliography acceptance, and any later decision to test or implement the approach remain separate from this synthesis.
