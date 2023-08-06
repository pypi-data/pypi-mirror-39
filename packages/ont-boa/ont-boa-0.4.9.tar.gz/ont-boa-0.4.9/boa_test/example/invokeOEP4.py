from boa.interop.Neo.App import RegisterAppCall

OEP4Contract = RegisterAppCall('1b86175747d0c1490d5b48b20b10584e378ed947', 'operation', 'args')


def Main(operation, args):
    if operation == 'transfer':
        return OEP4Contract('transfer', args)

    return False
