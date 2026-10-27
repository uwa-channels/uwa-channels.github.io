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

The Python package requires Python 3.10 or later; `pip` installs its dependencies (NumPy, SciPy, Matplotlib, and h5py).

Julia support is provided by the [`UnderwaterAcoustics.jl`](https://github.com/org-arl/UnderwaterAcoustics.jl) package, maintained separately by the Acoustic Research Laboratory, with the [`MAT`](https://github.com/JuliaIO/MAT.jl) package to read the files. It requires Julia 1.9 or later. The released version (v0.8.1) cannot apply `phi_hat` or `f_resamp`, which most channels use, so install the development version from GitHub as shown above until the next release. See the [replay guide](https://org-arl.github.io/UnderwaterAcoustics.jl/replay.html) of that package for more detail.

Once a package is installed, download the channel MAT-files from [Zenodo](https://doi.org/10.5281/zenodo.21287414) and place them where MATLAB, Octave, or Python can find them. The channel files are distributed separately from the code because of their size. In Julia, a name such as `uacr://blue_1` instead of a file path downloads that file from Zenodo and caches it.

## Applying a channel to an arbitrary signal

* To pass a signal of your choice through a channel, generate the desired signal in passband, respecting the bandwidth and sampling-rate limits of the chosen channel (see the [Channels](/channels) tab).
* Run `replay` on the signal.
* Scale the output of `noisegen` and add it to the output of `replay` to obtain the desired signal-to-noise ratio. That is, form $r_{\text{out}}(t) = \bar{r}_{\text{out}}(t) + \sigma_n \hat{n}(t)$, where $\bar{r}_{\text{out}}(t)$ is the noiseless replay output, $\hat{n}(t)$ is the generated noise, and $\sigma_n$ is the noise level that sets the SNR. The noise model is normalized over the whole array: the expected noise powers of all $M$ elements in the noise file sum to $M$, and each element keeps its measured power relative to the others, so elements with lower noise give a higher SNR. $\sigma_n^2$ is then the noise power per element, averaged over all $M$ elements. A subset selected with `array_index` keeps the powers of its elements, so its sum is not, in general, the number of selected elements. For the impulsive Red noise, the pseudo-power $2c^2$, with $c$ the scale parameter, takes the place of the power. In the example below, $\sigma_n$ is `0.05`.
* Pass the same `array_index` to `replay` and `noisegen`, so that the noise matches the selected elements. Indices are 1-based in MATLAB and Julia, and 0-based in Python.

{{< tabpane >}}
{{< tab header="Replay and generate noise" disabled=true />}}
{{< tab header="MATLAB/Octave" lang="matlab" >}}
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

The input is a real passband signal sampled at `fs`. It must be shorter than the channel, and the output is longer than the input by about the length of the impulse response. `replay` starts at a random point in the channel on each call; pass a fifth argument, `start`, to choose the starting sample (at `params.fs_delay`) and make the output repeatable. The output of `replay` is not normalized, so its power follows that of the channel.

In Python, `load_channel` and `load_noise` read both the released `-v7.3` files and MAT v5 files, and their output can be passed to `replay`, `noisegen`, and `unpack`. In MATLAB, the built-in `load` reads the files directly.

In Julia, `transmit` adds the noise itself, scaled by `σ`, so it returns $r_{\text{out}}(t)$ directly, and its `start` keyword plays the role of `start` in `replay`. `ReplayNoise` is added by [UnderwaterAcoustics.jl#95](https://github.com/org-arl/UnderwaterAcoustics.jl/pull/95), which is not merged yet; until it is, pass a noise model such as `WhiteGaussianNoise(0.05)` instead.

For a channel without a site-specific noise model, such as Brown, call `noisegen(size(y), fs)` in MATLAB or `noisegen(y.shape, fs)` in Python to generate the [generic noise](/noises), which is spatially uncorrelated with unit power on every element; in Julia, use `PinkGaussianNoise(σ)`, also added by that pull request.

A simple example of this process is given in [`MATLAB`](https://github.com/uwa-channels/matlab/blob/main/examples/example_replay.m) and [`Python`](https://github.com/uwa-channels/python/blob/main/examples/example_replay.py). Before running the example code, please read the corresponding `README` file; the examples expect `blue_1.mat` and `blue_noise.mat` from Zenodo in the working folder.

> [!WARNING] Important note
>
> The channels are specified for a certain acoustic bandwidth that was used during the experiment. When working with a channel, note that only that bandwidth is captured. If you are designing a signal to pass through a channel, the bandwidth of your signal must fit within the stated limit. Note that you do **not** need to decompress the channel first to replay the signal.

## Visualizing a channel

To visualize a channel as a collection of impulse responses evolving over time, you will need to decompress the channel impulse responses via `unpack`. This will produce the decompressed impulse response $\hat{h}(\tau, t)$, which is larger than the stored original and contains all the physical effects of delay drift. The call is `unpack(fs_time, array_index, channel)`, and the output is a $K \times M \times T$ array, where $K$ is the number of delay taps, $M$ is the number of elements selected by `array_index`, and $T$ is the number of time snapshots. The delay axis is zero-padded by 10% of the stored length on each side, so $K$ is larger than the first dimension of `h_hat`; the optional arguments `buffer_left` and `buffer_right` set the padding. This array can be generated at an arbitrary sampling rate in time, provided that rate does not exceed the sampling rate in delay.

A simple example of this process is given in [`MATLAB`](https://github.com/uwa-channels/matlab/blob/main/examples/example_unpack.m) and [`Python`](https://github.com/uwa-channels/python/blob/main/examples/example_unpack.py). Before running the example code, please read the corresponding `README` file. In Julia, `plot(channel)` (with `using Plots`) shows the impulse response of the first element, and `plot(channel, i)` that of element `i`; UnderwaterAcoustics.jl has no `unpack`.

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
