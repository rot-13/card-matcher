#!/usr/bin/ruby

imagesDbs = Dir.glob('./clusters/**/*.db').each { |imagesDb| File.unlink(imagesDb) }