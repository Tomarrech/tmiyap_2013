# coding=utf-8
from datetime import datetime
from lxml import etree
from lxml.builder import E
from lxml.etree import tostring


student_petrov = {'last_name': 'Petrov', 'first_name': 'Ivan', 'birthday': datetime(1990, 12, 1)}
student_ivanov = {'last_name': 'Ivanov', 'first_name': 'Petr', 'birthday': datetime(1989, 12, 1)}

teacher_1 = {
    'last_name': 'Ivanov',
    'first_name': 'Petr',
    'birthday': datetime(1980, 12, 1),
    'students': [student_petrov, student_ivanov]
}

teacher_xml = tostring(
    E.teacher(
        E.students(*[E.student(
            last_name=student['last_name'],
            first_name=student['first_name'],
            birthday=student['birthday'].isoformat(),
        ) for student in teacher_1['students']]
        ),
        last_name=teacher_1['last_name'],
        first_name=teacher_1['first_name'],
        birthday=teacher_1['birthday'].isoformat()
    ),
    xml_declaration=True, encoding='UTF-8', pretty_print=True
)

print 'azazaza\n', teacher_xml
print "end azazaza"

tch_file = open('teacher.xml', 'wb')
tch_file.write(teacher_xml)
tch_file.close()


# now from xml to dict
root = etree.fromstring(teacher_xml)

teacher = {
    'last_name': root.attrib['last_name'],
    'first_name': root.attrib['first_name'],
    'birthday': datetime.strptime(root.attrib['birthday'], '%Y-%m-%dT%H:%M:%S'),
    'students': [{
                     'last_name': el.attrib['last_name'],
                     'first_name': el.attrib['first_name'],
                     'birthday': datetime.strptime(el.attrib['birthday'], '%Y-%m-%dT%H:%M:%S'),
                 } for el in root.find('students').iter('student')]
}

for st in teacher['students']:
    print st


