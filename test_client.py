from pprint import pprint
from xclarityclient import client
from xclarityclient import exceptions


def test_get_node_status(c, node_id):
    print('node status: %s' % c.get_node_status(node_id))


def test_get_node_power_status(c, node_id):
    node_power_status = c.get_node_power_status(node_id)
    print('power status: %s' % node_power_status)
    return node_power_status


def test_get_node_boot_info(c, node_id):
    print('boot info: ')
    pprint(c.get_node_boot_info(node_id))


def test_set_node_power_status_on(c, node_id):
    print('Power on node %s...' % node_id)
    c.set_node_power_status(node_id, 'POWER_ON')


def test_set_node_power_status_off(c, node_id):
    print('Power off node %s...' % node_id)
    c.set_node_power_status(node_id, 'POWER_OFF')


def test_node_details_exception(node_id):
    try:
        raise exceptions.NodeDetailsException(node_id=node_id, detail="Just Error!!!")
    except exceptions.NodeDetailsException as ex:
        print('Got NodeDetailsException: %s, its code is %s' % (ex.get_message(), ex.get_code()))


def test_fail_to_set_power_status_exception(node_id):
    try:
        raise exceptions.FailToSetPowerStatusException(node_id=node_id, action='PowerOn')
    except exceptions.FailToSetPowerStatusException as ex:
        print('Got FailToSetPowerStatusException: %s, its code is %s'
              % (ex.get_message(), ex.get_code()))


def test_bad_power_status_setting_exception(c, node_id):
    try:
        c.set_node_power_status(node_id, 'OnOn')
    except exceptions.BadPowerStatusSettingException as ex:
        print('Got BadPowerStatusSettingException: %s, its code is %s'
              % (ex.get_message(), ex.get_code()))


def main():
    node_id = '2CA5B6C545F211E58CB5ADC3E29A7260'

    c = client.Client(version='xclarity_1.2.2',
                      username='USERID',
                      password='Passw0rd',
                      url='https://10.240.197.84')

    test_get_node_status(c, node_id)
    test_get_node_boot_info(c, node_id)
    power_status = test_get_node_power_status(c, node_id)

    if power_status == 'off':
        test_set_node_power_status_on(c, node_id)
    elif power_status == 'on':
        test_set_node_power_status_off(c, node_id)
    else:
        print('Unknown power status %s for node %s. ' % (power_status, node_id))

    test_node_details_exception(node_id)
    test_fail_to_set_power_status_exception(node_id)
    test_bad_power_status_setting_exception(c, node_id)


if __name__ == '__main__':
    main()
