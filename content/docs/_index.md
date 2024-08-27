---
title: "User's Guide"
linkTitle: "User's Guide"
menu:
  main:
    weight: 3
description: >

---

Here, you will find the explanation and ready-to-use code for working with the channels. ~~You can simply look at the channel by either unpacking the compressed channel coefficients via `unpack.m`, or you can use the `replay.m` to replay the signal through the channel, without unpacking the coefficients first.~~

The code is provided in **MATLAB**, **Python** and **Julia**.

## Inspecting a channel
* Decompress the channel impulse responses via `unpack.m`.
* This will produce a new channel matrix which contains all the physical effects of delay drifting. The new matrix can be generated at an arbitrary sampling rate in time, provided it is no greater than the sampling rate in delay.


## Applying a channel to an arbitrary signal 

* Generate a desired signal in passband, respecting the bandwidth and sampling rate limits of the channel (see “parameters” entry under the [channel](/channels) tab).
* State the sampling frequency of your passband signal.
* Run `replay.m` on the signal.
* Specify the noise power, and add noise outputs from `generate_noise.m` to the output of `replay.m`. 
* This will produce a noisy passband received signal.

{{% alert title="Important note" color="warning" %}}
The channels are specified for a certain acoustic bandwidth that was used during the experiment. When working with a channel, please understand that only that bandwidth is visible. If you are designing a signal that you will pass through a channel, the bandwidth of your signal must fit into the stated limit.  Note that you do **not** need to unpack the channel first to replay the signal.
{{% /alert %}}

