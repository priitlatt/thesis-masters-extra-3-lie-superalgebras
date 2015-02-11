from subprocess import Popen

MATHEMATICA_PATH = "/home/priit/files/programs/mathematica/MathematicaScript"

def create_script(equations, multipliers, even_count, odd_count):
    script = "Reduce[%s, {%s}, Complexes]" % (
        " && ".join(equations),
        ', '.join(sorted([mult.replace('_', '') for mult in multipliers]))
    )

    filename = '%s_%s.m' % (even_count, odd_count)
    output_filename = '%s_%s.result' % (even_count, odd_count)

    with open(filename, 'w') as f:
        f.write('%s >> %s' % (script, output_filename))

    return filename, output_filename


def run_script(filename):
    cmd_list = [MATHEMATICA_PATH, '-script', filename]
    print('running  "%s"' % ' '.join(cmd_list))
    Popen(cmd_list).wait()
    print('done')


def parse_result(result_file):
    with open(result_file) as f:
        print(f.read())
