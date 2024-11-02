# printer.py


def print_tables(tables):
    for relation in tables:
            print("---------------------------------------------------------------------------------------------")
            print(f"Relation: {relation.name}")
            print(f"Attributes: {relation.attributes}")
            print(f"Primary key: {relation.primary_key}")
            print(f"Canidate keys: {relation.candidate_keys}")
            print(f"Multivalued attributes: {relation.multivalued_attrs}")
            for fd in relation.fds:
                print(f"Functional dependencies:  {', '.join(fd.lhs)} -> {', '.join(fd.rhs)}")
            for mvd in relation.mvds:
                print(f"Multivalued Dependecies:  {', '.join(mvd.lhs)} -> {', '.join(mvd.rhs)}")