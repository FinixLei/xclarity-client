from xclarityclient import client
from pprint import pprint


def main():
    node_id = '2CA5B6C545F211E58CB5ADC3E29A7260'

    c = client.Client(version='xclarity_1.2.2',
                      username='USERID',
                      password='Passw0rd',
                      url='https://10.240.197.84')

    print('power status: %s' % c.get_node_power_status(node_id))
    pprint(c.get_node_boot_info(node_id))


if __name__ == '__main__':
    main()
