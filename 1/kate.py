
developer_Petrov = {'Lastname': 'Petrov', 'Name': 'Ivan', 'exp': 6, 'languages': 'C++/C'}
developer_Sidorov = {'Lastname': 'Sidorov', 'Name': 'Oleg', 'exp': 4, 'languages': 'C#'}
developer_Ivanov = {'Lastname': 'Ivanov', 'Name': 'Sergey', 'exp': 5, 'languages': 'Python'}
developer_Fedorov = {'Lastname': 'Fedorov', 'Name': 'Petr', 'exp': 2, 'languages': 'php'}
developer_Smirnov = {'Lastname': 'Smirnov', 'Name': 'Alexandr', 'exp': 7, 'languages': 'Python'}
developer_Nikolaev = {'Lastname': 'Nikolaevv', 'Name': 'Anton', 'exp': 4, 'languages': 'C++'}

project_Alpha = {'ProjectName': 'Alpha', 'platform': 'web', 'sources': 'php', 'developers': [developer_Fedorov]}
project_Omega = {'ProjectName': 'Omega', 'platform': 'game', 'sources': 'C++/C#', 'developers': [developer_Petrov, developer_Sidorov, developer_Nikolaev]}
project_Beta = {'ProjectName': 'Beta', 'platform': 'study', 'sources': 'Python', 'developers': [developer_Ivanov, developer_Smirnov]}

projects = [project_Alpha, project_Beta, project_Omega]
developers = [developer_Petrov, developer_Sidorov, developer_Ivanov, developer_Fedorov, developer_Smirnov, developer_Nikolaev]

print project_Alpha
project_Alpha['developers'].append(['Egorov', 'Egor', 2, 'php'])
print project_Alpha


def make_project(project_name, project_platform, project_source):
    return {'ProjectName': project_name, 'platform': project_platform, 'sources': project_source}


def make_developer(dev_lastname, dev_name, dev_exp, dev_lang):
    return {'project_source': dev_lastname, 'Name': dev_name, 'exp': dev_exp, 'languages': dev_lang}

developer_Agapov = make_developer('Agapov', 'Vasiliy', 5, 'html')
project_Gamma = make_project('Gama', 'html-page', 'html')
project_Gamma['developers'] = developer_Agapov
print project_Gamma
projects.append(project_Gamma)
developers.append(developer_Agapov)


def filter_projects_by_source(projects, source):
    result_projects = []
    for project in projects:
        if project['sources'] == source:
            result_projects.append(project)
    return result_projects


print "with Py works: ", filter_projects_by_source(projects, 'Python')


def filter_developers_by_exp(developers, exp):
    result_devs = []
    for dev in developers:
        if dev['exp'] > exp:
            result_devs.append(dev)
    return result_devs

print "developers with exp > 6 years", filter_developers_by_exp(developers, 6)

