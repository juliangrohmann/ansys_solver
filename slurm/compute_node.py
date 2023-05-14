import sys
import os
import traceback
from ansys.mapdl import core as pymapdl


def init_env():
    home = os.path.expanduser('~')
    scratch_path = os.path.join(home, 'scratch')
    sys.path.append(scratch_path)

    ansys_root = os.environ['ANSYS_ROOT']
    ansys_exe = os.path.join(ansys_root, 'v231', 'ansys', 'bin', 'ansys231')
    print(f"Setting ANSYS executable path: {ansys_exe}")
    pymapdl.change_default_ansys_path(ansys_exe)

    return scratch_path


def print_directory_tree(start_path):
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{sub_indent}{f}')


SCRATCH_PATH = init_env()
from parametric_solver.solver import BilinearSolver

HEMJ_INP = os.path.join(SCRATCH_PATH, 'inp', 'hemj_v2.inp')
OUTPUR_DIR = os.path.join(SCRATCH_PATH, 'output')
SOLUTION_DIR = os.path.join(OUTPUR_DIR, 'solutions')
RUN_DIR = os.path.join(OUTPUR_DIR, os.environ.get("SLURM_JOB_ID"))

solver = BilinearSolver(
    HEMJ_INP,
    run_location=RUN_DIR,
    loglevel="INFO",
    start_instance=False)

solver.add_sample(200e9, 700e6, 70e9)
solver.add_sample(200e9, 700e6, 80e9)
solver.add_sample(200e9, 700e6, 90e9)

solver.solve(verbose=True, write_path=SOLUTION_DIR)