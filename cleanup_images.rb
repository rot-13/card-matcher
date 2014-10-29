#!/usr/bin/ruby

imagesDbs = Dir.glob('./clusters/**/*.db').each { |imagesDb| File.unlink(imagesDb) }
File.unlink('./templates.db') if File.exist? './templates.db'
