---
title: "User's Guide"
linkTitle: "User's Guide"
menu:
  main:
    weight: 3
description: >

---

The channels stored in this library can be used in two ways: (1) a channel can be applied directly to a user-generated signal, or (2) it can be decompressed for visualizing. Ready-to-use code for performing these functions is avaialble under the GitHub tab. The code is provided in **MATLAB**, **Python** and **Julia**.

## Applying a channel to an arbitrary signal 

* To pass a signal of your choice through a channel, generate the desired signal in passband, respecting the bandwidth and the sampling rate limits of the chosen channel (see “parameters” entry under the [channel](/channels) tab).
* State the sampling frequency of your passband signal.
* Run `replay.m` on the signal. 
* Specify the noise power, and add the output of `generate_noise.m` to the output of `replay.m`. 
* This will produce a noisy passband received signal.

A simple example of this process is given in `example.m`. Before running the example code, please read the corresponding `readme` file. 

{{% alert title="Important note" color="warning" %}}
The channels are specified for a certain acoustic bandwidth that was used during the experiment. When working with a channel, please understand that only that bandwidth is visible. If you are designing a signal that you will pass through a channel, the bandwidth of your signal must fit within the stated limit.  Note that you do **not** need to decompress the channel first to replay the signal.
{{% /alert %}}

## Visualizing a channel
* To visualize a channel as a collection of impulse responses evolving over time, you will need to decompress the channel impulse responses via `unpack.m`.
* This will produce a new channel matrix which is decompressed and contains all the physical effects of delay drifting. The new matrix can be generated at arbitrary sampling rates in both time and delay, provided they are no greater than the sampling rate in delay.

A simple example of this process is given in `unpack.m`. Before running the example code, please read the corresponding `readme` file. Note that visualizing a channel requires considerable computer memory.

