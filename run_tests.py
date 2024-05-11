'''
Automatically runs all of the project's tests
'''

import subprocess
import glob

def run_tests():
    test_files = glob.glob("*_test.py")
    print("FOUND TESTS: ", test_files)
    for filename in test_files:
        print()
        print("RUNNING: ", filename)
        subprocess.run(["python", filename])

if __name__ == "__main__":
    run_tests()