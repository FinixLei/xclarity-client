from functools import wraps
from pprint import pprint
from xclarityclient import client
from xclarityclient import exceptions


def show_delimiter(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print('Testing %s: ' % fn.__name__)
        result = fn(*args, **kwargs)
        print('-' * 50)
        return result
    return wrapper


@show_delimiter
def test_get_node_status(c, node_id):
    print('node status: %s' % c.get_node_status(node_id))


@show_delimiter
def test_get_node_power_status(c, node_id):
    node_power_status = c.get_node_power_status(node_id)
    print('power status: %s' % node_power_status)
    return node_power_status


@show_delimiter
def test_get_node_boot_info(c, node_id):
    print('boot info: ')
    pprint(c.get_node_boot_info(node_id))


@show_delimiter
def test_set_node_power_status_on(c, node_id):
    print('Power on node %s...' % node_id)
    c.set_node_power_status(node_id, 'POWER_ON')


@show_delimiter
def test_set_node_power_status_off(c, node_id):
    print('Power off node %s...' % node_id)
    c.set_node_power_status(node_id, 'POWER_OFF')


@show_delimiter
def test_node_details_exception(node_id):
    try:
        raise exceptions.NodeDetailsException(node_id=node_id, detail="Just Error!!!")
    except exceptions.NodeDetailsException as ex:
        print('Got NodeDetailsException: %s, its code is %s' % (ex.get_message(), ex.get_code()))


@show_delimiter
def test_fail_to_set_power_status_exception(node_id):
    try:
        raise exceptions.FailToSetPowerStatusException(node_id=node_id, action='PowerOn')
    except exceptions.FailToSetPowerStatusException as ex:
        print('Got FailToSetPowerStatusException: %s, its code is %s'
              % (ex.get_message(), ex.get_code()))


@show_delimiter
def test_fail_to_set_boot_info_exception(node_id):
    try:
        raise exceptions.FailToSetBootInfoException(node_id=node_id)
    except exceptions.FailToSetBootInfoException as ex:
        print('Got FailToSetBootInfoException: %s, its code is %s. '
              % (ex.get_message(), ex.get_code()))


@show_delimiter
def test_bad_power_status_setting_exception(c, node_id):
    try:
        c.set_node_power_status(node_id, 'OnOn')
    except exceptions.BadPowerStatusSettingException as ex:
        print('Got BadPowerStatusSettingException: %s, its code is %s'
              % (ex.get_message(), ex.get_code()))


@show_delimiter
def test_get_node_all_boot_info(c, node_id):
    print("All boot info for node %s: " % node_id)
    pprint(c.get_node_all_boot_info(node_id))


@show_delimiter
def test_set_node_boot_info(c, node_id):
    def _validate_pxe_boot_item_in_permanent(timepoint):
        boot_order = c.get_node_all_boot_info(node_id)
        for item in boot_order['bootOrder']['bootOrderList']:
            del(item['possibleBootOrderDevices'])
            if item['bootType'].lower() == 'permanent':
                permanent_item = item
                boot_order['bootOrder']['bootOrderList'] = [item]
                break

        if permanent_item is None:
            print('No Permanent boot info')
            return

        if boot_order['bootOrder'].get('uri', None):
            del(boot_order['bootOrder']['uri'])

        print('>>>>> After getting boot info: >>>>>>>>>')
        pprint(boot_order)
        print('<<<<<<<<<<<<<<<<<<<<<<<')

        target_device = 'PXE Network'
        current_boot_devices = permanent_item['currentBootOrderDevices']
        if target_device in current_boot_devices:
            print('%s setting, there IS %s in Permanent boot item'
                  % (timepoint, target_device))
            current_boot_devices.remove(target_device)
            if len(current_boot_devices) == 0:
                current_boot_devices.append('None')
        else:
            print('%s setting, there is NO %s in Permanent boot item'
                  % (timepoint, target_device))
            current_boot_devices.append(target_device)
            if 'None' in current_boot_devices:
                current_boot_devices.remove('None')

        if timepoint == 'Before':
            print('>>>>> After adjusting the boot info: >>>>>>>>>>>>>')
            pprint(boot_order)
            print('<<<<<<<<<<<<<<<<<<<<<<<')

        return boot_order

    boot_order = _validate_pxe_boot_item_in_permanent('Before')
    c.set_node_boot_info(node_id, boot_order)
    _validate_pxe_boot_item_in_permanent('After')


def main():
    node_id = '2CA5B6C545F211E58CB5ADC3E29A7260'

    c = client.Client(version='xclarity_1.2.2',
                      username='USERID',
                      password='Passw0rd',
                      url='https://10.240.197.84')

    test_get_node_status(c, node_id)
    test_get_node_all_boot_info(c, node_id)
    test_get_node_boot_info(c, node_id)
    # test_set_node_boot_info(c, node_id)  # Time cost operation

    # Test Exceptions
    test_node_details_exception(node_id)
    test_fail_to_set_power_status_exception(node_id)
    test_bad_power_status_setting_exception(c, node_id)
    test_fail_to_set_boot_info_exception(node_id)

    # Test Power Status
    power_status = test_get_node_power_status(c, node_id)
    if False:  # Time cost operation
        if power_status == 'off':
            test_set_node_power_status_on(c, node_id)
        elif power_status == 'on':
            test_set_node_power_status_off(c, node_id)
        else:
            print('Unknown power status %s for node %s. ' % (power_status, node_id))


if __name__ == '__main__':
    main()
