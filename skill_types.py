## Types for skill_data.
    #- Generates descriptions.
    #- Categorization.


## There are two ways to specify descs:
    #- Functions for each type.
    #- Description format strings.
        #- E.g.:
            #- "Deals $pc1x Atk $E2 damage to all enemies."
                #- Means:
                    #- pc1: skp1, as a percent.
                    #- E2: skp2, as an element, capitalized.

## Decisions:
    #- Separate class for each type.
    #- 


## Leader skills:
    #- Needs:
        #- Desc.
        #- Max multiplier.
        #- Max multiplier for an attr/type sets pair.



skill_types = {}

def sktp(i, categories=()):
    """...
    """
    #! Some descs work for more than one type.
    #! Registrar for active and leader must be separate.
    def registrar(f):
        skill_types[i] = f
        return f
    return registrar


@sktp(0)
def damage(args):
    ...



## Description formats.
    #= Maps skilltype to a function that takes params.
    #- Types:
        #- Function. (Called on list of skill params.)
            #? Should it be `f(skp)` or `f(*skp)`?
desc_maker = {
    
}


