import vapoursynth
core = vapoursynth.core

import enkodo.utils as utils
from enkodo.analyze import analyze, VideoAnalysis

def deband(clip: vapoursynth.VideoNode, analysis: VideoAnalysis) -> vapoursynth.VideoNode:
    original_bit_depth = analysis.bit_depth

    # Convert to 16 bit color depth for gradient calculation
    if original_bit_depth < 16:
        clip = core.fmtc.bitdepth(clip, bits=16)

    # Use f3kdb to detect banding and smooth it out
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

    # If original bit depth < 16 bit depth, convert back with dithering
    # to add appearance of smooth gradients despite fewere color levels.
    if original_bit_depth < 16:
        clip = core.fmtc.bitdepth(clip, bits=original_bit_depth, dmode=6)

    return clip

def needs_debanding(analysis) -> bool:
    return analysis.bit_depth < 10
