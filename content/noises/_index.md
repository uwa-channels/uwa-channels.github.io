---
title: "Noise"
linkTitle: "Noise"
weight: 2
menu:
  main:
    weight: 1
description: >
  Site-specific ambient noise models accompanying every channel except Brown, covering colored Gaussian noise and, for the Red channel, impulsive alpha-stable noise.
cascade:
  - type: "docs"
---

Every channel except Brown has a noise model fitted to recordings from the same experiment. Most models describe colored Gaussian noise. Red captures impulsive noise using an $\alpha$-stable sub-Gaussian ($\alpha$SG) process.

Each model contains a characteristic exponent $\alpha$ and mixing coefficients $\beta_{ij}(kT_s)$. The exponent is 2 for Gaussian noise. The coefficients describe the noise spectrum and the spatial correlation between array elements. To generate noise samples $\hat{n}_i(nT_s)$, `noisegen` filters independent, identically distributed innovations through these coefficients. The [noise file specifications](/docs/file_specifications#noise-file-format) give the equations and field definitions.

A generic model is also available when you do not need noise from a particular site. It represents the Gaussian component of ambient noise, with a spectrum that falls by approximately 17 dB per decade and no spatial correlation. You can scale the generated noise to set its power within your signal bandwidth.

Use `noisegen(size(y), fs)` in MATLAB or `noisegen(y.shape, fs)` in Python. For Julia, see the availability note for `PinkGaussianNoise(σ)` in the [User's Guide](/docs#applying-a-channel-to-an-arbitrary-signal).

The table lists the noise file for each channel.

| Codename                                             | Channel(s)                          | Noise Source(s)                        |
|-------------------------------------------------------|--------------------------------------|-----------------------------------------|
| <span class="channel-blue">Blue</span>              | `blue_1` ... `blue_20`              | `blue_noise`                            |
| <span style="color: #D95319">Red</span>               | `red_1` ... `red_4`                 | `red_noise`                             |
| <span style="color: #EDB120">Yellow</span>            | `yellow_1` ... `yellow_3`           | `yellow_noise_1`                        |
|                                                         | `yellow_4`                          | `yellow_noise_2`                        |
|                                                         | `yellow_5`                          | `yellow_noise_3`                        |
|                                                         | `yellow_6`                          | `yellow_noise_4`                        |
| <span class="channel-purple">Purple</span>            | `purple_1` ... `purple_5`           | `purple_noise_1` ... `purple_noise_5`   |
|                                                         | `purple_6` ... `purple_10`          | `purple_noise_1` ... `purple_noise_5`   |
|                                                         | `purple_11` ... `purple_15`         | `purple_noise_1` ... `purple_noise_5`   |
| <span style="color: #77AC30">Green</span>             | `green`                             | `green_noise`                           |
| <span class="channel-black">Black</span>             | `black`                             | `black_noise`                           |
| <span style="color: #E377C2">Pink</span>              | `pink_1` ... `pink_3`               | `pink_noise_1` ... `pink_noise_3`       |
| <span class="channel-brown">Brown</span>             | `brown`                             | *(none)*                                |

<p style="font-size: 13px; margin-top: 8px;"><a href="/channels/purple" class="channel-purple">Purple</a> channels and noise files pair by receive system: <code>purple_k</code>, <code>purple_(k+5)</code>, and <code>purple_(k+10)</code> use <code>purple_noise_k</code>, the noise recorded on system k. No site-specific noise model is available for <a href="/channels/brown" class="channel-brown">Brown</a>; use the generic model described above.</p>
