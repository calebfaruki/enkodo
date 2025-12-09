import vapoursynth
core = vapoursynth.core

from enkodo.analyze import VideoAnalysis

def deband(clip: vapoursynth.VideoNode, analysis: VideoAnalysis) -> vapoursynth.VideoNode:
    original_bit_depth = analysis.bit_depth

    # neo_f3kdb only accepts 8-bit and 16-bit source
    if original_bit_depth not in (8, 16):
        clip = core.fmtc.bitdepth(clip, bits=16)

    # Use f3kdb to detect banding and smooth it out using bit output.
    clip = core.neo_f3kdb.Deband(
        clip,
        range=31, # pixel radius for gradient detection
        y=255, # Luma strength, (moderate, not extreme)
        cb=255, # Chroma blue strength
        cr=255, # Chroma red strength
        grainy=255, # Luma grain to mask smoothing
        grainc=255, # Chroma gain
        output_depth=16
    )

    # Sanity check
    # clip = core.std.Invert(clip)

    # 16-bit -> 10-bit. Higher bit depth input gives more headroom for dithering.
    clip = core.fmtc.bitdepth(clip, bits=10, dmode=6)

    return clip

def needs_debanding(analysis) -> bool:
    return analysis.bit_depth < 10
