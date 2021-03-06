menu_name = "Wireless"
#Some globals for LCS
callback = None
#Some globals for us
main_menu = None
i = None
o = None

from time import sleep

from ui import Menu, Printer, MenuExitException

import wpa_cli

def show_networks():
    network_menu_contents = []
    networks = wpa_cli.get_scan_results()
    for network in networks:
        network_menu_contents.append([network['ssid'], lambda x=network: network_info_menu(x)])
    network_menu_contents.append(["Exit", 'exit'])
    network_menu = Menu(network_menu_contents, i, o, "Wireless network menu")
    network_menu.activate()

def network_info_menu(network_info):
    network_info_contents = [
    ["Connect", lambda x=network_info: connect_to_network(x)],
    ["BSSID", lambda x=network_info['bssid']: Printer(x, i, o, 5, skippable=True)],
    ["Frequency", lambda x=network_info['frequency']: Printer(x, i, o, 5, skippable=True)],
    ["Open" if wpa_cli.is_open_network(network_info) else "Secured", lambda x=network_info['flags']: Printer(x, i, o, 5, skippable=True)],
    ["Exit", 'exit']]
    network_info_menu = Menu(network_info_contents, i, o, "Wireless network info")
    network_info_menu.activate()

def connect_to_network(network_info):
    #First, looking in the known networks
    configured_networks = wpa_cli.list_configured_networks()
    for network in configured_networks:
        if network_info['ssid'] == network['ssid']:
            Printer([network_info['ssid'], "known,connecting"], i, o, 1)
            wpa_cli.select_network(network['network id'])
            return True
    #Then, if it's an open network, just connecting
    if wpa_cli.is_open_network(network_info):
        network_id = wpa_cli.add_network()
        Printer(["Network is open", "adding to known"], i, o, 1)
        wpa_cli.set_network(network_id, 'ssid', '"'+network_info['ssid']+'"')
        wpa_cli.set_network(network_id, 'key_mgmt', 'NONE')
        Printer(["Connecting to", network_info['ssid']], i, o, 1)
        wpa_cli.select_network(network_id)
        return True
    #No passkey/WPS PIN input possible yet and I cannot yet test WPS button functionality.
    else:
        o.display_data("Network password", "unknown")
        sleep(1)
        return False

def scan():
    try:
        wpa_cli.initiate_scan()
    except wpa_cli.WPAException as e:
        if e.code=="FAIL-BUSY":
            Printer("Still scanning...", i, o, 1)
        else:
            raise
    else:
        Printer("Scanning...", i, o, 1)
    finally:
        sleep(1)

def wireless_status():
    w_status = wpa_cli.connection_status()
    state = w_status['wpa_state']
    status_menu_contents = [[["state:", state]]] #State is an element that's always there, let's see possible states
    if state == 'COMPLETED':
        #We have bssid, ssid and key_mgmt at least
        status_menu_contents.append(['SSID: '+w_status['ssid']])
        status_menu_contents.append(['BSSID: '+w_status['bssid']])
        key_mgmt = w_status['key_mgmt']
        status_menu_contents.append([['Security:', key_mgmt]])
        #If we have WPA in key_mgmt, we also have pairwise_cipher and group_cipher set to something other than NONE so we can show them
        if key_mgmt != 'NONE':
            group = w_status['group_cipher']
            pairwise = w_status['pairwise_cipher']
            status_menu_contents.append([['Group/Pairwise:', group+"/"+pairwise]])
    elif state in ['AUTHENTICATING', 'SCANNING', 'ASSOCIATING']:
        pass #These states don't have much information
    #In any case, we might or might not have IP address info
    status_menu_contents.append([['IP address:',w_status['ip_address'] if 'ip_address' in w_status else 'None']])
    #We also always have WiFi MAC address as 'address'
    status_menu_contents.append(['MAC: '+w_status['address']])
    status_menu = Menu(status_menu_contents, i, o, "Wireless status menu", entry_height=2)
    status_menu.activate()

def change_interface():
    #This function builds a menu out of all the interface names, each having a callback to show_if_function with interface name as argument
    menu_contents = []
    interfaces = wpa_cli.get_interfaces()
    for interface in interfaces:
        menu_contents.append([interface, lambda x=interface: change_current_interface(x)])
    menu_contents.append(["Exit", 'exit'])
    interface_menu = Menu(menu_contents, i, o, "Interface change menu")
    interface_menu.activate()

def change_current_interface(interface):
    try:
        wpa_cli.set_active_interface(interface)
    except wpa_cli.WPAException:
        Printer(['Failed to change', 'interface'], i, o, skippable=True)
    else:
        Printer(['Changed to', interface], i, o, skippable=True)
    finally:
        raise MenuExitException
        
def save_changes():
    try:
        wpa_cli.save_config()
    except wpa_cli.WPAException:
        Printer(['Failed to save', 'changes'], i, o, skippable=True)
    else:
        Printer(['Saved changes'], i, o, skippable=True)
        
def launch():
    try:
       current_interface = wpa_cli.get_current_interface()
    except OSError as e:
       if e.errno == 2:
           Printer(["Do you have", "wpa_cli?"], i, o, 3, skippable=True)
           return
       else:
           raise e
    except wpa_cli.WPAException:
        Printer(["Do you have", "wireless cards?", "Is wpa_supplicant", "running?"], i, o, 3, skippable=True)
        return
    else:
        main_menu_contents = [
        [current_interface, change_interface],
        ["Scan", scan],
        ["Networks", show_networks],
        ["Status", wireless_status],
        ["Save changes", save_changes],
        #["Saved networks", manage_saved_networks],
        ["Exit", 'exit']]
        main_menu = Menu(main_menu_contents, i, o, "wpa_cli main menu")
        main_menu.activate()


def init_app(input, output):
    global callback, main_menu, i, o
    i = input; o = output
    callback = launch
