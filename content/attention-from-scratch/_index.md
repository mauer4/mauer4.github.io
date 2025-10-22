---
title: Attention From Scratch
date: 2025-01-01
lastmod: 2025-10-22
type: page
outputs: [HTML]

design:
  spacing: '4rem'

hero:
  enable: true
  image:
    placement: full
---

I'm mapping the landscape of large language models to see what's possible for an individual, not just for massive tech teams. The exciting news is that fully open-source LLMs exist: you can inspect the weights, study the architecture, run the inference code, and even examine the training stack. As someone who loves marrying hardware, software, and math--classic HW/SW co-design--I'm inspired by the breakthroughs that pushed LLM performance forward: from FlashAttention and its fused kernels, to asynchronous attention in FlashAttention 2/3, and the paged-attention serving tricks in engines like vLLM. With today's cloud options, renting enterprise-class GPUs for inference is also within reach. So I've set a personal roadmap that takes me from beginner to building production-grade inference infrastructure on top of open models like Olmo 2. I'm not aiming to train new models; I'm aiming to run them exceptionally well. Along the way, I hope to understand the algorithms behind one of the most impactful technologies of our time--and maybe even find new ways to push them further.

**Repository:** [Attention-From-Scratch](https://github.com/mauer4/Attention-From-Scratch)

{{< attention_timeline >}}
