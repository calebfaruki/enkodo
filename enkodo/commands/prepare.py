from enkodo.utils import load_clip, pipe_to_ffmpeg
from enkodo.analyze import analyze
from enkodo.filters.deband import deband, needs_debanding

def prepare(arguments):
    filename = arguments["<filename>"]
    clip = load_clip(filename)
    analysis = analyze(arguments)

    if needs_debanding(analysis):
        clip = deband(clip, analysis)

    clip.set_output()

    pipe_to_ffmpeg(clip, "master.mp4", crf=26)
