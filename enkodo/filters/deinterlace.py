import vapoursynth
core = vapoursynth.core
from enkodo.analyze import VideoAnalysis
import enkodo.utils as utils

def deinterlace(clip: vapoursynth.VideoNode, field_order: str):
    # Use OpenCL version - no weights file needed
    field_number = 2
    if field_order == "bb":
        field_number = 1

    clip = core.std.SetFieldBased(clip, field_number)
    clip = core.nnedi3cl.NNEDI3CL(clip, field=field_number+1, nns=4, nsize=6, qual=2)
    clip = core.std.SelectEvery(clip, cycle=2, offsets=0)

    return clip

def needs_deinterlacing(analysis: VideoAnalysis) -> bool:
    return analysis.field_order != "progressive"
