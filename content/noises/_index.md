---
title: "Noise"
linkTitle: "Noise"
weight: 2
menu:
  main:
    weight: 1
description: >
cascade:
  - type: "docs"
---

Along with each channel, you will find the noise model corresponding to it. The noise models are based on the statistics derived from the corresponding experimental recordings. The noise is modeled as non-white Gaussian for all the channels except the `red` channel, whose impulsive noise is modeled by the $\alpha$-stable sub-Gaussian distribution. The power spectral density (psd) of the Gaussian noise estimated from the recordings is included in the models, as is the spatial correlation across the array elements.

The library also contains a generic noise model, which represents the Gaussian component of the ambient noise. This noise exhibits log-linear decay in frequency (nominally 17 dB/decade), and is assumed to be uncorrelated in space. The power of the noise within a given bandwidth can be adjusted by the user.


| Color  | Channel(s)                          | Noise Source(s)                                    | Notes                                                                                    |
|--------|-------------------------------------|----------------------------------------------------|------------------------------------------------------------------------------------------|
| Black  | `black`                             | `black_noise`                                      |                                                                                          |
| Blue   | `blue_1` ... `blue_20`              | `blue_noise`                                       | All 20 channels share one noise source                                                   |
| Brown  | `brown`                             | *(none)*                                           | No noise file                                                                            |
| Green  | `green`                             | `green_noise`                                      | Virtual time-diversity channel (collecting repetitions); `green_noise` is one repetition |
| Pink   | `pink_1`                            | `pink_noise_1`                                     |                                                                                          |
|        | `pink_2`                            | `pink_noise_2`                                     |                                                                                          |
|        | `pink_3`                            | `pink_noise_3`                                     |                                                                                          |
| Purple | `purple_1` ... `purple_5`           | `purple_noise_1` ... `purple_noise_5`              | One-to-one correspondence                                                                |
|        | `purple_6` ... `purple_10`          | `purple_noise_1` ... `purple_noise_5`              | Cycles back; `purple_6` maps to `purple_noise_1`, etc.                                   |
|        | `purple_11` ... `purple_15`         | `purple_noise_1` ... `purple_noise_5`              | Cycles again; `purple_11` maps to `purple_noise_1`, etc.                                 |
| Red    | `red_1`, `red_2`, `red_3`, `red_4`  | `red_noise`                                        | All four channels share one noise source                                                 |
| Yellow | `yellow_1`, `yellow_2`, `yellow_3`  | `yellow_noise_1`                                   | Three channels share one noise source                                                    |
|        | `yellow_4`                          | `yellow_noise_2`                                   |                                                                                          |
|        | `yellow_5`                          | `yellow_noise_3`                                   |                                                                                          |
|        | `yellow_6`                          | `yellow_noise_4`                                   |                                                                                          |
