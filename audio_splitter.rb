#!/usr/bin/env ruby

require 'time'
require 'fileutils'

def split_audio(input_file, time_file)
  output_folder = File.basename(input_file, '.*')
  FileUtils.mkdir_p(output_folder)

  time_entries = File.readlines(time_file)
  time_entries = time_entries.map { |line| line.chomp.split(' ') }
  time_entries.reject! { |entry| entry.empty? || entry[0].start_with?('#') }

  time_entries.each_with_index do |entry, index|
    start_time = Time.parse(entry[0])
    end_time = index < time_entries.size - 1 ? Time.parse(time_entries[index + 1][0]) : nil
    name = entry[1]

    command = "ffmpeg -i #{input_file} "
    command += "-ss #{start_time.strftime('%H:%M:%S')} "
    command += "-to #{end_time.strftime('%H:%M:%S')} " unless end_time.nil?
    command += "#{output_folder}/#{name}.mp3"

    system(command)
  end
end

input_file = ARGV[0]
time_file = ARGV[1] || 'timestamps.txt'

if input_file.nil?
  puts 'Please provide the input audio file path as the first argument.'
  exit(1)
end

if !File.file?(time_file)
  puts "Timestamps file not found: #{time_file}"
  exit(1)
end

split_audio(input_file, time_file)
