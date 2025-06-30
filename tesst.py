# user 1
# user 2
# user 3

# name
# age
# fuse


class Users:
    def __init__(self, name, age, fuse):
        self.name = name
        self.age = age
        self.fuse = fuse

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Fuse: {self.fuse}"


user_1 = Users("god", "115", True)
user_2 = Users("Ghost", "10000000", False)

print(user_1)
print(user_2)
