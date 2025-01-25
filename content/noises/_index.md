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

Along with each channel, you will find the noise model corresponding to it. The noise models are based on the statistics derived from the corresponding experimental recordings. The noise is modeled as non-white Gaussian for all the channels except the red channel, whose impulsive noise is modeled by the $alpha$-stable sub-Gaussian distribution. The power spectral density (psd) of the Gaussian noise estimated from the recordings is included in the models, as is the spatial correlation across the array elements. For some channels, the measured psd is additionally fitted to a log-linear model whose decay rate is specified in dB/decade. For these channels, which include the sampling rate of the noise signal, spatial covariance, and estimated and model-fitted psd, synthetic noise can be generated using either the original or the model-fitted psd.

The library also contains a generic noise model, which represents the Gaussian component of the ambient noise. This noise exhibits log-linear decay in frequency (nominally 17 dB/decade), and is assumed to be uncorrelated in space. The power of the noise within a given bandwidth can be adjusted by the user.

Download the noise statistics files [here](https://www.dropbox.com/scl/fo/3gyt4cgw47jfx716v0epd/AIqYaL5S2RxGylREu3sn-vY?rlkey=w2mvoklkm42zrrf6k6lwlzcxu&st=u3u6b5r9&dl=0).

