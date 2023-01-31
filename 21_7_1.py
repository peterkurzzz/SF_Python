from cat_cl import Cat

cat_param = ['name', 'gender', 'age']
cat_value = [['Lucy', 'female', 1],
             ['Sam', 'male', 2]]

for i in range(len(cat_value)):
    param = dict(zip(cat_param, cat_value[i]))
    pet_cat = Cat(**param)
    print(f'Name: {pet_cat.name}, gender: {pet_cat.gender}, age: {pet_cat.age}')


