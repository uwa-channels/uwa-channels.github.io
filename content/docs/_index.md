---
title: "User's Guide"
linkTitle: "User's Guide"
menu:
  main:
    weight: 3
description: >

---

The channels stored in this library can be used in two ways: (1) a channel can be applied directly to a user-generated signal, or (2) it can be decompressed for visualizing. Ready-to-use code for performing these functions is avaialble under the GitHub tab.

## Applying a channel to an arbitrary signal 

* To pass a signal of your choice through a channel, generate the desired signal in passband, respecting the bandwidth and the sampling rate limits of the chosen channel (see “parameters” entry under the [channel](/channels) tab).
* State the sampling frequency of your passband signal.
* Run `replay` on the signal. 
* Specify the noise power, and add the output of `generate_noise` to the output of `replay` at a desired signal-to-noise ratio.
* This will produce a noisy passband received signal.

A simple example of this process is given in [**MATLAB**](https://github.com/uwa-channels/replay/blob/main/example.m) and [**Python**](https://github.com/uwa-channels/replay_python/blob/main/example.py). Before running the example code, please read the corresponding `readme` file.

For `Julia`, please visit [**UnderwaterAcoustics.jl**](https://github.com/org-arl/UnderwaterAcoustics.jl).

{{% alert title="Important note" color="warning" %}}
The channels are specified for a certain acoustic bandwidth that was used during the experiment. When working with a channel, please understand that only that bandwidth is visible. If you are designing a signal that you will pass through a channel, the bandwidth of your signal must fit within the stated limit.  Note that you do **not** need to decompress the channel first to replay the signal.
{{% /alert %}}

## Visualizing a channel

To visualize a channel as a collection of impulse responses evolving over time, you will need to decompress the channel impulse responses via unpacking. This will produce a new channel matrix which is decompressed (it is larger than the stored original) and contains all the physical effects of delay drifting. The new matrix can be generated at arbitrary sampling rates in time, provided it is no greater than the sampling rate in delay.

A simple example of this process is given in [`unpack.m`](https://github.com/uwa-channels/unpack/blob/main/unpack.m). Before running the example code, please read the corresponding [`readme`](https://github.com/uwa-channels/unpack) file. Note that decompressing and visualizing a channel requires considerable computer memory.

