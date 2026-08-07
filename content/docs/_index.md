---
title: "User's Guide"
linkTitle: "User's Guide"
menu:
  main:
    weight: 3
description: >
  Instructions for downloading the channel library, replaying a signal through a channel, adding site-specific noise, and visualizing a decompressed channel.
---

The channels stored in this library can be used in two ways: a channel can be (1) applied directly to a user-generated signal, or (2) decompressed for visualization. Ready-to-use code for performing these functions is available on [GitHub](https://github.com/uwa-channels). You can also download the MATLAB package [here](https://github.com/uwa-channels/matlab/archive/refs/heads/main.zip). To install the Python package,

```bash
pip install uwa-channels
```

Julia support is provided by the [`UnderwaterAcoustics.jl`](https://github.com/org-arl/UnderwaterAcoustics.jl) package, maintained separately. See that package's documentation for installation and usage instructions.

## Applying a channel to an arbitrary signal

* To pass a signal of your choice through a channel, generate the desired signal in passband, respecting the bandwidth and sampling-rate limits of the chosen channel (see the [Channels](/channels) tab).
* Run `replay` on the signal.
* Scale the output of `noisegen` and add it to the output of `replay` to obtain the desired signal-to-noise ratio. That is, form $r_{\text{out}}(t) = \bar{r}_{\text{out}}(t) + \sigma_n \hat{n}(t)$, where $\bar{r}_{\text{out}}(t)$ is the noiseless replay output, $\hat{n}(t)$ is the generated noise, and $\sigma_n$ is the noise level that sets the SNR. In the example below, $\sigma_n$ is `0.05`.

{{< tabpane >}}
{{< tab header="Replay and generate noise" disabled=true />}}
{{< tab header="MATLAB/Octave" lang="matlab" >}}
channel = load('blue_1.mat');
noise = load('blue_1_noise.mat');
array_index = [1, 2, 3];
y = replay(input, fs, array_index, channel);
w = noisegen(size(y), fs, array_index, noise);
r = y + 0.05 * w;
{{< /tab >}}
{{< tab header="Python" lang="python" >}}
import h5py
from uwa_channels import replay, noisegen
channel = h5py.File("blue_1.mat", "r")
noise = h5py.File("blue_1_noise.mat", "r")
array_index = [0, 1, 2]
y = replay(input, fs, array_index, channel)
w = noisegen(y.shape, fs, array_index, noise)
r = y + 0.05 * w
{{< /tab >}}
{{< /tabpane >}}

A simple example of this process is given in [`MATLAB`](https://github.com/uwa-channels/matlab/blob/main/examples/example_replay.m) and [`Python`](https://github.com/uwa-channels/python/blob/main/examples/example_replay.py). Before running the example code, please read the corresponding `README` file.

> [!WARNING] Important note
>
> The channels are specified for a certain acoustic bandwidth that was used during the experiment. When working with a channel, note that only that bandwidth is captured. If you are designing a signal to pass through a channel, the bandwidth of your signal must fit within the stated limit. Note that you do **not** need to decompress the channel first to replay the signal.

## Visualizing a channel

To visualize a channel as a collection of impulse responses evolving over time, you will need to decompress the channel impulse responses via `unpack`. This will produce the decompressed impulse response $\hat{h}(\tau, t)$, which is larger than the stored original and contains all the physical effects of delay drift. The output is a $K \times M \times N_t$ array, where $K$ is the number of delay taps, $M$ is the number of array elements, and $N_t$ is the number of time snapshots. This array can be generated at an arbitrary sampling rate in time, provided that rate does not exceed the sampling rate in delay.

A simple example of this process is given in [`MATLAB`](https://github.com/uwa-channels/matlab/blob/main/examples/example_unpack.m) and [`Python`](https://github.com/uwa-channels/python/blob/main/examples/example_unpack.py). Before running the example code, please read the corresponding `README` file.

