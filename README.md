<!-- SWIR-README-STANDARD:v2 -->

<div align="center">

<img width="100%" src="assets/readme/hero.svg" alt="WAV to MP3 Converter — local audio conversion and DSP desktop tool" />

# WAV to MP3 Converter

**Local WAV/MP3 conversion, batch processing and optional audio DSP in a CustomTkinter desktop interface.**

![Python](https://img.shields.io/badge/Python-3.x-02050A?style=for-the-badge&logo=python&logoColor=62E5FF)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-02050A?style=for-the-badge&logoColor=62E5FF)
![Engine](https://img.shields.io/badge/Engine-FFmpeg%20%2B%20pydub-02050A?style=for-the-badge&logo=ffmpeg&logoColor=62E5FF)
![Formats](https://img.shields.io/badge/Audio-WAV%20%7C%20MP3-02050A?style=for-the-badge&logoColor=62E5FF)

[![Author](https://img.shields.io/badge/by-Swir-0088FF?style=flat-square&logo=github)](https://github.com/Swir)
[![Release](https://img.shields.io/badge/Windows%20release-v1.0.0-0088FF?style=flat-square)](https://github.com/Swir/WAV-to-MP3-converter/releases/tag/v1.0.0)
[![Stars](https://img.shields.io/github/stars/Swir/WAV-to-MP3-converter?style=flat-square&color=0088FF)](https://github.com/Swir/WAV-to-MP3-converter/stargazers)

[**Highlights**](#-highlights) · [**Quick Start**](#-quick-start) · [**Workflow**](#-workflow) · [**Releases**](#-releases) · [**Limitations**](#-limitations-and-responsible-use)

</div>

<img width="100%" src="https://raw.githubusercontent.com/Swir/Swir/main/assets/power-divider-v4.svg" alt="SWIR electric divider" />

## 📍 Project Status

| Item | Status |
|---|---|
| Current stage | Existing desktop utility; no canonical product roadmap is maintained |
| Published package | Windows x64 [`v1.0.0`](https://github.com/Swir/WAV-to-MP3-converter/releases/tag/v1.0.0) |
| Source runtime | Python + CustomTkinter + pydub with FFmpeg/FFprobe available in `PATH` |
| Product progress | **N/A** — no authoritative completion denominator exists |

<p align="center">
  <img width="100%" src="assets/readme/progress-card.svg" alt="WAV to MP3 Converter product progress — N/A because no canonical roadmap exists" />
</p>

The progress graphic intentionally shows **N/A** instead of an invented completion percentage. It measures product-roadmap progress only; release existence and documentation work are not substitutes for a roadmap.

## 🚀 Overview

**WAV to MP3 Converter** is a local desktop audio-processing utility built with Python, CustomTkinter and pydub. It accepts WAV and MP3 files, supports single-file or folder-based processing, exposes several optional DSP transformations, and exports the results into a `Cleaned_Export` directory.

The current code checks for both `ffmpeg` and `ffprobe` before enabling processing. Audio is handled locally by the application and FFmpeg backend; this repository does not provide cloud processing or hosted uploads.

## ✨ Highlights

| Feature | What it does |
|---|---|
| 🎵 WAV / MP3 input | Select one local audio file or scan a folder for supported files. |
| 📁 Batch mode | Process all `.wav` and `.mp3` files found in the selected folder. |
| 🔄 Format conversion | Preserve the original format or force MP3/WAV output. |
| 🎚️ Frequency filtering | Optional 20 Hz high-pass and 16 kHz low-pass processing. |
| 🎧 Stereo timing step | Optional stereo timing adjustment implemented by the current pydub workflow. |
| 📼 Noise texture | Optional low-level filtered white-noise overlay. |
| 📈 Peak-level step | Optional gain adjustment toward a -1.0 dBFS peak target. |
| 🧭 Export presets | Original, MP3, WAV and a distribution-oriented 44.1 kHz / 320 kbps preset. |
| 📊 Progress + log | Shows per-batch progress and operation messages in the GUI. |
| ⚙️ Engine check | Processing remains disabled when FFmpeg/FFprobe are not detected. |

## ⚙️ Quick Start

### Existing Windows package

The repository has a real [v1.0.0 Windows release](https://github.com/Swir/WAV-to-MP3-converter/releases/tag/v1.0.0) containing:

- `WAV-to-MP3-Converter.exe`
- `WAV-to-MP3-Converter-v1.0.0-Windows-x64.zip`
- a SHA-256 sidecar for the ZIP

**FFmpeg and FFprobe are still external requirements** for the packaged application and must be installed and available in `PATH`.

### From source

```bash
git clone https://github.com/Swir/WAV-to-MP3-converter.git
cd WAV-to-MP3-converter
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install customtkinter pydub
python run.py
```

Verify the external media engine separately:

```bash
ffmpeg -version
ffprobe -version
```

## 📋 Requirements / Compatibility

| Component | Current requirement |
|---|---|
| Python | Python 3.x; the release workflow builds with Python 3.11 |
| GUI | CustomTkinter / Tk |
| Audio library | pydub |
| Media engine | FFmpeg + FFprobe on `PATH` |
| Published binary | Windows x64 |
| Source platforms | Not claimed beyond environments where Python/Tk/pydub and FFmpeg work correctly |

The documentation migration does not change dependency versions, runtime behavior or the existing packaged binary.

## 🎛️ Workflow

1. Start the application and confirm the FFmpeg/FFprobe status is green.
2. Select one WAV/MP3 file or an entire folder.
3. Enable or disable the optional DSP switches.
4. Choose the output mode: keep the original extension, force MP3, force WAV, or use the distribution-oriented preset.
5. Start processing. Results are written to a `Cleaned_Export` subdirectory next to the selected source location.
6. Review the output before publishing or replacing any original material.

### What the current DSP path actually does

The implementation can apply short fades, frequency filters, a stereo timing operation, a 0.5% sample-rate reinterpretation followed by 44.1 kHz resampling, a filtered -45 dB white-noise overlay, peak-oriented gain adjustment and metadata replacement.

These transformations change the audio signal. They **do not prove removal of an AI watermark, do not guarantee evasion of automated classifiers or content-identification systems, and do not guarantee acceptance by any distributor or platform**. Treat labels in the current GUI such as “AI Cleaner” as historical UI wording, not as a verified capability claim.

## 🧠 Technology / Project Layout

| Path | Role |
|---|---|
| [`run.py`](run.py) | CustomTkinter UI, batch selection, pydub DSP and export workflow |
| [`.github/workflows/release.yml`](.github/workflows/release.yml) | Windows PyInstaller build and v-tag release packaging |
| [`assets/readme/`](assets/readme/) | SWIR README PRO hero, project icon and progress graphics |
| [`tools/generate_progress_svg.py`](tools/generate_progress_svg.py) | Deterministic generation/check for the progress card and mini bar |

## 🗺️ Progress

<p align="center">
  <img width="100%" src="assets/readme/progress-mini.svg" alt="WAV to MP3 Converter roadmap progress — N/A" />
</p>

There is currently **no canonical roadmap or verified product-completion denominator** in this repository, so product progress is reported as **N/A** rather than estimated. The SVGs can be checked for staleness with:

```bash
python tools/generate_progress_svg.py --check
```

## 📦 Releases

The latest published release verified during this documentation update is [**v1.0.0**](https://github.com/Swir/WAV-to-MP3-converter/releases/tag/v1.0.0), published on September 12, 2026. The release workflow builds a one-file Windows executable and ZIP, then creates or updates the matching GitHub Release.

[**Browse all GitHub Releases →**](https://github.com/Swir/WAV-to-MP3-converter/releases)

## ⚠️ Limitations and Responsible Use

- FFmpeg and FFprobe are mandatory even when using the packaged Windows EXE.
- No lossless-quality guarantee is made when exporting to MP3; MP3 is a lossy codec.
- Peak adjustment in the current code is not a full loudness-normalization or mastering-analysis suite.
- Metadata is replaced with a small fixed tag set during export; preserve originals if metadata matters.
- The repository does not maintain an authoritative product roadmap, so progress remains N/A.
- Use the tool only on audio you own or are authorized to edit and distribute. Processing does not change copyright ownership, licensing obligations, disclosure requirements or platform rules.
- Do not rely on the DSP options to conceal provenance or bypass a service's detection or eligibility policies.

## 🔎 Search Keywords

`wav to mp3 converter python` • `python audio converter gui` • `ffmpeg audio gui` • `pydub audio processing` • `batch wav mp3 converter` • `python audio dsp` • `desktop audio converter` • `customtkinter audio converter` • `wav mp3 batch processing` • `local audio conversion` • `ffmpeg pydub desktop app` • `audio export utility`

<img width="100%" src="https://raw.githubusercontent.com/Swir/Swir/main/assets/power-divider-v4.svg" alt="SWIR electric divider" />

<div align="center">

<img src="assets/readme/project-icon.svg" width="64" alt="WAV to MP3 Converter project icon" />

### `CONVERT • PROCESS • REVIEW • EXPORT`

**WAV to MP3 Converter — by Swir**

[**← SWIR profile**](https://github.com/Swir) · [**All projects →**](https://github.com/Swir?tab=repositories) · [**Report an issue**](https://github.com/Swir/WAV-to-MP3-converter/issues)

</div>
