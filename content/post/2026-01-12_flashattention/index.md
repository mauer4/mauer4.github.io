---
title: 'FlashAttention'
date: 2026-01-12T00:00:00Z
authors: ['admin']
tags: ['transformers', 'attention', 'deep-learning']
draft: false
---

FlashAttention is an IO-aware attention algorithm designed to reduce memory traffic and improve throughput by fusing attention operations and recomputing intermediates as needed. This post outlines the key ideas, practical implications for large-sequence workloads, and where the approach fits in modern transformer pipelines. I presented this paper to the UBC CPEN 511 class in February 2025. See the presentation below for the walkthrough, and download the source document for the full technical details.

Source document (PDF): [Review_FlashAttention_AdinMauer.pdf](Review_FlashAttention_AdinMauer.pdf)

<!--more-->

## Presentation
{{< pdf src="FlashAttention_AdinMauer_Presentation.pdf" height="900" >}}
