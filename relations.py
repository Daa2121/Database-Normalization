class Relation:
    def __init__(self, name, attributes, primary_key, candidate_keys, multivalued_attrs):
        self.name = name
        self.attributes = attributes
        self.primary_key = primary_key
        self.candidate_keys = candidate_keys
        self.multivalued_attrs = multivalued_attrs
        self.fds = []   # Store functional dependencies specific to this relation
        self.mvds = []  # Store multivalued dependencies specific to this relation
    
    def get_relation_by_name(tables, table_name):
    # Search for the relation with the specified table_name
        for relation in tables:
            if relation.name == table_name:
                return relation  # Return the found relation
        return None  # Return None if not found
    
    def print_relation_details(relation):
        if relation:
            print(f"Table Name: {relation.name}")
            print(f"Attributes: {', '.join(relation.attributes)}")
            print(f"Primary Key: {', '.join(relation.primary_key)}")
            print(f"Candidate Keys: {', '.join(relation.candidate_keys) if relation.candidate_keys else 'None'}")
            print(f"Multivalued Attributes: {', '.join(relation.multivalued_attrs) if relation.multivalued_attrs else 'None'}")
            
            # Print Functional Dependencies
            if relation.fds:
                print("Functional Dependencies:")
                for fd in relation.fds:
                    print(f"  {', '.join(fd.lhs)} -> {', '.join(fd.rhs)}")
            else:
                print("Functional Dependencies: None")
            
            # Print Multivalued Dependencies
            if relation.mvds:
                print("Multivalued Dependencies:")
                for mvd in relation.mvds:
                    print(f"  {', '.join(mvd.lhs)} -> {', '.join(mvd.rhs)}")
            else:
                print("Multivalued Dependencies: None")
        else:
            print("Relation not found.")
    

class FunctionalDependency:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class MultivaluedDependency:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

import json

def parse_input(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Dictionary to map table names to Relation objects
    table_dict = {}

    # Create Relation objects for each table and store them in table_dict
    for table in data['tables']:
        t = Relation(
            table['name'],
            table['attributes'],
            table['primary_key'],
            table['candidate_keys'],
            table['multivalued_attributes']
        )
        table_dict[table['name']] = t  # Use the table name as the key in table_dict
        print(f"Created Relation for table '{table['name']}' with attributes {t.attributes} and primary key {t.primary_key}")

    # Assign functional dependencies to the correct Relation based on table name
    for fd in data['functional_dependencies']:
        table_name = fd['table']  # 'table' field indicates which Relation this FD belongs to
        if table_name in table_dict:  # Ensure the table exists in table_dict
            dependency = FunctionalDependency(fd['lhs'], fd['rhs'])
            table_dict[table_name].fds.append(dependency)  # Append FD to the correct Relation
            print(f"Added Functional Dependency {fd['lhs']} -> {fd['rhs']} to table '{table_name}'")
        else:
            print(f"Error: Table '{table_name}' not found for FD {fd}")

    # Assign multivalued dependencies to the correct Relation based on table name
    for mvd in data['multivalued_dependencies']:
        table_name = mvd['table']  # 'table' field indicates which Relation this MVD belongs to
        if table_name in table_dict:  # Ensure the table exists in table_dict
            dependency = MultivaluedDependency(mvd['lhs'], mvd['rhs'])
            table_dict[table_name].mvds.append(dependency)  # Append MVD to the correct Relation
            print(f"Added Multivalued Dependency {mvd['lhs']} -> {mvd['rhs']} to table '{table_name}'")
        else:
            print(f"Error: Table '{table_name}' not found for MVD {mvd}")

    # Return only the list of Relation objects
    return list(table_dict.values())

# TEST INPUT
def main(input_file): 
    input = parse_input(input_file)
    table = Relation.get_relation_by_name(input, "Employee")
    Relation.print_relation_details(table)

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    main(input_file)

