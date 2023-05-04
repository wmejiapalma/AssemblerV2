What is this?
=============
This is a simple assembler for the ARM architecture used in raspberry pi 4. It is written in python.

## How to use
1. Write your assembly code in the "input.txt" file.
2. Run the main.py file.
3. The output will be in the "kernel7.img" file.

## How to write assembly code
The assembly code is written in the "input.txt" file. The assembly code is written in the following format:
```
instruction arg1, arg2 ... #destinationTag or :gotoTag
```
The tags are optional but they make writing the code easier

