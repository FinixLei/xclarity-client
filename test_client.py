from pprint import pprint
from xclarityclient import client
from xclarityclient import exceptions


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

        # print('Setting power status...')
        # c.set_node_power_status(node_id, 'powerOn')
        # print('power status: %s' % c.get_node_power_status(node_id))

        if False:
            c.set_node_power_status(node_id, 'OnOn')
        if True:
            raise exceptions.NodeDetailsException(node_id=node_id, detail="Just Error!!!")

    except exceptions.BadRequestException as ex:
        print(ex.get_message())
    except exceptions.NodeDetailsException as ex:
        print(ex.get_message())
    except exceptions.FailToSetPowerStatusException as ex:
        print(ex.get_message())
    except Exception as ex:
        print("Error: %s" % str(ex))


if __name__ == '__main__':
    main()
