require 'json'
begin
# need to url-encode spaces
`curl stumobile0.wesleyan.edu/clear/thisiswhy`
year = Time.now.year
year -= 1 if Time.now.month < 6
all_courses = JSON.parse `curl https://webapps.wesleyan.edu/wapi/v1/public/academic/courses/#{year} 2>/dev/null`
term = ''
valid_courses = all_courses['academic']['courses'].select { |c| c['course'] and c['section'] and c['term'] }
valid_courses.each do |section|
  begin
  section_info = JSON.parse `curl https://webapps.wesleyan.edu/wapi/v1/public/academic/course/#{section['course']}/#{section['section']}/#{section['term']} 2>/dev/null`
  section_info = section_info['academic']['courses'][0]
  if section['section'] == '01' # this is the first section
    cmd = 'curl --data "genEdArea='
    if section_info and section_info['attributes'] and section_info['attributes'][0] and section_info['attributes'][0]['attribute']
      cmd << section_info['attributes'][0]['attribute'].gsub(' ','%20')
    else
      cmd << "NA"
    end
    cmd << '&title='
    cmd << section['description'].gsub(' ','%20') # is actually title
    cmd << '&number='
    cmd << section['catalog_number'].gsub(' ','%20')
    cmd << '&courseid='
    cmd << section['course'].to_i.to_s
    cmd << '&semester='
    term = section['term'].to_i % 10
    if term == 6
      cmd << 'Summer'
    elsif term == 9
      cmd << 'Fall'
    else
      cmd << 'Spring'
    end
    cmd << '&department=' 
    cmd << section['subject'].gsub(' ','%20')
    cmd << '&description='
    if section_info and section_info['description_long']
      cmd << section_info['description_long'].gsub(' ','%20')
    else
      cmd << 'NA'
    end
    cmd << '" http://stumobile0.wesleyan.edu/courses/add'
    system(cmd)
    course_id = JSON.parse(`#{cmd}`)['course_id']
  end
  cmd = "curl --data  \"course_uid=#{section['course'].to_i.to_s}"
  cmd << '&semester='
  if term == 6
      cmd << '0'
    elsif term == 9
      cmd << '1'
    else
      cmd << '2'
    end
  cmd << '&professors='
  if section_info and section_info['meetings'] and section_info['meetings'][0] and section_info['meetings'][0]['instructors']
    if section_info['meetings'][0]['instructors'].class != Array
      instructors = section_info['meetings'][0]['instructors'].gsub(' ','%20')
      cmd << instructors['first_name'].gsub(' ','%20')
      cmd << '%20'
      cmd << instructors['last_name'].gsub(' ','%20')
    else
      instructors = section_info['meetings'][0]['instructors'].join('%20')
      cmd << instructors
    end
  else
    cmd << 'NA'
  end
  cmd << '&time='
  if section_info and section_info['meetings'] and section_info['meetings'][0] and section_info['meetings'][0]['meeting_pattern']
    cmd << section_info['meetings'][0]['meeting_pattern'].gsub(' ','%20')
    cmd << '%20'
    cmd << section_info['meetings'][0]['start_time'].gsub(' ','%20')
    cmd << '-'
    cmd << section_info['meetings'][0]['end_time'].gsub(' ','%20')
  else
    cmd << 'NA'
  end
  cmd << '&location='
  if section_info and section_info['meetings'] and section_info['meetings'][0] and section_info['meetings'][0]['location']
    cmd << section_info['meetings'][0]['location'].gsub(' ','%20')
  else
    cmd << 'NA'
  end
  cmd << '&seats_available='
  if section_info and section_info['available_seats']
    cmd << section_info['available_seats'].gsub(' ','%20')
  else
    cmd << 'NA'
  end
  cmd << '" http://stumobile0.wesleyan.edu/sections/add' 
  system(cmd)
  rescue
    puts "Error (line #{$@}): #{$!}"
  end
end
end
