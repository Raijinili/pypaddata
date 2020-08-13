# Assert that skill_data fits our assumptions.

#TODO:
#- SKP doesn't contain 0s.
#- All skills of a given type have the same number of params.
    #- I.e. nonzero params.
#+ Alert if:
    #- Unknown skilltype.
    #- Unknown skill param value.
    #? Shouldn't this just raise some exceptions?
        #- Ideally allowing one to change things and resume without restarting.
#+ Also alert:
    #- Something changed.
    #- [5] = ""
    #- Min length 6.



