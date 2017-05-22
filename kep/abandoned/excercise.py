# ---------------------------------

#groups consume a copy of more_def 
groups = [main_def]
print("Main parsing definition:\n", groups)

more_def2 = more_def.copy()
while more_def2:
    p = more_def2.pop()
    cur_group = [p]
    for d in more_def2:
        if d.has_same_scope(p):
            cur_group.append(d)
            more_def2.remove(d)
    print()
    print (cur_group)               
    groups.append(cur_group)
# ---------------------------------
