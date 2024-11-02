# normalizer.py
from relations import Relation

def is_1nf(tables):
    """Checks if the relation is in 1NF by ensuring there is a primary key and there are no multivalued attributes."""
    for relation in tables:
        if len(relation.primary_key) == 0:
            print(f"Error not in 1nf because there isn't a primary key for relation {relation.name}")
            return False
    else:
        return True

def decompose_2NF(tables):
    if is_1nf(tables):
        for relation in tables:
            # Create a copy of fds to safely iterate over it while modifying the original list
            fd_copy = relation.fds[:]
            for fd in fd_copy:
                if set(fd.lhs).issubset(set(relation.primary_key)) and not set(fd.lhs) == set(relation.primary_key): #Find partial dependencies 

                    attributes = list(fd.lhs) + list(fd.rhs)

                    #create new relation for the partial funcitonal dependency 
                    tables.append(Relation(
                        fd.rhs[0],
                        attributes,
                        fd.lhs,
                        [],
                        [],))
                    new = Relation.get_relation_by_name(tables, fd.rhs[0])
                    new.fds.append(fd) #get new relation and copy the functional dependency from previous relation

                    #Remove attributes that violate 2NF
                    for i in fd.rhs:
                        for j in relation.attributes:
                            if i == j:
                                relation.attributes.remove(j)


                    relation.fds.remove(fd) #remove the partial functional dependency  from original relation
        print("All tables are now in 2NF")
        
def decompose_3NF(tables):
    decompose_2NF(tables)
    for relation in tables:
        # Create a copy of fds to safely iterate over it while modifying the original list
        fd_copy = relation.fds[:]
        for fd in fd_copy:
            lhs_is_superkey = set(fd.lhs) == set(relation.primary_key)
            rhs_is_prime = all(attr in relation.primary_key for attr in fd.rhs)
            
            # Check if it violates 3NF
            if not lhs_is_superkey and not rhs_is_prime:
                # Attributes for the new relation based on this transitive dependency
                attributes = list(fd.lhs) + list(fd.rhs)
                
                # Create a new relation for the transitive dependency
                tables.append(Relation(
                    fd.rhs[0],  # Using the first attribute of RHS as the new relation name for simplicity
                    attributes,
                    fd.lhs,  # Use the LHS as the primary key for the new relation
                    [],
                    []
                ))
                
                # Add the functional dependency to the new relation
                new_relation = Relation.get_relation_by_name(tables, fd.rhs[0])
                new_relation.fds.append(fd)
                
                # Remove transitive attributes from the original relation
                for attr in fd.rhs:
                    if attr in relation.attributes:
                        relation.attributes.remove(attr)
                        
                
                # Remove the transitive dependency from the original relation
                relation.fds.remove(fd)

    print("All tables are now in 3NF")

def decompose_BCNF(tables):
    # Ensure tables are in 3NF first
    decompose_3NF(tables)

    def is_superkey(relation, attributes):
        # Helper function to check if a set of attributes forms a superkey
        return set(relation.primary_key).issubset(set(attributes))

    for relation in tables:
        # Create a copy of fds to safely iterate over it while modifying the original list
        fd_copy = relation.fds[:]
        for fd in fd_copy:
            lhs_is_superkey = is_superkey(relation, fd.lhs)

            # Check if it violates BCNF
            if not lhs_is_superkey:
                # Attributes for the new relation based on this BCNF violation
                attributes = list(fd.lhs) + list(fd.rhs)
                
                # Create a new relation for the BCNF violation
                new_relation_name = f"{relation.name}_decomp_{len(tables)}"  # Name for the new relation
                tables.append(Relation(
                    new_relation_name,
                    attributes,
                    fd.lhs,  # Use the LHS as the primary key for the new relation
                    [],
                    []
                ))
                
                # Add the functional dependency to the new relation
                new_relation = Relation.get_relation_by_name(tables, new_relation_name)
                new_relation.fds.append(fd)
                
                # Remove BCNF-violating attributes from the original relation
                for attr in fd.rhs:
                    if attr in relation.attributes:
                        relation.attributes.remove(attr)
                        relation.primary_key.remove(attr)
                
                # Remove the violating dependency from the original relation
                relation.fds.remove(fd)
    print("All tables are now in BCNF")

def decompose_4NF(tables):
    # Ensure tables are in BCNF first to handle 3NF, BCNF violations
    decompose_BCNF(tables)

    for relation in tables:
        # Create a copy of mvds to safely iterate over it while modifying the original list
        mvds_copy = relation.mvds[:]
        
        for mvd in mvds_copy:  # Check each multi-valued dependency in the copied list
            lhs_is_superkey = set(relation.primary_key).issubset(set(mvd.lhs))

            # Check if it violates 4NF
            if not lhs_is_superkey:
                # Create attributes for the new relation based on this multi-valued dependency
                attributes = list(mvd.lhs) + list(mvd.rhs)
                name = f"{mvd.rhs[0]} MVD"
                tables.append(Relation(
                    name,
                    attributes,
                    mvd.lhs,  # Use LHS of MVD as the primary key for the new relation
                    [],
                    []
                ))

                # Add the multi-valued dependency to the new relation
                new_relation = Relation.get_relation_by_name(tables, name)
                new_relation.mvds.append(mvd)

                # Remove the multi-valued dependency from the original relation
                relation.mvds.remove(mvd)  # Safely remove from the original mvds list
        if len(relation.fds) == 0 and len(relation.mvds) == 0:
            tables.remove(relation)

    print("All tables are now in 4NF")

def decompose_5NF(tables):
    # Ensure tables are in 4NF first to handle any existing multi-valued dependencies
    decompose_4NF(tables)

    while True:  # Loop until no more decompositions occur
        decomposed = False  # Reset at the beginning of each iteration

        for relation in tables:
            # Create a copy of FDs to safely iterate over it while modifying the original list
            fd_copy = relation.fds[:]

            for fd in fd_copy:
                lhs = fd.lhs
                rhs = fd.rhs

                # Check if the lhs of the functional dependency is a superkey
                if not set(lhs).issubset(set(relation.primary_key)):
                    # Form the new relation for the join dependency
                    new_relation_name = f"{fd.rhs[0]} JD"
                    new_attributes = list(lhs) + list(rhs)

                    # Create the new relation
                    new_relation = Relation(
                        new_relation_name,
                        new_attributes,
                        lhs,  # Use LHS as primary key
                        [],
                        []
                    )

                    # Add the new relation to the tables
                    tables.append(new_relation)

                    # Remove the attributes that are part of the join dependency from the original relation
                    for attr in new_attributes:
                        if attr in relation.attributes:
                            relation.attributes.remove(attr)

                    # Copy the functional dependency to the new relation
                    new_relation.fds.append(fd)

                    # Remove the FD from the original relation
                    relation.fds.remove(fd)

                    decomposed = True  # Set decomposed to True when a decomposition happens

            # Clean up empty relations
            if len(relation.fds) == 0 and len(relation.mvds) == 0:
                tables.remove(relation)

        if not decomposed:  # Exit the loop if no decompositions occurred in this iteration
            break

    print("All tables are now in 5NF")

def normalize(tables, target_nf):

    if target_nf == 2:
        decompose_2NF(tables)
    elif target_nf == 3: 
        decompose_3NF(tables)
    elif target_nf == 3.5:
        decompose_BCNF(tables)
    elif target_nf == 4:
        decompose_4NF(tables)
    elif target_nf == 5:
        decompose_5NF(tables)
    else:
        print("Error please input 2-5 for 2NF-5NF and 3.5 for BCNF")

