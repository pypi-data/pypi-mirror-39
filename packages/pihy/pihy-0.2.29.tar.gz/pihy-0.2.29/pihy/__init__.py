import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from .x import joke

def main():
  print('foo = ', 1)
  print(joke())

if __name__ == '__main__':
  main()
