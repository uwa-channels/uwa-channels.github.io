---
title: "Noise"
linkTitle: "Noise"
weight: 2
menu:
  main:
    weight: 1
description: >
  Site-specific ambient noise models accompanying each channel, covering colored Gaussian noise and, for the Red channel, impulsive alpha-stable noise.
cascade:
  - type: "docs"
---

Along with each channel, you will find the noise model corresponding to it. The noise models are based on the statistics derived from the corresponding experimental recordings. The noise is modeled as non-white Gaussian for all the channels except the `red` channel, whose impulsive noise is modeled by the $\alpha$-stable sub-Gaussian distribution. The power spectral density (psd) of the Gaussian noise estimated from the recordings is included in the models, as is the spatial correlation across the array elements.

The library also contains a generic noise model, which represents the Gaussian component of the ambient noise. This noise exhibits log-linear decay in frequency (nominally 17 dB/decade), and is assumed to be uncorrelated in space. The power of the noise within a given bandwidth can be adjusted by the user.


| Color                                                | Channel(s)                          | Noise Source(s)                        |
|-------------------------------------------------------|--------------------------------------|-----------------------------------------|
| <span style="color: #0072BD">Blue</span>              | `blue_1` ... `blue_20`              | `blue_noise`                            |
| <span style="color: #D95319">Red</span>               | `red_1` ... `red_4`                 | `red_noise`                             |
| <span style="color: #EDB120">Yellow</span>            | `yellow_1` ... `yellow_3`           | `yellow_noise_1`                        |
|                                                         | `yellow_4`                          | `yellow_noise_2`                        |
|                                                         | `yellow_5`                          | `yellow_noise_3`                        |
|                                                         | `yellow_6`                          | `yellow_noise_4`                        |
| <span style="color: #7E2F8E">Purple</span>            | `purple_1` ... `purple_5`           | `purple_noise_1` ... `purple_noise_5`   |
|                                                         | `purple_6` ... `purple_10`          | `purple_noise_1` ... `purple_noise_5`   |
|                                                         | `purple_11` ... `purple_15`         | `purple_noise_1` ... `purple_noise_5`   |
| <span style="color: #77AC30">Green</span>             | `green`                             | `green_noise`                           |
| <span style="color: #000000">Black</span>             | `black`                             | `black_noise`                           |
| <span style="color: #E377C2">Pink</span>              | `pink_1` ... `pink_3`               | `pink_noise_1` ... `pink_noise_3`       |
| <span style="color: #8C564B">Brown</span>             | `brown`                             | *(none)*                                |
