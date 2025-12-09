from enkodo.utils import load_clip, pipe_to_ffmpeg
from enkodo.analyze import analyze
from enkodo.filters.deband import deband, needs_debanding
from enkodo.filters.deinterlace import deinterlace, needs_deinterlacing
from enkodo.filters.deblock import deblock, needs_deblocking

def prepare(arguments):
    filename = arguments["<filename>"]
    clip = load_clip(filename)
    analysis = analyze(arguments["<filename>"])

    if needs_debanding(analysis):
        print("Debanding...")
        clip = deband(clip, analysis)
    if needs_deinterlacing(analysis):
        print("Deinterlacing...")
        clip = deinterlace(clip, analysis.field_order)
    if needs_deblocking(analysis):
        clip = deblock(clip)

    clip.set_output()

    pipe_to_ffmpeg(clip, "master.mp4", crf=26)
