#!/usr/bin/env python

import os
import ssl
import argparse
import datetime
import re
import sys
import shlex
from subprocess import Popen, PIPE
from pytube import YouTube
from pysndfx import AudioEffectsChain
import moviepy.editor as mp
from pydub import AudioSegment

# Disable certificate verification (for educational purposes only)
ssl._create_default_https_context = ssl._create_unverified_context

# Colors for terminal output


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def download_video(url, output_dir):
    try:
        youtube = YouTube(url)
        video = youtube.streams.get_highest_resolution()
        video_filename = video.default_filename.replace(" ", "_")
        current_dir = os.getcwd()
        os.chdir(output_dir)
        video.download(filename=video_filename)
        os.chdir(current_dir)
        return video_filename
    except Exception as e:
        print(f"{bcolors.FAIL}Error downloading video: {str(e)}{bcolors.ENDC}")
        return None


def convert_to_mp3(video_path, output_dir):
    try:
        video = mp.VideoFileClip(video_path)
        audio = video.audio
        mp3_filename = os.path.splitext(
            os.path.basename(video_path))[0] + ".mp3"
        mp3_filename = mp3_filename.replace(" ", "_")
        mp3_path = os.path.join(output_dir, mp3_filename)
        audio.write_audiofile(mp3_path, codec='libmp3lame')
        return mp3_path
    except Exception as e:
        print(f"{bcolors.FAIL}Error converting to MP3: {str(e)}{bcolors.ENDC}")
        return None


def apply_vaporwave_effects(audio_input, audio_output, speed_ratio, pitch_shift, lowpass_cutoff, bass_boost=None, gain_db=None, oops=False, phaser=False, tremolo=False, compand=False, no_reverb=False):
    try:
        fx = AudioEffectsChain()

        if bass_boost is not None:
            bass_boost_effect = f'bass {bass_boost}'
            fx = fx.custom(bass_boost_effect)

        fx = fx.pitch(pitch_shift)

        if oops:
            fx = fx.custom("oops")

        if tremolo:
            fx = fx.tremolo(freq=500, depth=50)

        if phaser:
            fx = fx.phaser(0.9, 0.8, 2, 0.2, 0.5)

        if gain_db is not None:
            fx = fx.gain(gain_db)

        if compand:
            fx = fx.compand()

        fx = fx.speed(speed_ratio).lowpass(lowpass_cutoff)

        if not no_reverb:
            fx = fx.reverb()

        fx(audio_input, audio_output)
    except Exception as e:
        if str(e) == "invalid literal for int() with base 10: b''":
            print(f"{bcolors.FAIL}Please make sure that there is no space in the audio file's name.{
                  bcolors.ENDC}")
            sys.exit(1)
        else:
            print(f"{bcolors.FAIL}Error applying audio effects: {
                  str(e)}{bcolors.ENDC}")
            sys.exit(1)


def validate_youtube_url(url):
    if not (re.match(r'^https?://(www\.)?youtube\.com/watch\?v=', url) or re.match(r'^https?://youtu.be/', url)):
        print(f"{bcolors.FAIL}Invalid YouTube URL{bcolors.ENDC}")
        sys.exit(1)


def check_file_existence(file_path):
    if not os.path.isfile(file_path):
        print(f"{bcolors.FAIL}File not found: {file_path}{bcolors.ENDC}")
        sys.exit(1)


def check_directory_writable(directory_path):
    if not os.access(directory_path, os.W_OK):
        print(f"{bcolors.FAIL}Directory not writable: {
              directory_path}{bcolors.ENDC}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Creates a music remix (slowed + reverb or sped up) of a given MP3 file"
    )

    parser.add_argument("-o", "--output", dest="output_name",
                        help="Name of output file", type=str)

    required_arguments = parser.add_argument_group("required arguments")

    required_arguments.add_argument("-a", "--audio", dest="audio_input",
                                    help="Input audio file to modify (.mp3)", type=str, required=False)
    required_arguments.add_argument("-u", "--url", dest="youtube_url",
                                    help="YouTube URL to download and vaporise", type=str, required=False)

    audio_arguments = parser.add_argument_group(
        "audio arguments", "These arguments control audio effects that will be applied by default")

    audio_arguments.add_argument("-s", "--speed", dest="speed_ratio",
                                 help="Ratio of new playback speed to old speed.", type=float, default=1.0)
    audio_arguments.add_argument("-p", "--pitch", dest="pitch_shift",
                                 help="Pitch shift (100ths of a semitone).", type=float, default=0.0)
    audio_arguments.add_argument("-l", "--lowpass", dest="lowpass_cutoff",
                                 help="Cutoff for lowpass filter (Hz).", type=int, default=3500)

    audio_arguments_optional = parser.add_argument_group(
        "extra audio arguments", "These arguments control extra, optional audio effects")

    audio_arguments_optional.add_argument(
        "-b", "--bass", dest="bass_boost", help="Add a bass boost effect.", type=int, default=None)
    audio_arguments_optional.add_argument(
        "-ga", "--gain", dest="gain_db", help="Applies gain (dB).", type=int, default=None)
    audio_arguments_optional.add_argument(
        "-op", "--oops", dest="oops", help="Applies Out Of Phase Stereo effect.", action="store_true")
    audio_arguments_optional.add_argument(
        "-ph", "--phaser", dest="phaser", help="Enable phaser effect.", action="store_true")
    audio_arguments_optional.add_argument(
        "-tr", "--tremolo", dest="tremolo", help="Enable tremolo effect.", action="store_true")
    audio_arguments_optional.add_argument(
        "-co", "--compand", dest="compand", help="Enable compand, which compresses the dynamic range of the audio.", action="store_true")
    audio_arguments_optional.add_argument(
        "-nr", "--noreverb", dest="no_reverb", help="Disables reverb.", action="store_true")
    audio_arguments_optional.add_argument("-e", "--effect", dest="effect", help="Choose audio effect: 'slowed_reversed', 'sped_up', 'keep_original'.",
                                          type=str, choices=['slowed_reversed', 'sped_up', 'keep_original'], default='keep_original')

    args = parser.parse_args()

    if args.youtube_url:
        validate_youtube_url(args.youtube_url)
        output_dir = os.getcwd()
        check_directory_writable(output_dir)
        video_filename = download_video(args.youtube_url, output_dir)
        if video_filename is None:
            return
        args.audio_input = convert_to_mp3(
            os.path.join(output_dir, video_filename), output_dir)

    if args.audio_input is None:
        print(f"{bcolors.FAIL}ERROR: No audio input provided{bcolors.ENDC}")
        want_youtube_download = input(
            f"{bcolors.OKCYAN}Would you like to download a YouTube video instead? (n/y): {bcolors.ENDC}").lower()
        if want_youtube_download == 'y':
            args.youtube_url = input(
                f"{bcolors.OKCYAN}Enter the YouTube URL: {bcolors.ENDC}")
            validate_youtube_url(args.youtube_url)
            effect_choice = input(f"{bcolors.OKCYAN}What effect would you like to apply? (slowed_reversed [r], sped_up [s], keep_original [k]): {
                                  bcolors.ENDC}").lower()
            if effect_choice == 'r':
                args.effect = 'slowed_reversed'
            elif effect_choice == 's':
                args.effect = 'sped_up'
            else:
                args.effect = 'keep_original'

            output_dir = os.getcwd()
            check_directory_writable(output_dir)
            video_filename = download_video(args.youtube_url, output_dir)
            if video_filename is None:
                return
            args.audio_input = convert_to_mp3(
                os.path.join(output_dir, video_filename), output_dir)
        else:
            print(f"{bcolors.FAIL}ERROR: No audio input provided{bcolors.ENDC}")
            sys.exit(1)

    check_file_existence(args.audio_input)

    if args.output_name is None:
        audio_input_string = re.sub(".mp3", "", str(args.audio_input))
        audio_output = audio_input_string + "_" + args.effect + ".mp3"
    else:
        output_string = re.sub(".mp3", "", str(args.output_name))
        audio_output = output_string + ".mp3"
        if args.audio_input == args.output_name:
            print(f"{bcolors.FAIL}ERROR: Input and output name are identical{
                  bcolors.ENDC}")
            sys.exit(1)

    if args.effect == 'slowed_reversed':
        args.speed_ratio = 0.75
        args.pitch_shift = -75
    elif args.effect == 'sped_up':
        args.speed_ratio = 1.30
        args.pitch_shift = -50

    if args.effect == 'keep_original':
        try:
            AudioSegment.from_file(args.audio_input).export(
                audio_output, format="mp3")
        except Exception as e:
            print(f"{bcolors.FAIL}Error exporting original audio: {
                  str(e)}{bcolors.ENDC}")
            sys.exit(1)
    else:
        try:
            apply_vaporwave_effects(
                shlex.quote(args.audio_input),
                audio_output,
                args.speed_ratio,
                args.pitch_shift,
                args.lowpass_cutoff,
                bass_boost=args.bass_boost,
                gain_db=args.gain_db,
                oops=args.oops,
                phaser=args.phaser,
                tremolo=args.tremolo,
                compand=args.compand,
                no_reverb=args.no_reverb,
            )
        except Exception as e:
            print(f"{bcolors.FAIL}Error applying effects: {
                  str(e)}{bcolors.ENDC}")
            sys.exit(1)

    print(f"{bcolors.OKGREEN}Script finished at {
          datetime.datetime.now().strftime('%H:%M:%S')}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Output MP3 file: {audio_output}{bcolors.ENDC}")


if __name__ == "__main__":
    main()
