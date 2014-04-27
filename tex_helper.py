import os
from subprocess import Popen

TEX_TEMPLATE = r"""\documentclass[12pt]{{article}}
\begin{{document}}
\begin{{enumerate}}
{equations}
\end{{enumerate}}
\end{{document}}
"""

def create_tex(equations_list, even_count, odd_count):
    file_prefix = '__combinations_%s_%s__' % (even_count, odd_count)
    s = ""
    for eq in equations_list:
        s += eq + '\n'
    tex = TEX_TEMPLATE.format(equations=s)
    with open(file_prefix + '.tex', 'w') as f:
        f.write(tex)
    Popen(['pdflatex', '"%s".tex' % file_prefix]).wait()
    for f in os.listdir(os.getcwd()):
        if file_prefix in f and not f.endswith(('.tex', '.pdf')):
            os.remove(f)
        elif file_prefix in f and f.endswith(('.tex', '.pdf')):
            os.rename(f, f.replace('_', ''))


def add_tex(output_list, c, l, r, b1, b2):
    l = [' '.join(el) for el in l]
    r = [' '.join(el) for el in r]
    # print '[', b1, b2, c, ']', '=', ' '.join(r), '\n'
    o = r'\left[%s, %s, %s \right] \\ %s = %s' % (b1, b2, c, ' '.join(l) or 0, ' '.join(r) or 0)
    output_list.append('\item $%s$' % o)