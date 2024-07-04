# CO_Project
CO Group Project
This repository is a python program of a custom-made assembler designed to translate assembly language code into machine code for a specific 
computer architecture (ISA) and a custom-made simulator designed to execute instuctions from binary file generated from assembler.
There is a folder in the repository named "CO-Project" which has the python files for the both the assembler & simulator, bonus Q4 readme file along with bonus part testcases along with their bins & traces.

Description - 
The assembler program will convert an assembly language code to machine language(Binary Format). 
The program is able to handle all the supported instructions of the ISA, labels & variables along with three floating point instruction (addf, subf & movf)
The program is able to generate errors for different types of invalid instructions along with the line no. in which the error is encountered.
The simulator program will read the machine code & execute the instructions. It is able to handle several operations, computations & check for overflows.
The assembler & simulator are also capable of handling floating point computations (addf, subf & movf)
Bonus part -->
The assembler & simulator also handles 5 instructions that we have designed on our own i.e. increment, decrement, left rotate, right rotate & swap. A brief description of these instructions are given in the readmeQ4.md file.

Input/Output - 
The assembler reads the assembly program as an input text file using sys.stdin and supports automated testing.
It prints the binary format of the respective instructions if the assembly program is error free.
The simulator reads the binary file as an input text file using sys.stdin & supports automated testing. 
It prints the program counter & register values after each execution of instruction & also the entire "memory dump" at the end.

Error Handling & flag register - 
The errors present in the assembly code will be printed along with the line number in which the error is encountered. 
The error handling has been done using IF-ELSE and exit() function.
The flag register is set by overflows & comparison instruction. 


Contributions - 
Prakhar Agrawal - 2022361 (prakhar22361@iiitd.ac.in)
Shobhit Raj - 2022482 (shobhit22482@iiitd.ac.in)
Souparno Ghose - 2022506 (souparno22506@iiitd.ac.in)
Sujal Soni - 2022513 (sujal22513@iiitd.ac.in)
