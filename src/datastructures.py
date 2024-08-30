
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self.familia_id = self._generateId()
        # example list of members
        self._members = []
        self.add_member("John", 33, [7, 13, 22])
        self.add_member("Tommy", 23, [34,65,23,4,6], 3443)
        self.add_member("Jimmy", 5, [1])

    def _generateId(self):
        return randint(0, 99999999)


    def add_member(self, firs_name, age, numeros, id=None):
        if age <= 0:
            return {"error": "La edad tiene que ser mayor a cero", "status": 400}
        
        member = {
            "id": id if id is not None else self._generateId(),
            "first_name": firs_name,
            "last_name": self.last_name,
            "age": age,
            "lucky_numbers": numeros
        }
        
        self._members.append(member)
        return {"mensaje": "Miembro agregado exitosamente", "status": 200}


    def delete_member(self, id):
        for i, miembro in enumerate(self._members):
            if miembro["id"] == id:
                self._members.pop(i)
                return {"done": True} 
        return {"error": "Id no encontrado", "status": 400}



    def get_member(self, id):
        for miembro in self._members:
            if miembro["id"] == id:
                return {"miembro": miembro, "status": 200}
        return {"error": "id no encontrado", "status": 400}    
        

    
    def get_all_members(self):
        return self._members
