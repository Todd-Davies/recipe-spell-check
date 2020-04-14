import argparse
import json
import sys
import os
import unidecode
from subprocess import Popen, PIPE
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    parser.add_argument('--dictionary', type=str, default=None, help='The custom dictionary to use.')
    args = parser.parse_args(argv)

    dictionary_flag = ("--add-extra-dicts=" + os.path.abspath(args.dictionary)) if args.dictionary else ""

    retval = 0
    for filename in args.filenames:
        # ignore non-html files
        if not filename.endswith('.html'):
          pass

        with open(filename, 'rb') as f:
            print("Spell checking ", filename)
            process=Popen(['aspell', 'list', '--mode=sgml',dictionary_flag],
                                     stdin=PIPE,
                                     stdout=PIPE,
                                     stderr=PIPE)
            inputdata=f.read()
            input_str = inputdata.decode("utf-8")
            sanitized_input = unidecode.unidecode(input_str)
            stdoutdata,stderrdata=process.communicate(input=sanitized_input.encode('utf-8'))
            if stderrdata:
              print("Failed to spellcheck", filename.strip())
              print(stderrdata.decode("utf-8"))
              retval += 1
            elif stdoutdata:
              print("Found the following issues for ", filename.strip())
              results = stdoutdata.decode("utf-8")
              print('\n'.join(sorted(list(dict.fromkeys(results.split())))))
              print()
              retval += 1
    return retval


if __name__ == '__main__':
    exit(main())
