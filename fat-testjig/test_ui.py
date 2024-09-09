import yaml


with open('names.yaml', 'r') as file:
    names = yaml.safe_load(file)

names = {}
names['test'] = 'value'
print(names)

with open('names.yaml', 'w') as file:
    yaml.dump(names, file)
