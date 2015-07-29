import splunklib.client as client
import splunklib.results as results

Hosts = ['localhost']

PORT = 8089
USERNAME = 'admin'
PASSWORD = 'password'

for host in Hosts:
    service = client.connect(
        host=host,
        port=PORT,
        username=USERNAME,
        password=PASSWORD)

    for i in xrange(50):
        service.users.create('power_user_{0}'.format(str(i)), 'password', 'power')
        service.users.create('can_delete_user_{0}'.format(str(i)), 'password', 'can_delete')
        service.users.create('user_{0}'.format(str(i)), 'password', 'user')
        service.users.create('admin_user_{0}'.format(str(i)), 'password','admin')

    print '{0} | {1} | {2}'.format('USERNAME','PASSWORD','ROLES')
    for user in service.users:
        print '{0} | {1} | {2}'.format(user.name,'password',user.name.split('_')[0])