#!/usr/bin/ruby

img_to_download_path = "https://raw.githubusercontent.com/itayadler/self-modifying-card/master/src/images/%{type}/%{type}_%{faction}.png"
Dir.glob('./clusters/*/*').each do |path|
  type = path.split('/')[2]
  faction = path.split('/')[3]
  if faction.include?('-')
    faction = faction.split('-')[0]
  end

  download_path = img_to_download_path % { type: type, faction: faction }
  Dir.chdir(path) do
    unless File.exists?('./template.png')
      %x(wget -O template.png #{download_path})
    end
  end
end
