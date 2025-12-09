import vapoursynth
core = vapoursynth.core

def deblock(clip):
    print("Deblocking...")
    # quant: 0-60, higher = stronger deblocking
    clip = core.deblock.Deblock(clip, quant=60)

    return clip

def needs_deblocking(analysis) -> bool:
    # Very low bitrate = likely blocking artifacts
    return analysis.bitrate < 1_000_000  # Under 1 Mbps