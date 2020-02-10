#optie met alleen richting 0 en 2:
for entry in tempd:

    if len(test_data) < 10 and (entry[-1] == 0 or entry[-1] == 2):
        test_data.append(entry)

    elif len(test_data) == 10 and (entry[-1] == 0 or entry[-1] == 2):
        training_data.append(entry)

#optie met richting 1 2 en 3 als richting 1:
for entry in tempd:

    if entry[-1] == 2 or entry[-1] == 3:
        entry[-1] = 1  

    if len(test_data) < 20 :
        test_data.append(entry)

    else:
       training_data.append(entry)

# alle richtingen, random test:
for entry in tempd:

    if len(test_data) < 10 :
        test_data.append(entry)
    else:
       training_data.append(entry)

# alle richtingen, 1 specifieke richting
for entry in tempd:
    if len(test_data) < 10  and entry[-1] == 'vulrichting in, 0 1 2 3' :
        test_data.append(entry)
    else:
       training_data.append(entry)

