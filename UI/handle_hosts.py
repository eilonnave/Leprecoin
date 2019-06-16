from core_code.database import HostNodes
from core_code.logger import Logging

hosts_db = HostNodes(
    Logging('handle_hosts_file').logger)
stop = False
while not stop:
    respond = raw_input('to add address enter- a'
                        '\nto remove address enter -r'
                        '\nto exit enter e\n')
    if respond == 'a':
        address = raw_input('enter address to add\n')
        hosts_db.insert_address(address)
    elif respond == 'r':
        address = raw_input('enter address to remove\n')
        addresses = hosts_db.extract_hosts()
        if address in addresses:
            index = addresses.index(address)
            hosts_db.delete_node(index)
    elif respond == 'e':
        stop = True
        hosts_db.close_connection()
