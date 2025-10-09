import json

print("Interface Status")
print("================================================================================")
print("{:<50} {:<20} {:<10} {:<5}".format("DN", "Description", "Speed", "MTU"))  
print("-------------------------------------------------- -------------------- -------  -------")

with open("sample-data.json", "r") as obj:
    data = json.load(obj)
    for obj_item in data['imdata']:
        dn = obj_item['l1PhysIf']['attributes']['dn']
        descr = obj_item['l1PhysIf']['attributes']['descr']
        speed = obj_item['l1PhysIf']['attributes']['speed']
        mtu = obj_item['l1PhysIf']['attributes']['mtu']
        print("{:<50} {:<20} {:<10} {}".format(dn, descr, speed, mtu))