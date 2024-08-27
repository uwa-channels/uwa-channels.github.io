---
title: "Noises"
linkTitle: "Noises"
weight: 2
menu:
  main:
    weight: 1
description: >
cascade:
  - type: "docs"
---

Here you will find noise generators corresponding to each channel (blue, green, etc.). They generate synthetic noise according to the statistics derived from the corresponding experiments. The basic component of each noise is Gaussian, but not white. The power spectral density (psd) estimated from the recordings is also fitted to a log-linear model whose decay rate is specified in dB/decade. Synthetic noise can be generated using either the original or the model-fitted psd. Spatial correlation that exists across the receiving array elements is also taken into account when generating the synthetic noise.  

The library also contains theoretical noise, which represents the Gaussian component of the ambient noise. This noise exhibits log-linear decay in frequency, and is assumed to be uncorrelated in space. The power of the noise within a given bandwidth can be adjusted by the user.

Download the noise statistics files [here](), then go to [Github](), download and run `generate_noise.m`.

