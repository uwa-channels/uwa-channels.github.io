---
title: "Channel file format specifications"
linkTitle: "Channel file format specifications"
weight: 1
description: >
  Specification of the required and optional fields in the channel and noise .mat files, including the impulse response, phase/delay tracking, and metadata formats.
cascade:
  - type: "docs"
---

The `uwa-channels`-compatible `.mat` files **must** be saved with the following flags:

* `-v7.3` to support large variables and the `HDF5` file format.
* `-nocompression` to speed up loading.

## Required fields

Each `.mat` file must include the following variables:

### `h_hat`

* **Type**: Multi-dimensional complex tensor.
* **Dimensions**: `[delay, receiver, time]`
* **Units**:
  * Delay axis: sampled at `params.fs_delay` [Hz]
  * Time axis: sampled at `params.fs_time` [Hz]
  * Amplitude: complex baseband impulse response (unitless)
* **Description**: The estimated time-varying channel impulse response (TVIR).

### `params`

A structure with the following scalar fields:

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `fs_delay` | scalar | Hz | Sampling rate along the delay axis. |
| `fs_time` | scalar | Hz | Sampling rate along the time axis. |
| `fc` | scalar | Hz | Center frequency of the signal used during channel estimation. |

### `version`

* **Type**: Numeric scalar.
* **Description**: Dataset format version number (currently `1.0`).

## Phase/delay tracking fields (optional)

`phi_hat`, `theta_hat`, and `f_resamp` may coexist; the replay engine applies them according to the following precedence:

* If none of the three is present, no Doppler correction is applied.
* `phi_hat` takes precedence over `theta_hat`: if `phi_hat` is present, it is used and `theta_hat` is ignored; if only `theta_hat` is present, it is used instead.
* `f_resamp` (see [Optional fields](#optional-fields)) is applied independently of the two phase/delay fields, whether or not either of them is present.

### `phi_hat` (delay tracking)

* **Type**: Numeric matrix, size `[receiver, time]`
* **Units**: Radians
* **Sampling rate**: `params.fs_delay`
* **Description**: Time-varying phase that encodes *both* phase rotation and delay drift. In this mode, `h_hat` is *static* (drift-free). The delay drift is recovered from `phi_hat` as:

$$\Delta\tau(t) = \frac{\hat\varphi(t)}{2\pi f_c}$$

The unpacking procedure reinserts both the phase (via multiplication by $e^{j\hat\varphi(t)}$) and the delay drift (via interpolation).

### `theta_hat` (phase tracking only)

* **Type**: Numeric matrix, size `[receiver, time]`
* **Units**: Radians
* **Sampling rate**: `params.fs_delay`
* **Description**: Time-varying phase correction. In this mode, `h_hat` contains the *drifting* impulse response (delay drift is embedded in the taps). Only the phase is tracked separately. The baseband received signal is modeled as:

$$v(t) = \sum_n d(n)\, h(t, t - nT)\, e^{j\hat\theta(t)} + z(t)$$

where $d(n)$ is the data symbol, $h(t, \tau)$ is the time-varying impulse response with drifting taps, $T$ is the symbol duration, $\hat\theta(t)$ is the tracked phase, and $z(t)$ is the additive noise.

### Duration constraint

The time dimension of `theta_hat` or `phi_hat` and the third dimension of `h_hat` must span the same duration. The check is written below for `theta_hat`; the same applies to `phi_hat`:

```
size(theta_hat, 2) / params.fs_delay == size(h_hat, 3) / params.fs_time
```

## Optional fields

### `f_resamp`

* **Type**: Scalar (double precision)
* **Units**: Unitless resampling factor
* **Description**: A time-invariant resampling factor applied to the output signal. This is typically the inverse of a resampling operation applied to remove the nominal Doppler frequency offset before channel estimation. It is applied after the time-varying convolution.

### `meta`

The `meta` structure is optional but strongly encouraged. The following fields are recognized by the toolbox:

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Free-text description of the experiment. |
| `nsd` | scalar | Samples per symbol in the delay domain. |
| `nst` | scalar | Samples per symbol in the time domain. |
| `K_1` | scalar | Anti-causal filter length [symbols]. |
| `K_2` | scalar | Causal filter length [symbols]. |
| `fc` | scalar | Center frequency [Hz]. |
| `element_spacing` | scalar | Array element spacing [m]. |
| `vertical` | logical | `true` if vertical array. |
| `delay_tracking` | logical | `true` if delay tracking is enabled (`phi_hat` present). |
| `limit` | scalar | Lower dB limit for plotting. |
| `optim` | scalar | Optimizer used: `1` LMS, `2` RLS, `3` SFTF. |
| `mu` | scalar | LMS step size (when `optim == 1`). |
| `lambda` | scalar | Forgetting factor (when `optim == 2` or `3`). |
| `regularization` | scalar | Regularization factor (when `optim == 2` or `3`). |
| `Kf_1` | scalar | PLL loop filter coefficient 1. |
| `Kf_2` | scalar | PLL loop filter coefficient 2. |
| `nslr` | scalar | Delay tracking rate (when `delay_tracking == true`). |
| `codename` | string | Short identifier for the channel (e.g., `"blue_1"`). |

Users are free to add additional fields to `meta` to capture experiment-specific metadata.

## Noise file format

Each noise `.mat` file contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `Fs` | scalar | Sampling rate at which noise statistics were measured [Hz]. |
| `R` | scalar | Bandwidth of the recorded noise [Hz]. Not to be confused with the symbol rate $R$ used on the channel pages. |
| `alpha` | scalar | Stability index of the symmetric α-stable (SαS) distribution: `2` Gaussian, `< 2` impulsive. |
| `beta` | tensor `[M, M, L+1]` | Mixing coefficients for spatiotemporal noise coloring, where `M` is the number of array elements and `L` is the maximum lag (both defined below). |
| `fc` | scalar | Center frequency [Hz]. |
| `version` | scalar | Noise struct version number. |

The noise generation function `noisegen` uses the mixing equation:

$$n_i(nT_s) = \sum_{j=0}^{M-1}\sum_{k=0}^{L}\beta_{ij}(kT_s)\,\eta_j(nT_s - kT_s)$$

where $T_s = 1/F_s$ is the sampling interval, $L$ is the maximum discrete time lag with non-negligible covariance (so $\beta_{ij}(kT_s)$ has $L+1$ taps, $k = 0, \ldots, L$), and $\eta_j \sim S\alpha S(0, 1, 0)$ are i.i.d. symmetric α-stable innovations with zero location, unit scale, and zero skew. When $\alpha = 2$, this reduces to Gaussian noise.
