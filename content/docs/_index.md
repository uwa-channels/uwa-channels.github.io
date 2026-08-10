---
title: "User's Guide"
linkTitle: "User's Guide"
menu:
  main:
    weight: 3
description: >
  Instructions for downloading the channel library, replaying a signal through a channel, adding site-specific noise, and visualizing a decompressed channel.
---

The channels stored in this library can be used in two ways: a channel can be (1) applied directly to a user-generated signal, or (2) decompressed for visualization. Ready-to-use code for performing these functions is available on [GitHub](https://github.com/uwa-channels).

## Installation

{{< tabpane >}}
{{< tab header="Install the package:" disabled=true />}}
{{< tab header="MATLAB/Octave" lang="matlab" >}}
matlab.addons.install(websave([tempname '.mltbx'], 'https://github.com/uwa-channels/matlab/releases/latest/download/uwa-channels.mltbx'))
{{< /tab >}}
{{< tab header="Python" lang="python" >}}
pip install uwa-channels
{{< /tab >}}
{{< /tabpane >}}

The MATLAB command downloads the latest release and installs it as an add-on, so `replay`, `noisegen`, and `unpack` are on your path in every session afterwards. Running it again later upgrades the toolbox in place. To remove it, run `matlab.addons.uninstall('uwa-channels')`, or use **Home > Add-Ons > Manage Add-Ons**.

### Installing from a clone, and under Octave

If you want to read or modify the source, or if you are running Octave (which cannot read `.mltbx` files), add the repository folders to the search path instead:

```bash
git clone https://github.com/uwa-channels/matlab.git
cd matlab
```

Then, from that folder, in MATLAB or Octave:

```matlab
install
```

This adds `src` and `examples` to the search path and saves the path for later sessions, so edits to `src` take effect immediately. Avoid combining the two routes: if the packaged add-on is also installed, both copies sit on the path and the winner depends on path order.

### Requirements

The MATLAB package requires R2021a or later with the [Signal Processing Toolbox](https://www.mathworks.com/products/signal.html). Under Octave, it requires version 9.0 or later with the [`signal`](https://gnu-octave.github.io/packages/signal/) and [`statistics`](https://gnu-octave.github.io/packages/statistics/) packages.

Julia support is provided by the [`UnderwaterAcoustics.jl`](https://github.com/org-arl/UnderwaterAcoustics.jl) package, maintained separately. See that package's documentation for installation and usage instructions.

Once a package is installed, download the channel MAT-files from [Zenodo](https://doi.org/10.5281/zenodo.21287414) and place them where MATLAB, Octave, or Python can find them. The channel files are distributed separately from the code because of their size.

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

To visualize a channel as a collection of impulse responses evolving over time, you will need to decompress the channel impulse responses via `unpack`. This will produce the decompressed impulse response $\hat{h}(\tau, t)$, which is larger than the stored original and contains all the physical effects of delay drift. The output is a $K \times M \times T$ array, where $K$ is the number of delay taps, $M$ is the number of array elements, and $T$ is the number of time snapshots. This array can be generated at an arbitrary sampling rate in time, provided that rate does not exceed the sampling rate in delay.

A simple example of this process is given in [`MATLAB`](https://github.com/uwa-channels/matlab/blob/main/examples/example_unpack.m) and [`Python`](https://github.com/uwa-channels/python/blob/main/examples/example_unpack.py). Before running the example code, please read the corresponding `README` file.

