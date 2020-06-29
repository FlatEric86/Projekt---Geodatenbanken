import PY_lib, sys



sql_api_obj = PY_lib.PY_SQL_API()

row = sql_api_obj.get_row_by_name(sys.argv[1])

name         = row[0]
picture_name = row[3]
text_info    = row[4]

print('\t\t\t<img width="500" height="350" src="/geodatenbanken_projekt/Bilder/' + picture_name + '.png">\n')

path = 'C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/HTML/sub_html/' + name
with open(path + '.html', 'w') as fout:
    fout.write('<html>\n\t<meta charset="UTF-8">\n')
    fout.write('<header><title' + name + '></></header>\n')
    fout.write('<body>\n')
    fout.write('\t<div>\n\t\t<figure>\n')
    fout.write('\t\t\t<img width="750" height="400" src="/geodatenbanken_projekt/Bilder/' + picture_name + '">\n')
    fout.write('\t\t</figure>\n')
    fout.write('\t</div>\n')
    fout.write('\t<div>\n')
    fout.write('\t\t<p>\n')
    fout.write(text_info + '\n')
    fout.write('\t\t</p>\n')
    fout.write('\t<div>\n')
    fout.write('</body>\n')
    fout.write('</html>\n')


