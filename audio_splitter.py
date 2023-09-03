#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

def split_audio(input_file, time_file):
    output_folder = os.path.splitext(os.path.basename(input_file))[0]
    os.makedirs(output_folder, exist_ok=True)

    with open(time_file, 'r') as file:
        time_entries = [line.strip().split(' ') for line in file if line.strip() and not line.startswith('#')]

    for index, entry in enumerate(time_entries):
        start_time = datetime.strptime(entry[0], '%H:%M:%S')
        end_time = datetime.strptime(time_entries[index + 1][0], '%H:%M:%S') if index < len(time_entries) - 1 else None
        name = entry[1]

        command = [
            'ffmpeg',
            '-i', input_file,
            '-ss', start_time.strftime('%H:%M:%S'),
        ]

        if end_time:
            command.extend(['-to', end_time.strftime('%H:%M:%S')])

        command.append(os.path.join(output_folder, f'{name}.mp3'))

        subprocess.run(command)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print('Usage: python audio_splitter.py <input_file> [timestamps_file]')
        sys.exit(1)

    input_file = sys.argv[1]
    time_file = sys.argv[2] if len(sys.argv) > 2 else 'timestamps.txt'

    if not os.path.isfile(time_file):
        print(f"Timestamps file not found: {time_file}")
        sys.exit(1)

    split_audio(input_file, time_file)
