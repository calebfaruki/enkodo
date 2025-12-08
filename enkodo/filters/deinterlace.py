import vapoursynth
core = vapoursynth.core
import enkodo.utils as utils


def deinterlace(arguments):
    filename = arguments["<filename>"]

    clip = utils.load_clip(filename)

    # Use OpenCL version - no weights file needed
    clip = core.nnedi3cl.NNEDI3CL(clip, field=1)

    utils.pipe_to_ffmpeg(clip, "examples/interlacing/deinterlaced.mp4")
