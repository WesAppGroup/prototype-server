#! /usr/bin/ruby

require 'rubygems'
require 'feedzirra'
require 'date'

begin


dayOfWeek = DateTime.now.to_date.wday - 1
dayOfWeek = 6 if dayOfWeek < 0

feed = Feedzirra::Feed.fetch_and_parse('http://legacy.cafebonappetit.com/rss/menu/332')

File.open('/root/prototype-server/static/usdan.html', 'w') do |f|
  f << feed.entries[dayOfWeek].summary
end

feed = Feedzirra::Feed.fetch_and_parse('http://legacy.cafebonappetit.com/rss/menu/337')

File.open('/root/prototype-server/static/summerfields.html', 'w') do |f|
  f << feed.entries[dayOfWeek].summary
end

end
