---
title: "MAT-file format specifications"
linkTitle: "MAT-file format specifications"
weight: 1
description: >
cascade:
  - type: "docs"
---

## UWA-Channels MAT File Format Specification

The `uwa-channels`-compatible `.mat` files must be saved with the following flags:

* `-v7.3`: Supports large variables and the HDF5 file format, ensuring better compatibility with other programming languages such as Python and Julia.
* `-nocompression`: Accelerates loading speed.

### Required Fields

Each `.mat` file must include the following variables:

#### **`h_hat`**

* **Type**: Multi-dimensional numeric tensor (single or double precision). Arbitrarily scaled.
* **Dimensions**: `[delay, receiver, time]`
* **Description**: The estimated time-varying channel impulse response (TVIR), complex baseband.

#### **`params`**

A MATLAB structure containing the following scalar fields:

* `fs_delay` (Hz): Sampling rate of `h_hat` along the *delay* axis.
* `fs_time` (Hz): Sampling rate of `h_hat` along the *time* axis.
* `fc` (Hz): The probing waveform was basebanded with respect to `fc` prior to the TVIR estimation; `fc` typically corresponds to the center frequency of the probing waveform. 

#### **`version`**

* **Type**: Numeric scalar
* **Description**: Dataset format version number.

### Optional Fields

#### **`theta_hat`**

* **Type**: Numeric matrix of size `[receiver, time]` (single or double precision).
* **Sampling Rate**: Must match `params.fs_time`
* **Duration Constraint**: The time duration of `theta_hat` must match the third dimension of `h_hat`, i.e., `size(theta_hat, 2) * params.fs_time == size(h_hat, 3) *  params.fs_delay`.
* **Description**: For each hydrophone (receiver), theta_hat represents a time-varying *resampling factor* $R(t)$ to be applied to the output signal in conjunction with $h(t,\tau)$:
$$ R(t) = 1 - \frac{1}{2 \pi f_c} \frac{\text{d} \hat{\theta}(t)}{\text{d} t} $$
where $f_c$ is the center frequency, and the $\hat{\theta}(t)$ is the `theta_hat`.

#### **`f_resamp`**

* **Type**: Scalar (single or double precision)
* **Units**: Unitless resampling factor
* **Description**: A *time-invariant* resampling factor applied to the output signal after convolution. This is typically the *inverse* of a resampling operation used to remove nominal Doppler offsets during channel estimation. It is applied *after* the time-varying convolution.

#### **`meta`**

The `meta` structure is optional but encouraged for documenting dataset context. The suggested fields include:

* `meta.experiment_name` (string): Name of the experiment.
* `meta.experiment_info` (string or struct): Descriptive details about the experimental setup.
* `meta.array_info` (string or struct): Information about the hydrophone array (e.g., geometry, number of elements).
* `meta.authorship` (string or struct): Data contributor names and affiliations.

Users are free to add *any number of additional fields* to `meta` to record experiment-specific metadata.

### Dataset Configurations

The following configurations are currently supported:

* `h_hat` only — supported but not used in official datasets.
* `h_hat` and `theta_hat` — used in the *blue*, *red*, *green*, *purple*, *yellow*, *abyssal*, and *namikaze* datasets.
* `h_hat` and `f_resamp` — used in *Watermark* datasets.
* `h_hat`, `theta_hat`, and `f_resamp` — used in the *Sky* dataset.
