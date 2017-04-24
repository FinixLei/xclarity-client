from xclarityclient import client
from pprint import pprint


def main():
    node_id = '2CA5B6C545F211E58CB5ADC3E29A7260'

    c = client.Client(version='xclarity_1.2.2',
                      username='USERID',
                      password='Passw0rd',
                      url='https://10.240.197.84')

    try:
        print('node status: %s' % c.get_node_status(node_id))
        print('power status: %s' % c.get_node_power_status(node_id))
        print('boot info: ')
        pprint(c.get_node_boot_info(node_id))

        # print('Powering on the node...')
        # c.set_node_power_status(node_id, 'powerOn')
        # print('power status: %s' % c.get_node_power_status(node_id))
    except Exception as ex:
        print("Error: %s" % str(ex))


if __name__ == '__main__':
    main()
