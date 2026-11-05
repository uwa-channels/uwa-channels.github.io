---
title: "User's Guide"
linkTitle: "User's Guide"
menu:
  main:
    weight: 3
description: >
  Instructions for downloading the channel library, replaying a signal through a channel, adding site-specific noise, and visualizing a decompressed channel.
---

Use the library to pass a signal through a measured underwater channel or to plot how the channel changes over time. The code is available on [GitHub](https://github.com/uwa-channels).

## Installation

{{< tabpane >}}
{{< tab header="Install the package:" disabled=true />}}
{{< tab header="MATLAB" lang="matlab" >}}
matlab.addons.install(websave([tempname '.mltbx'], 'https://github.com/uwa-channels/matlab/releases/latest/download/uwa-channels.mltbx'))
{{< /tab >}}
{{< tab header="Python" lang="bash" >}}
pip install uwa-channels
{{< /tab >}}
{{< tab header="Julia" lang="julia" >}}
using Pkg
Pkg.add(url="https://github.com/org-arl/UnderwaterAcoustics.jl")
Pkg.add("MAT")
{{< /tab >}}
{{< /tabpane >}}

The MATLAB command installs the latest release as an add-on. The functions `replay`, `noisegen`, and `unpack` will then be available in every session. Run the command again to update the toolbox. To remove it, run `matlab.addons.uninstall('Underwater Acoustic Channel Toolbox')`, or use **Home > Add-Ons > Manage Add-Ons**.

### Installing the MATLAB source

If you want to read or modify the source, add the repository folders to the search path instead:

```bash
git clone https://github.com/uwa-channels/matlab.git
cd matlab
```

In MATLAB, open the cloned folder and run:

```matlab
install
```

This adds `src` and `examples` to the search path and saves it for future sessions. Changes to `src` take effect immediately. If you previously installed the packaged add-on, remove it before using the source installation. Otherwise, MATLAB may run a different copy from the one you are editing.

### Requirements

The MATLAB package requires R2021a or later with the [Signal Processing Toolbox](https://www.mathworks.com/products/signal.html). Octave is not supported.

The Python package requires Python 3.10 or later; `pip` installs its dependencies (NumPy, SciPy, Matplotlib, and h5py).

Julia support is provided by the [`UnderwaterAcoustics.jl`](https://github.com/org-arl/UnderwaterAcoustics.jl) package, maintained separately by the Acoustic Research Laboratory, with the [`MAT`](https://github.com/JuliaIO/MAT.jl) package to read the files. It requires Julia 1.9 or later. The released version (v0.8.1) cannot apply `phi_hat` or `f_resamp`, which most channels use, so install the development version from GitHub as shown above until the next release. See the [replay guide](https://org-arl.github.io/UnderwaterAcoustics.jl/replay.html) of that package for more detail.

Once a package is installed, download the channel MAT-files from [Zenodo](https://doi.org/10.5281/zenodo.21287414) and place them where MATLAB or Python can find them. The channel files are distributed separately from the code because of their size. In Julia, a name such as `uacr://blue_1` instead of a file path downloads that file from Zenodo and caches it.

## Applying a channel to an arbitrary signal

1. Generate a real passband signal within the chosen channel's bandwidth and sampling-rate limits. These limits are listed on the [Channels](/channels) pages.
2. Pass the signal through the channel with `replay`.
3. Generate noise with `noisegen`, scale it to the desired level, and add it to the replay output.

Use the same `array_index` for `replay` and `noisegen` so that the signal and noise correspond to the same array elements. Indices start at 1 in MATLAB and Julia, and at 0 in Python.

The example uses the first three elements of the Blue array and a noise scale of `0.05`.

{{< tabpane >}}
{{< tab header="Replay and generate noise" disabled=true />}}
{{< tab header="MATLAB" lang="matlab" >}}
channel = load('blue_1.mat');
noise = load('blue_noise.mat');
array_index = [1, 2, 3];
y = replay(input, fs, array_index, channel);
w = noisegen(size(y), fs, array_index, noise);
r = y + 0.05 * w;
{{< /tab >}}
{{< tab header="Python" lang="python" >}}
from uwa_channels import replay, noisegen, load_channel, load_noise
channel = load_channel("blue_1.mat")
noise = load_noise("blue_noise.mat")
array_index = [0, 1, 2]
y = replay(input, fs, array_index, channel)
w = noisegen(y.shape, fs, array_index, noise)
r = y + 0.05 * w
{{< /tab >}}
{{< tab header="Julia" lang="julia" >}}
using UnderwaterAcoustics, MAT
noise = ReplayNoise("blue_noise.mat"; σ=0.05)
channel = BasebandReplayChannel("blue_1.mat"; rxs=1:3, noise)
r = transmit(channel, input; fs)
{{< /tab >}}
{{< /tabpane >}}

### Replay duration and starting point

The input is a real passband signal sampled at `fs` and must be shorter than the channel recording. The output extends beyond the input by approximately the impulse-response duration. Channels with `phi_hat` also need room for the largest delay drift reached during replay.

Each call to `replay` starts at a random point in the recording. To choose that point, pass `start` as the fifth argument. It specifies the starting sample at `params.fs_delay` and makes the replay repeatable. The output is not normalized: its power depends on the channel.

### Loading files and using Julia

In Python, `load_channel` and `load_noise` read both the released `-v7.3` files and MAT v5 files, and their output can be passed to `replay`, `noisegen`, and `unpack`. In MATLAB, the built-in `load` reads the files directly.

In Julia, `transmit` adds the noise itself, scaled by `σ`, so it returns $r_{\text{out}}(t)$ directly, and its `start` keyword plays the role of `start` in `replay`. `ReplayNoise` is added by [UnderwaterAcoustics.jl#95](https://github.com/org-arl/UnderwaterAcoustics.jl/pull/95), which is not merged yet; until it is, pass a noise model such as `WhiteGaussianNoise(0.05)` instead.

For a channel without a site-specific noise model, such as Brown, call `noisegen(size(y), fs)` in MATLAB or `noisegen(y.shape, fs)` in Python to generate the [generic noise](/noises), which is spatially uncorrelated with unit power on every element; in Julia, use `PinkGaussianNoise(σ)`, also added by that pull request.

### Noise level

The received signal is

$$r_{\text{out}}(t) = \bar{r}_{\text{out}}(t) + \sigma_n \hat{n}(t),$$

where $\bar{r}_{\text{out}}(t)$ is the noiseless replay output and $\hat{n}(t)$ is the generated noise. Adjust $\sigma_n$ to set the signal-to-noise ratio. In the example, $\sigma_n = 0.05$.

Noise is normalized across the full array. The expected powers of all $M$ elements sum to $M$, while their measured relative powers are preserved. Thus $\sigma_n^2$ is the average noise power per element, and quieter elements have a higher SNR. Selecting a subset with `array_index` preserves each element's power; the powers of the selected elements need not sum to the number selected. For Red's impulsive noise, pseudo-power $2c^2$ replaces power, where $c$ is the scale parameter.

### Complete examples

The [MATLAB example](https://github.com/uwa-channels/matlab/blob/main/examples/example_replay.m) and [Python example](https://github.com/uwa-channels/python/blob/main/examples/example_replay.py) show the full process. Follow the repository's `README` before running them, and put `blue_1.mat` and `blue_noise.mat` from Zenodo in the working folder.

> [!WARNING] Signal bandwidth
>
> Each channel captures only the acoustic bandwidth used in its experiment. Your signal must fit within that bandwidth. You can call `replay` directly on the stored channel; decompression is not required.

## Visualizing a channel

Use `unpack` to reconstruct the impulse response $\hat{h}(\tau, t)$, including delay drift, for plotting:

```text
unpack(fs_time, array_index, channel)
```

The result is a $K \times M \times T$ array: $K$ delay taps, $M$ selected array elements, and $T$ time snapshots. Choose the time sampling rate with `fs_time`; it must be positive and no greater than the delay sampling rate.

By default, `unpack` adds zero padding equal to 10% of the stored delay length on each side. The reconstructed array is therefore larger than `h_hat`. Use `buffer_left` and `buffer_right` to change the padding.

`unpack` checks the inputs before reconstruction. It requires channel version 1.0 or later, a nonempty selection of distinct, valid array elements, and nonnegative padding. If `f_resamp` is present, it must contain one positive factor for the whole array or one per element.

See the [MATLAB example](https://github.com/uwa-channels/matlab/blob/main/examples/example_unpack.m) or [Python example](https://github.com/uwa-channels/python/blob/main/examples/example_unpack.py), and follow the setup instructions in the repository's `README`.

In Julia, load `Plots` and use `plot(channel)` for the first element or `plot(channel, i)` for element `i`. UnderwaterAcoustics.jl does not provide `unpack`.

## Citing the library

If you use the channels, the noise models, or the code in your work, please cite the paper that describes the library, [arXiv:2609.03207](https://arxiv.org/abs/2609.03207):

```bibtex
@misc{li2026underwater,
  title         = {Underwater Acoustic Channel Library},
  author        = {Li, Zhengnan and Chitre, Mandar and Cuji, Diego A. and Preisig, James and Singer, Andrew C. and Stojanovic, Milica and van Walree, Paul},
  year          = {2026},
  eprint        = {2609.03207},
  archivePrefix = {arXiv},
  primaryClass  = {eess.SP},
  doi           = {10.48550/arXiv.2609.03207},
  url           = {https://arxiv.org/abs/2609.03207}
}
```
