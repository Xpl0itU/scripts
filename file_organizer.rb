#!/usr/bin/env ruby

require 'fileutils'

def organize_folder(folder_path)
  Dir.glob("#{folder_path}/**/*").each do |item|
    next unless File.file?(item)

    extension = File.extname(item).downcase.delete('.')
    next if extension.empty?

    destination_folder = File.join(folder_path, extension)
    FileUtils.mkdir_p(destination_folder) unless Dir.exist?(destination_folder)

    FileUtils.mv(item, destination_folder)
  end
end

if ARGV.empty?
  puts "Usage: ruby folder_organizer.rb <folder_path>"
else
  folder_path = ARGV[0]

  if Dir.exist?(folder_path)
    organize_folder(folder_path)
    puts "Folder organized successfully!"
  else
    puts "Invalid folder path."
  end
end
