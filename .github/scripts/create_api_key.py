import sys

from bioblend import galaxy
from bioblend.galaxy.users import UserClient

args = sys.argv

address = args[1]
master_key = args[2]

gi = galaxy.GalaxyInstance(url=address, key=master_key)
users = UserClient(gi)
u = users.get_users()[0]
key = users.create_user_apikey(u.get('id'))

print(key)


