# Database-Normalization

Please look at the three json files for an example as to how to structure your input file. This program takes a json file in that structure and normalizes it to the the specified form and returns the schema. To run the program use *python3 main.py {input_file} {target_NF}* 
This program can normalize from 2nf-5nf (including BCNF). Access 2NF-5NF with 2-5 and BCNF with 3.5
The input json file can have multiple tables, functional dependecies, and Multi-valued dependencies. 
