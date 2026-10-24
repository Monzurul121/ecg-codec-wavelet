# Wavelet ECG Compression (Fixed-Block 2-D DWT)

A lossy ECG codec that arranges the signal into a two-dimensional matrix of fixed-length blocks, applies a separable discrete wavelet transform, and stores only the significant coefficients with Huffman coding.

> **Status: preview.** This repository documents the method and its interface. The implementation will be released later.

## Overview

Transform coding is one of the most widely used approaches to ECG compression. A wavelet transform concentrates most of the signal's energy into a small number of coefficients. The remaining coefficients can then be quantized to zero with little visible change to the waveform.

This codec arranges the ECG as a 2-D matrix, so the wavelet transform can exploit structure both within each block and across neighboring blocks. It uses fixed-length blocks instead of beat-aligned segments, so the encoder does not depend on a QRS detector or on beat annotations.

## How it works

1. **Mean removal.** The record's mean is subtracted and stored, so the transform works on a zero-centered signal.
2. **Blocking.** The signal is cut into consecutive blocks of 1024 samples. Each block becomes one row of a 2-D matrix, and the last block is zero-padded.
3. **Separable 2-D wavelet transform.** A multilevel 1-D discrete wavelet transform is applied along the columns of the matrix and then along its rows.
4. **Uniform quantization.** Every coefficient is divided by a quantization step and rounded, so small coefficients become zero. The step is the codec's main setting.
5. **Sparse representation.** Only the nonzero coefficients are kept, as three streams: their magnitudes, their signs and the gaps between their positions.
6. **Huffman coding.** Each stream is Huffman coded. The block lengths and the transform layout are stored as side information.
7. **Decoding.** The decoder rebuilds the sparse coefficient matrix, applies the inverse 2-D transform, removes the padding and adds back the mean.

## Key properties

- **One setting:** the quantization step controls the trade-off between compression ratio and distortion.
- **No beat detection needed:** fixed-length blocks make the encoder independent of QRS detection.
- **Self-contained payload:** all side information needed for decoding is stored in the payload and counted in the compression ratio.
- **No training:** the codec is fully deterministic.

## Measuring performance

- **Compression ratio (CR):** the size of the signal stored as 16-bit samples, divided by the size of the compressed payload, side information included.
- **Percent root-mean-square difference (PRD):** the root-mean-square reconstruction error as a percentage of the root-mean-square value of the original signal.

## Limitations

- The codec is lossy. Higher compression comes with a larger reconstruction error, so the quantization step should be chosen for the intended use.
- Fixed-length blocks do not line up with heartbeats. The 2-D arrangement therefore captures less beat-to-beat similarity than beat-aligned framing.

## Typical uses

ECG storage and transmission in wearable and remote-monitoring devices, where a controlled amount of distortion is acceptable in exchange for much higher compression.

## Interface (preview)

```python
from wavelet_codec import compress, decompress, compression_ratio, prd

payload = compress(x, step=step)        # x: 1-D array, single-lead ECG
x_hat = decompress(payload)

print(compression_ratio(x, payload))    # 16-bit original size / payload size
print(prd(x, x_hat))                    # reconstruction error in percent
```

In this preview, these functions raise `NotImplementedError`. They show the interface that the released code will provide.

## Roadmap

- Release the implementation.
- Add usage examples and documentation.

## Reference

This codec adapts the method of:

> H. S. Pal, A. Kumar, A. Vishwakarma, and G. K. Singh, "A 2D electrocardiogram signal compression algorithm using 1D discrete wavelet transform," *Physical and Engineering Sciences in Medicine*, vol. 48, no. 2, pp. 903–914, 2025. doi: [10.1007/s13246-025-01556-8](https://doi.org/10.1007/s13246-025-01556-8)

**Main change:** fixed-length blocks replace the original beat-aligned framing.

If you use this method, please cite the original paper.

## Copyright

Copyright © 2026 Md Monzurul Islam Rabu. All rights reserved.

No permission is granted to use, copy, modify or redistribute the contents of this repository. An open-source license will be added when the code is released.
