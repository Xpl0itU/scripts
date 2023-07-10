#!/usr/bin/env ruby

require 'combine_pdf'

if ARGV.length < 2
  puts 'Usage: ruby pdf_merger.rb output.pdf input1.pdf input2.pdf ...'
  exit
end

output_file = ARGV[0]
input_files = ARGV[1..-1]

pdf = CombinePDF.new

input_files.each do |file|
  begin
    pdf << CombinePDF.load(file)
  rescue CombinePDF::Error
    puts "Error loading file: #{file}"
  end
end

pdf.save(output_file)
puts "PDF files merged successfully! Output file: #{output_file}"
