"""Wavelet ECG compression (fixed-block 2-D DWT): public interface (preview).

The implementation will be released later. Until then, every function below
raises NotImplementedError.

Copyright (c) 2026 Md Monzurul Islam Rabu. All rights reserved.
"""
from __future__ import annotations

import numpy as np

__all__ = ["compress", "decompress", "compression_ratio", "prd"]

RELEASE_MESSAGE = (
    "This is a preview of the interface. The implementation will be released "
    "later. See README.md."
)


def compress(x: np.ndarray, step: float) -> bytes:
    """Compress a single-lead ECG.

    Parameters
    ----------
    x : np.ndarray
        1-D float array: single-lead ECG.
    step : float
        Quantization step for the wavelet coefficients. Larger values give a
        smaller payload and a larger reconstruction error.

    Returns
    -------
    bytes
        Self-contained payload, including all side information needed to
        decode it.
    """
    raise NotImplementedError(RELEASE_MESSAGE)


def decompress(payload: bytes) -> np.ndarray:
    """Reconstruct the ECG from a payload produced by :func:`compress`.

    Returns
    -------
    np.ndarray
        1-D float array with the same length as the original signal.
    """
    raise NotImplementedError(RELEASE_MESSAGE)


def compression_ratio(x: np.ndarray, payload: bytes) -> float:
    """Compression ratio of ``payload`` relative to ``x``.

    Defined as the size of a 16-bit uncompressed signal (2 bytes per sample)
    divided by the payload size in bytes, side information included.
    """
    raise NotImplementedError(RELEASE_MESSAGE)


def prd(x: np.ndarray, x_hat: np.ndarray) -> float:
    """Percent root-mean-square difference (PRD, %) between the original
    signal ``x`` and the reconstruction ``x_hat``."""
    raise NotImplementedError(RELEASE_MESSAGE)
