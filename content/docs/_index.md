---
title: "User's Guide"
linkTitle: "User's Guide"
menu:
  main:
    weight: 3
description: >

---

The channels stored in this library can be used in two ways: (1) a channel can be applied directly to a user-generated signal, or (2) it can be decompressed for visualizing. Ready-to-use code for performing these functions is available under [GitHub](https://github.com/uwa-channels). You can also download the MATLAB package [here](https://github.com/uwa-channels/matlab/archive/refs/heads/main.zip). To install the Python package,

```bash
pip install -i https://test.pypi.org/simple/ uwa-replay
```

## Applying a channel to an arbitrary signal 

* To pass a signal of your choice through a channel, generate the desired signal in passband, respecting the bandwidth and the sampling rate limits of the chosen channel (see the [channel](/channels) tab).
* Run `replay` on the signal. 
* Specify the noise power, and add the output of `noisegen` to the output of `replay` at a desired signal-to-noise ratio.

{{< tabpane >}}
{{< tab header="Replay and generate noise" disabled=true />}}
{{< tab header="MATLAB/Octave" lang="matlab" >}}
channel = load('blue_1.mat');
noise = load('blue_1_noise.mat');
y = replay(input, fs, array_index, channel);
w = noisegen(size(y), fs, array_index, noise);
r = y + 0.05 * w;
{{< /tab >}}
{{< tab header="Python" lang="python" >}}
from uwa_replay import replay, noisegen
channel = h5py.File("blue_1.mat", "r")
noise = h5py.File("blue_1_noise.mat", "r")
y = replay(input, fs, array_index, channel)
w = noisegen(y.shape, fs, array_index, noise)
r = y + 0.05 * w
{{< /tab >}}
{{< /tabpane >}}

A simple example of this process is given in [`MATLAB`](https://github.com/uwa-channels/matlab/blob/main/examples/example_replay.m) and [`Python`](https://github.com/uwa-channels/python/blob/main/examples/example_replay.py). Before running the example code, please read the corresponding `README` file.

{{% alert title="Important note" color="warning" %}}
The channels are specified for a certain acoustic bandwidth that was used during the experiment. When working with a channel, please understand that only that bandwidth is visible. If you are designing a signal that you will pass through a channel, the bandwidth of your signal must fit within the stated limit. Note that you do **not** need to decompress the channel first to replay the signal.
{{% /alert %}}

## Visualizing a channel

To visualize a channel as a collection of impulse responses evolving over time, you will need to decompress the channel impulse responses via `unpack.m`. This will produce a new channel matrix that is decompressed (it is larger than the stored original) and contains all the physical effects of delay drifting. The new matrix can be generated at arbitrary sampling rates in time, provided it is no greater than the sampling rate in delay.

A simple example of this process is given in [`MATLAB`](https://github.com/uwa-channels/matlab/blob/main/examples/example_unpack.m) and [`Python`](https://github.com/uwa-channels/python/blob/main/examples/example_unpack.py). Before running the example code, please read the corresponding `README` file.

