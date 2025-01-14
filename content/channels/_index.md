---
title: "Channels"
linkTitle: "Channels"
weight: 50
menu:
  main:
    weight: 1
description: >
cascade:
  - type: "docs"
---

The channels contained in this library come from various experiments. The experiments differ by geographical location, transmission distance, water depth, transmitter/receiver mobility, acoustic bandwidth and the size of the recording array. The channels are color-labeled, and a detailed description of relevant parameters is given for each.

A channel is estimated from the experimental data and stored in a <mark>matrix</mark> ${\bf H}$ of complex-baseband impulse responses evolving over time. Each <mark>row</mark> of this matrix represents an instantaneous channel response as a function of delay. Different rows correspond to different, equi-spaced instants in time. Any motion-induced delay drifting is suppressed in the channel matrix ${\bf H}$ to enable compression for efficient storage. A separate vector <mark>$\theta$</mark> is provided which contains the uncompressed time-varying channel phase (delay). <mark>To fully reconstruct the channel, the matrix ${\bf H}$ needs to be uncompressed</mark>, and the phase $\theta$ needs to be imparted onto the channel to re-introduce phase shifting and delay drifting. Details of this process, along with the ready-to-use code, are given in the [User’s Guide](/docs).
