#!/usr/bin/ruby

require 'json'
require 'faraday'
require 'fileutils'

NETRUNNER_HOST = 'http://netrunnerdb.com'

def get_cards
  conn = Faraday.new(:url => NETRUNNER_HOST) do |faraday|
    #faraday.response :logger                  # log requests to STDOUT
    faraday.adapter  Faraday.default_adapter  # make requests with Net::HTTP
  end

  response = conn.get '/api/cards/'
  cards = JSON.parse(response.body)
  cards.map do |card|
    new_card = card.clone
    new_card['card_type'] = new_card['type']
    new_card
  end
end

cardLists = Dir.glob('./clusters/**/cards.txt')
cardLists.each do |cardlist|
  File.unlink(cardlist)
end

cards = get_cards
cards = cards.reject { |card| card['largeimagesrc'].length == 0 }
cardUrls = cards.each do |card|
  dir = "./clusters/#{card['type_code']}/#{card['faction_code']}"
  FileUtils.mkdir_p(dir) unless Dir.exist?(dir)
  File.open("#{dir}/cards.txt", 'a') do |f|
    f << "#{NETRUNNER_HOST}#{card['imagesrc']}\n"
  end
  # curl it
end

cardLists = Dir.glob('./clusters/**/cards.txt')
cardLists.each do |cardlist|
  Dir.chdir(File.dirname(cardlist)) {
    %x(wget -i cards.txt)
  }
end
puts "Imported #{cards.length} cards."


