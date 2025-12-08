from dataclasses import dataclass
import subprocess
import json

@dataclass
class VideoAnalysis:
    container: str
    codec: str
    resolution: str
    duration: str
    bitrate: int # kbps
    bit_depth: int # number of color levels
    field_order: str # assume progressive
    framerate: str


def analyze(arguments) -> VideoAnalysis:
    print("Analyzing...")

    filename = arguments['<filename>']

    command = f"""
        ffprobe -print_format json -show_format -show_streams -v quiet {filename}
    """

    result = subprocess.run(command, capture_output=True, shell=True)
    
    parsed_result = json.loads(result.stdout)

    # Get container
    container = parsed_result["format"]["format_long_name"]

    streams = parsed_result["streams"]

    # Find default video stream.
    vstream = [stream for stream in streams if stream["codec_type"] == "video" and stream["disposition"]["default"] == 1][0]

    # Get resolution
    height = vstream["height"]
    width = vstream["width"]
    resolution = f"{height}x{width}"

    # Get duration
    total_seconds = int(float(vstream["duration"]))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # Get bitrate in kbps
    bitrate = int(vstream["bit_rate"])

    # Get color levels (bit depth)
    bit_depth = int(vstream["bits_per_raw_sample"])

    analysis = VideoAnalysis(
        container=container,
        codec=vstream["codec_name"],
        resolution=resolution,
        duration=duration,
        bitrate=bitrate,
        bit_depth=bit_depth,
        field_order=vstream.get("field_order", "progressive"),
        framerate=vstream["r_frame_rate"])
    )
    return analysis
