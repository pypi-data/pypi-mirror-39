#!/usr/bin/env python3
import argparse
import os.path
import re
import zipfile

from typing import Any, Dict, List, Optional, Tuple

import epub_meta

def get_chapter_title(mdata:List[Dict[str, Any]], fname:str) -> Optional[Tuple[str, int]]:
    found_list = [(x['title'], x['index']) for x in mdata if x['src'] == fname]
    if len(found_list) > 0:
        chap_title = found_list[0][0].strip(' \t.0123456789')
        return chap_title, found_list[0][1]
    else:
        return ('Unknown', 0)


def grep_book(filename:str, pattern:str, flags:int):
    assert os.path.isfile(filename), "{} is not EPub file.".format(filename)
    sought_RE = re.compile(pattern, flags)

    metadata = epub_meta.get_epub_metadata(filename)
    book = zipfile.ZipFile(filename)

    for zif in book.infolist():
        with book.open(zif) as inf:
            printed_title = False
            for line in inf:
                decoded_line = line.decode()
                if sought_RE.search(decoded_line):
                    if not printed_title:
                        chap_info = get_chapter_title(metadata.toc,
                                                          zif.filename)
                        print("{}. {}:\n".format(chap_info[1], chap_info[0]))
                        printed_title = True
                    print(decoded_line)

def main():
    parser = argparse.ArgumentParser(description='Grep through EPub book')
    parser.add_argument('pattern')
    parser.add_argument('filename')
    parser.add_argument('-i', '--ignore-case',
                        action='store_true',
                        help="make search case insensitive")
    args = parser.parse_args()

    search_flags = 0
    if args.ignore_case:
        search_flags |= re.I

    book_fname = os.path.realpath(args.filename)
    grep_book(book_fname, args.pattern, search_flags)

if __name__ == "__main__":
    main()
