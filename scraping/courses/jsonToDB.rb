require 'json'

json_data = JSON.parse(IO.read("courses.json"))

primaryKey = 0
sPk = 0
total = json_data.size
coursesAdded = []
json_data.each do | course |
        if not coursesAdded.index(course['title'])
                coursesAdded << course['title']
                courseuid = primaryKey
                sections = ""
                course['sections'].each do | section |
                        sqlStatement = "curl -d '"
                        sections << sPk.to_s
                        sections << ";"
                        sqlStatement << "course_uid=#{courseuid.to_s}"
                        sqlStatement << '\&permissionRequired='
                        sqlStatement << section['permissionRequired'].to_s
                        sqlStatement << '\&name='
                        sqlStatement << section['name'].gsub('"',"'")
                        sqlStatement << '\&fr='
                        if section['FR']
                                sqlStatement << section['FR']
                        else
                                sqlStatement << 'X'
                        end
                        sqlStatement << '\&so='
                        if section['SO']
                                sqlStatement << section['SO']
                        else
                                sqlStatement << 'X'
                        end
                        sqlStatement << '\&jr_NonMajor='
                        if section['JR_NonMajor']
                                sqlStatement << section['JR_NonMajor']
                        else
                                sqlStatement << 'X'
                        end
                        sqlStatement << '\&=jr_Major='
                        if section['JR_Major']
                                sqlStatement << section['JR_Major']
                        else
                                sqlStatement << 'X'
                        end
                        sqlStatement << '\&sr_NonMajor='
                        if section['SR_NonMajor']
                                sqlStatement << section['SR_NonMajor']
                        else
                                sqlStatement << 'X'
                        end
                        sqlStatement << '\&sr_Major='
                        if section['SR_Major']
                                sqlStatement << section['SR_Major']
                        else
                                sqlStatement << 'X'
                        end
                        sqlStatement << '\&grad_Major='
                        if section['GRAD_Major']
                                sqlStatement << section['GRAD_Major']
                        else
                                sqlStatement << 'X'
                        end
                        sqlStatement << '\&additional_requirements='
                        #sqlStatement << section['additional_requirements']
                        sqlStatement << "None"
                        sqlStatement << '\&time='
                        sqlStatement << section['times']
                        sqlStatement << '\&seats_available='
                        sqlStatement << section['seatsAvailable'].to_s
                        sqlStatement << '\&professors='
                        sqlStatement << instructors.join(';')
                        sqlStatement << '\&location='
                        sqlStatement << section['location']
                        sqlStatement << '\&major_reading='
                        sqlStatement << section['major_readings'].gsub("\n",";").gsub("'",'"')
                        sqlStatement << '&\enrollment_limit='
                        sqlStatement << section['enrollmentLimit'].to_s
                        sqlStatement << '&\assignments_and_examinations='
                        sqlStatement << section['assignments_and_examinations'].gsub("'",'"')
                        sqlStatement << "' http://stumobile0.wesleyan.edu:3000/sections/add"
                        system(sqlStatement)
                        sPk += 1
                end
                sqlStatement = 'curl -d "genEdArea='
                sqlStatement << course['genEdArea']
                sqlStatement << '\&prerequisites='
                sqlStatement << course['prerequisites']
                sqlStatement << '\&title='
                sqlStatement << course['title'].gsub('"',"'")
                sqlStatement << '\&url='
                sqlStatement << course['url']
                sqlStatement << '\&credit='
                sqlStatement << course['credit'].to_s
                sqlStatement << '\&number='
                sqlStatement << course['number']
                sqlStatement << '\&courseid='
                sqlStatement << course['courseid']
                sqlStatement << '\&semester='
                sqlStatement << course['semester']
                sqlStatement << '\&department='
                sqlStatement << course['department']
                sqlStatement << '\&gradingMode='
                sqlStatement << course['gradingMode']
                sqlStatement << '\&description='
                sqlStatement << course['description'].gsub('"',"'")
                sqlStatement << '\&sections='
                sqlStatement << sections
                sqlStatement << '" https://stumobile0.wesleyan.edu:3000/courses/add'
                system(sqlStatement)
                primaryKey += 1
                printf("\r%0.3f%%", primaryKey.to_f/total.to_f * 100)
        end
end
puts "... #{primaryKey} total added"
