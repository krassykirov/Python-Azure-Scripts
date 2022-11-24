#!/usr/bin/python3
from pathlib import Path
import re
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pattern', type=str,required=True)
    parser.add_argument('--path', type=str,required=True)
    return parser.parse_args()

def grep(text_to_search, path):
    s = time.perf_counter()
    if not Path(path).exists():
        print(f'{path}", No such path!')
        return
    elif Path(path).exists() and Path(path).is_file():
        print(f'Looking for "{text_to_search}" in "{path}"\n')
        try:
            with open(path, 'r') as path:
                if re.findall(text_to_search, path.read()):
                    print(f'Found "{text_to_search}" in "{path.name}"')
        except Exception as e:
            pass
    elif Path(path).exists() and Path(path).is_dir():
         print(f'Looking for "{text_to_search}" in "{path}"')
         for file in Path(path).rglob("*"):
             if Path(file).is_file():
                 try:
                     with open(file,'r') as path:
                        if re.findall(text_to_search,path.read()):
                            print(f'Found "{text_to_search}" in "{path.name}"')
                 except Exception as e:
                     pass
    elapsed = time.perf_counter() - s
    print('###############')
    print(f"Script executed in {elapsed:0.2f} seconds.")

def grep2(text_to_search, path):
    s = time.perf_counter()
    if not Path(path).exists():
        print(f'{path}", No such path!')
        return
    elif Path(path).exists() and Path(path).is_file():
        print(f'Looking for "{text_to_search}" in "{path}"\n')
        try:
            with open(path, 'r') as path:
                for line_i,line in enumerate(path,1):
                    if re.search(text_to_search, line):
                        print(f'{path.name}:{line_i}: {line}',end='')
        except Exception as e:
            pass
    elif Path(path).exists() and Path(path).is_dir():
         print(f'Looking for "{text_to_search}" in "{path}"')
         for file in Path(path).rglob("*"):
             if Path(file).is_file():
                 print(file)
                 try:
                     with open(file,'r') as path:
                         for line_i, line in enumerate(path, 1):
                             if re.search(text_to_search, line):
                                 print(f'{path.name}:{line_i}: {line}',end='')
                 except Exception as e:
                     # print(e)
                     pass
    elapsed = time.perf_counter() - s
    print(f"Script executed in {elapsed:0.2f} seconds.")

args = parse_args()

if args.pattern and args.path:
    pattern = args.pattern
    path = args.path
    grep2(pattern, path)


# async def grep2(text_to_search, path):
#     if not Path(path).exists():
#         print(f'{path}", No such path!')
#         return
#     elif Path(path).exists() and Path(path).is_dir():
#          print(f'Looking for "{text_to_search}" in "{path}"\n')
#          for file in Path(path).rglob("*"):
#              if Path(file).is_file():
#                  try:
#                      async with aiofiles.open(file, 'r') as f:
#                         if re.findall(text_to_search, f.read()):
#                             print(file, Path(path))
#                  except Exception as e:
#                      pass


# async def main():
#     s = time.perf_counter()
#     task = asyncio.create_task(grep2('krassy@CentOS',path2))
#     result = await task
#     print(result)
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")

# print("#####################")
# asyncio.run(main())
