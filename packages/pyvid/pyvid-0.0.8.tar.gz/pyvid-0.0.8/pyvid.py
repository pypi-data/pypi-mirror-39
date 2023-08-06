#!/usr/bin/env python
# -*- encoding: utf-8
"""pyvid package. converts files in path to smaller mp4 files."""
from typing import List, Tuple, Generator, Any
from pathlib import Path
import os
import re

import ffmpeg
import click
import click_spinner as spin
from hurry.filesize import size

__version__ = "0.0.8"


class VideoPath(os.PathLike):
    __slots__ = ("path", "exts", "force", "rem")

    def __init__(
        self, path: str, ext: str = "", force: bool = False, rem: bool = False
    ) -> None:
        self.path = Path(path)
        if ext:
            self.exts = [ext[1:] if ext[0] == "." else ext]
        else:
            self.exts = ["mp4", "avi", "mkv", "mov", "webm"]
        self.force = force
        self.rem = rem

    def __fspath__(self):
        return str(self.path)

    def __iter__(self) -> Generator:
        if self.path.is_file():
            yield Video(self.path, self.force)
        else:
            for y in self.exts:
                for z in self.path.glob("*." + y):
                    yield Video(z, self.force)


class Video:
    __slots__ = ("path", "converted", "force", "size", "conv_path")

    def __init__(self, path: Path, force: bool) -> None:
        self.path = path
        self.converted = 0
        self.force = force
        self.size = self.path.stat().st_size

        conv_name = self.path.with_suffix(".mp4").name
        self.conv_path = self.path.parent / "converted" / conv_name

    def __repr__(self) -> str:
        return f"<Video {self.path.name} {size(self.size)}>"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Video):
            return os.path.samestat(os.stat(self.path), os.stat(other.path))
        elif isinstance(other, Path):
            return os.path.samestat(os.stat(self.path), os.stat(other))
        return NotImplemented


class Logger:
    """Logger for video conversion stats"""

    __slots__ = "fname"

    def __init__(self, fname: str, append: bool = False) -> None:
        """Store ref to fname and create fresh log unless append is True"""
        self.fname = fname
        if append:
            self.reset()

    def __repr__(self) -> str:
        return f"<Logger {self.fname}>"

    def log(self, entry: str, orig: int = 0, conv: int = 0) -> None:
        """Write entry to log file. If passed orig and conv, append to entry"""
        if orig:
            entry += f":{orig}:{conv}"

        with open(self.fname, "a") as f:
            print(entry, file=f)

    def get(self, n: int) -> List[str]:
        """Return last n lines of log file."""
        with open(self.fname, "r") as f:
            return f.readlines()[-n if n > 1 else -1 :]

    def reset(self) -> None:
        """Delete log file from disk."""
        if os.path.exists(self.fname):
            os.remove(self.fname)

    def summarise(self, num: int) -> None:
        """Generate summary stats for conversions."""
        lines = "\n".join(self.get(num))
        size_regex = re.compile(r":(?P<original>\d+):(?P<converted>\d+)$", re.M)

        tot_o = 0
        tot_c = 0
        for original, converted in size_regex.findall(lines):
            tot_o += int(original)
            tot_c += int(converted)

        try:
            rel_size = round(tot_c * 100 / tot_o)
        except ZeroDivisionError:
            click.echo("summary not written")
        else:
            self.log(
                "-- Batch of last %d: %d%% of original size - %s -> %s"
                % (num, rel_size, size(tot_o), size(tot_c))
            )


def convert_files(vids: VideoPath, logger: Logger) -> None:
    """Convert file in VideoPath object."""
    top = vids if vids.path.is_dir() else vids.path.parent
    n_proc = 0

    for vid in vids:
        click.echo()
        if n_proc == 0:
            logger.log(f"CONVERTING FILES IN {top}")

        success, code = convert_video(vid)

        if not success:
            if code:
                break
            continue

        logger.log(vid.path.name, vid.size, vid.converted)
        n_proc += 1

        if vids.rem:
            os.remove(vid.path)

    if n_proc:
        logger.summarise(n_proc)
        max_lines = 3
        click.echo()
        if n_proc > max_lines:
            click.echo("...")
        n_lines = max_lines if n_proc > max_lines else n_proc + 1
        click.echo("".join(logger.get(n_lines)))
        if n_proc > max_lines:
            click.echo(f"see {logger.fname} for more details")
    else:
        logger.reset()
        click.echo(f"NO VIDEO FILES CONVERTED IN {top}")


def convert_video(vid: Video) -> Tuple[bool, int]:
    """Use fmmpeg to convert Video object."""
    prompt = (
        click.style(str(vid.path), fg="yellow")
        + " -> "
        + click.style(str(vid.conv_path.parent), fg="green")
        + "\\"
        + click.style(vid.conv_path.name, fg="yellow")
        + "\n"
    )

    if not vid.force:
        prompt += "continue? (y)es/(n)o/(c)ancel all"
    click.echo(prompt)
    opt = "y" if vid.force else click.getchar()

    if opt == "y":
        os.makedirs(vid.conv_path.parent, exist_ok=True)

        stream = ffmpeg.input(str(vid.path))
        stream = ffmpeg.output(
            stream,
            str(vid.conv_path),
            vcodec="libx264",
            crf=20,
            acodec="copy",
            preset="veryfast",
        )

        click.echo(f"converting {vid.path}...", nl=False)
        try:
            with spin.spinner():
                err, out = ffmpeg.run(stream, quiet=True, overwrite_output=True)
        except KeyboardInterrupt:
            click.echo("aborted")
            os.remove(vid.conv_path)
            vid.conv_path.parent.rmdir()
            return False, 0
        except FileNotFoundError:
            raise OSError("ffmpeg is either not installed or not in PATH")

        click.echo("done")
        vid.converted = vid.conv_path.stat().st_size
        return True, 0

    if opt == "c":
        return False, 1
    # default option n
    return False, 0


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-e", "--ext", help="File extension to look for")
@click.option("-y", "--force", is_flag=True, help="Disable convert prompt")
@click.option("-d", "--rem", is_flag=True, help="Delete source video file(s)")
@click.version_option()
def main(path: str, ext: str, force: bool, rem: bool) -> None:
    """Convert video(s) in specified path."""
    if ext:
        click.echo(f"extension: {ext}")

    logger = Logger("stats.txt")

    vp = VideoPath(path, ext=ext, force=force, rem=rem)
    convert_files(vp, logger)


if __name__ == "__main__":
    main()
