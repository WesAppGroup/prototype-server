require 'json'
begin
# need to url-encode spaces
year = Time.now.year
all_courses = JSON.parse `curl https://webapps.wesleyan.edu/wapi/v1/public/academic/courses/#{year}`
all_courses['academic']['courses'].each do |section|
  section_info = JSON.parse `curl https://webapps.wesleyan.edu/wapi/v1/public/academic/course/#{section['course']}/{#{section['section']}/#{section['term']}`
  section_info = section_info['academic']['courses'][0]
  if section['section'] == '01' # this is the first section
    cmd = 'curl --data "genEdArea='
    cmd << section_info['attributes'][0]['attribute'].gsub(' ','%20')
    cmd << '\&title='
    cmd << section['description'].gsub(' ','%20') # is actually title
    cmd << '\&number='
    cmd << section['catalog_number'].gsub(' ','%20')
    cmd << '\&courseid='
    cmd << section['course'].gsub(' ','%20')
    cmd << '\&semester='
    term = section['semester'].to_i % 10
    if term == 6
      cmd << 'Summer'
    elsif term == 9
      cmd << 'Fall'
    else
      cmd << 'Spring'
    end
    cmd << '\&department=' 
    cmd << section['subject'].gsub(' ','%20')
    cmd << '\&description='
    cmd << section_info['description_long'].gsub(' ','%20')
    cmd << '" http://stumobile0.wesleyan.edu/courses/add'
    course_id = JSON.parse(`#{cmd}`)['course_id']
  end
  cmd = "curl --data  \"course_uid=#{course_id}"
  cmd << '\&professors='
  instructors = section_info['meetings'][0]['instructors'].gsub(' ','%20')
  cmd << instructors['first_name'].gsub(' ','%20')
  cmd << '%20'
  cmd << instructors['last_name'].gsub(' ','%20')
  cmd << '\&time='
  cmd << section_info['meetings'][0]['meeting_pattern'].gsub(' ','%20')
  cmd << '%20'
  cmd << section_info['meetings'][0]['start_time'].gsub(' ','%20')
  cmd << '-'
  cmd << section_info['meetings'][0]['end_time'].gsub(' ','%20')
  cmd << '\&location='
  cmd << section_info['meetings'][0]['location'].gsub(' ','%20')
  cmd << '\&seats_available='
  cmd << section_info['available_seats'].gsub(' ','%20')
  cmd << '" http://stumobile0.wesleyan.edu/sections/add' 
  system(cmd)
end
end