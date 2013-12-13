#! /usr/bin/ruby

require 'rubygems'
require 'feedzirra'
require 'date'
require 'json'

begin


dayOfWeek = DateTime.now.to_date.wday - 1
dayOfWeek = 6 if dayOfWeek < 0

feed = Feedzirra::Feed.fetch_and_parse('http://legacy.cafebonappetit.com/rss/menu/332')
to_parse = feed.entries[dayOfWeek].summary.gsub("\n",'')
lunchData = to_parse.scan(/<h3>Lunch<\/h3>(.*)<h3>/)
dinnerData = to_parse.scan(/<h3>Dinner<\/h3>(.*)<h3>/)
breakfastData = to_parse.scan(/<h3>Breakfast<\/h3>(.*)/)
lunchMeals = lunchData[0][0].scan(/<h(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>([^<]*)<\/(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>/)
lunchMeals = lunchMeals.select { |m| m[0] }
dinnerMeals = dinnerData[0][0].scan(/<h(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>([^<]*)<\/(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>/)
dinnerMeals = dinnerMeals.select { |m| m[0] }
breakfastMeals = breakfastData[0][0].scan(/<h(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>([^<]*)<\/(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>/)
breakfastMeals = breakfastMeals.select { |m| m[0] }
data = { "lunch" => lunchMeals, "dinner" => dinnerMeals, "breakfast" => breakfastMeals }
File.open('/root/prototype-server/static/usdan.json', 'w') do |f|
  f << data.to_json
end

feed = Feedzirra::Feed.fetch_and_parse('http://legacy.cafebonappetit.com/rss/menu/337')
to_parse = feed.entries[dayOfWeek].summary.gsub("\n",'')
lunchData = to_parse.scan(/<h3>Lunch<\/h3>(.*)<h3>/)
dinnerData = to_parse.scan(/<h3>Dinner<\/h3>(.*)/)
lunchMeals = lunchData[0][0].scan(/<h(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>([^<]*)<\/(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>/)
lunchMeals = lunchMeals.select { |m| m[0] }
dinnerMeals = dinnerData[0][0].scan(/<h(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>([^<]*)<\/(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>/)
dinnerMeals = dinnerMeals.select { |m| m[0] }
data = { "lunch" => lunchMeals, "dinner" => dinnerMeals }
File.open('/root/prototype-server/static/summerfields.json', 'w') do |f|
  f << data.to_json
end

end
