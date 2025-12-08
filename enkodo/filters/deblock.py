import vapoursynth
core = vapoursynth.core
import enkodo.utils as utils

def deblock(arguments):
    print("Deblocking...")
    filename = arguments["<filename>"]

    clip = utils.load_clip(filename)

    # quant: 0-60, higher = stronger deblocking
    clip = core.deblock.Deblock(clip, quant=60)

    utils.pipe_to_ffmpeg(clip, "examples/blocking/deblocked.mp4", crf=20)
