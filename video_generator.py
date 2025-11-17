import os
import subprocess
import logging

VIDEODIR = "assets/output"
os.makedirs(VIDEODIR, exist_ok=True)
logger = logging.getLogger("videogenerator")

def makevideofromassets(imagepaths, audiopath):
    """
    Creates a simple slideshow video using FFmpeg with fade transitions for each image.
    Each image shows for 1.3 seconds, with a 0.5s fade out.
    """

    outputpath = os.path.join(VIDEODIR, "finalvideo.mp4")

    # Build filter_complex for fades
    filter_complex = ""
    duration = 1.3
    fade_duration = 0.5
    inputs = ""
    for idx, img in enumerate(imagepaths):
        inputs += f" -loop 1 -t {duration} -i {img}"
        filter_complex += f"[{idx}:v]fade=out:st={duration-fade_duration}:d={fade_duration}[v{idx}];"
    # Concatenate images with fade
    streams = "".join([f"[v{i}]" for i in range(len(imagepaths))])
    filter_complex += f"{streams}concat=n={len(imagepaths)}:v=1:a=0,scale=1080:1920[v]"

    cmd = f"ffmpeg -y{inputs} -i {audiopath} -filter_complex \"{filter_complex}\" -map \"[v]\" -map {len(imagepaths)}:a -c:v libx264 -c:a aac -shortest {outputpath}"
    logger.info("Running FFmpeg to create video...")
    subprocess.run(cmd, shell=True, check=True)
    logger.info(f"Video created {outputpath}")
    return outputpath
