# Research

| File | What | When |
|---|---|---|
| [card-sets-in-real-games.md](card-sets-in-real-games.md) | What Playrix and other games put in film and horror sets | 2026-11-02 |
| [measuring-visual-style.md](measuring-visual-style.md), [notes](measuring-visual-style-notes/README.md) | Literature on measuring a visual style: embeddings, color, shape, calibration | 2026-10-31, before the build |
| [image-generation-and-style.md](image-generation-and-style.md) | Literature on reference-conditioned generation, adapters, editing, agentic loops | 2026-10-31, before the build |

What the build took from the literature: CSD for style, DINO and SigLIP for content, BiRefNet masks, calibration of model raters on labelled pairs, pairwise rather than lone judging, and 3D geometry as structure for the image model.

## Landscape check, 2026-11-07

What changed since the literature review, and what the project tried. Sources were read on 2026-11-07.

- **Open models now fit one consumer GPU.** Qwen-Image-2.1 (7B, 10 references, research licence) and FLUX 3 Image Klein (5.6B, 10 references, gated, free under $5M revenue) run through `diffusers` 0.42 with no remote code. Qwen-Image-2.1 was tried in `experiments/generators.py`; FLUX 3 Klein needs its licence accepted on Hugging Face first. ([Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1), [FLUX 3 Klein](https://bfl.ai/blog/flux-3-image-klein))
- **Closed models:** the GPT image line behind Codex takes several references; Nano Banana Pro has an explicit style-reference role and was tried through the Antigravity CLI; Recraft V4 Styles and Midjourney V8 expose a style-strength control. ([OpenAI](https://developers.openai.com/api/docs/guides/image-generation), [Google](https://aistudio.google.com/docs/image-generation), [Recraft](https://www.recraft.ai/docs/api-reference/models/recraft-v4-styles))
- **Studios train a style.** Scenario, Layer and Leonardo train a LoRA on a studio's own art, often one per asset type, and edit LoRAs on before/after pairs. The brief provides no LoRA, so training one on the 160 reference cards is the obvious next step: `diffusers` ships a LoRA script for FLUX 3 Klein, about 1-3 hours here. ([Scenario](https://help.scenario.com/en/articles/basics-of-model-training), [Layer](https://www.layer.ai/case-study/games-united), [script](https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/README_flux3_klein.md))
- **3D renders as structure.** Depth control holds contours too rigidly; edit models copy the render's finish, which is the gloss the producer saw on blockout cards. Practice is an edit model with a style LoRA, or a matte structure pass instead of the shaded render.
- **Measuring style.** Raw CSD cosine fails as an absolute score and is corrected for hubness by CSD+ (CSLS); here it moved agreement with the producer from 128 to 132 of 218 pairs, within noise (`experiments/csd_plus.py`). VLM judges do better pairwise than pointwise and show position bias, which is why the director judges both orders. ([CSD+](https://arxiv.org/abs/2605.09030), [GenArena](https://arxiv.org/abs/2602.06013))
- **What the tools lack that this project has:** none of the products measures against a human, runs blind twins or builds geometry for construction.
