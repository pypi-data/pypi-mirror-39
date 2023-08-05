from user import User1
print(User1)
# u = User1('aman@cs.com')
# print(u.get_id())
token = User1.create_auth_token('aman@angrish.com')
u1 = User1.create_user(auth_id='aman@angrish.com', org='tn', role='dev')
print(u1)
# print(u1.ob.role)
u2, info = User1.get_by_auth_token('aman@angrish.com', token)
print(vars(u2.ob))
print(u2.get_id())


