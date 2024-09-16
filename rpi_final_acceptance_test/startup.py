import subprocess
import sys

def main():
    subprocess.run([sys.executable, '-m', 'rpi_final_acceptance_test.main.py'] + sys.argv[1:])