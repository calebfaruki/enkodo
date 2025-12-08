import os
import subprocess
import vapoursynth
core = vapoursynth.core

def pipe_to_ffmpeg(clip: vapoursynth.VideoNode, output: str, crf: int = 12):
    clip.set_output()

    command = f"""
        ffmpeg -y -f yuv4mpegpipe -i - -c:v libx264 -crf {crf} -pix_fmt yuv420p {output}
    """
    ffmpeg = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)
    clip.output(ffmpeg.stdin, y4m=True)
    ffmpeg.communicate()

def load_clip(filename) -> "vapoursynth.VideoNode":
    return core.lsmas.LWLibavSource(filename, cachefile=f"/tmp/{os.path.basename(filename)}.lwi")
