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

Along with each channel (blue, green, etc.), you will find the noise parameters corresponding to it. These parameters correspond to the statistics derived from the corresponding experiments. The noise is non-white Gaussian for all the channels except the red channel, whose impulsive noise is modeled by the alpha-stable sub-Gaussian distribution.. The power spectral density (psd) of the Gaussian noise estimated from the recordings is included in the models, as is the spatial correlation across the array elements. The measured psd is additionally fitted to a log-linear model whose decay rate is specified in dB/decade. Synthetic noise can be generated using either the original or the model-fitted psd. 

The library also contains a theoretical noise model, which represents the Gaussian component of the ambient noise. This noise exhibits log-linear decay in frequency (nominally 17 dB/decade), and is assumed to be uncorrelated in space. The power of the noise within a given bandwidth can be adjusted by the user.

Download the noise statistics files [here](), then go to [Github](), download and run `generate_noise.m`.

