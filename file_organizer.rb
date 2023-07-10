#!/usr/bin/env ruby

require 'fileutils'

def organize_folder(folder_path, organized_folder_path)
  puts "Organizing folder: #{folder_path}"

  Dir.mkdir(organized_folder_path) unless Dir.exist?(organized_folder_path)

  entries = Dir.entries(folder_path) - ['.', '..']

  entries.each do |entry|
    entry_path = File.join(folder_path, entry)

    if File.directory?(entry_path)
      if entry.downcase == entry_path.downcase
        organize_files(entry_path, organized_folder_path)
      else
        subfolder_path = File.join(organized_folder_path, entry)
        organize_folder(entry_path, subfolder_path)
      end
    else
      extension = File.extname(entry).downcase[1..-1]

      if extension != ''
        subfolder_path = File.join(organized_folder_path, extension)
        FileUtils.mkdir_p(subfolder_path) unless Dir.exist?(subfolder_path)

        new_entry_path = File.join(subfolder_path, entry)
        FileUtils.mv(entry_path, new_entry_path)
        puts "Moved #{entry} to #{subfolder_path}"
      end
    end
  end
end

def organize_files(folder_path, organized_folder_path)
  puts "Organizing files in folder: #{folder_path}"

  entries = Dir.entries(folder_path) - ['.', '..']

  entries.each do |entry|
    entry_path = File.join(folder_path, entry)

    if File.file?(entry_path)
      extension = File.extname(entry).downcase[1..-1]

      if extension != ''
        subfolder_path = File.join(organized_folder_path, extension)
        FileUtils.mkdir_p(subfolder_path) unless Dir.exist?(subfolder_path)

        new_entry_path = File.join(subfolder_path, entry)
        FileUtils.mv(entry_path, new_entry_path)
        puts "Moved #{entry} to #{subfolder_path}"
      end
    end
  end
end

folder_path = ARGV[0]

if folder_path.nil?
  puts "Please provide the folder path as a command-line argument."
else
  if Dir.exist?(folder_path)
    organized_folder_path = File.join(folder_path, 'organized')

    organize_folder(folder_path, organized_folder_path)
    puts "Folder organization complete!"
  else
    puts "The specified folder does not exist."
  end
end
