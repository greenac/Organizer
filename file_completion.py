def make_file_completion():
    file = open('files/.file_names.txt', 'r')
    file_names = []
    for line in file:
        if '#' not in line and line != '' and line != '\n':
            if '\n' in line:
                line = line[:line.find('\n')]
            if ':' in line:
                name = line.split(':')[1]
            else:
                name = line
            file_names.append(name.split(',')[0])
    counter = 0
    file.close()
    file = open('files/.file_names', 'w')
    for name in file_names:
        if name[:2] == '18':
            name_underscored = 'eighteen_years_old'
        elif name[:3] == '8th':
            name_underscored = 'eight_street_latinas'
        else:
            name_underscored = name.replace(' ', '_')
        file.write(name_underscored + '="' + name + '"\n')
    file.close()


make_file_completion()