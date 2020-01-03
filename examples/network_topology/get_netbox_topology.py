import pynetbox
import pandas as pd
import logging
import json
import random
import pprint

def get_netbox_connections(nb_token,nb_url):
    NB_TOKEN = nb_token
    NB_URL = nb_url
    nb = pynetbox.api(url=NB_URL, token=NB_TOKEN, ssl_verify=False)
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(lineno)s) - %(levelname)s: %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel('INFO')

    network_map = []

    logger.info('Get all routers from netbox')
    # get all routers
    routers = nb.dcim.devices.filter(
        role='router')
    # generate a list of strings instead of objects
    routers_list = ', '.join([str(x) for x in routers])
    for rtr in routers:
        logger.info('Get all interface connection for router %s' % rtr)
        interface_connection = nb.dcim.interface_connections.filter(
            device=rtr)
        rtr_interface = [
            interface for interface in interface_connection if interface.interface_a.device.name == str(rtr)]
        rtr_interface_flip = [
            interface for interface in interface_connection if interface.interface_b.device.name == str(rtr)]
        for interface in rtr_interface:
            if (interface.interface_a.device.name in routers_list) and (interface.interface_b.device.name in routers_list):
                entry = {'source': interface.interface_a.device.name,
                         'target': interface.interface_b.device.name,
                         'local_ip': interface.interface_a.name,
                         'remote_ip': interface.interface_b.name}
                network_map.insert(0, entry)
        for interface in rtr_interface_flip:
            if (interface.interface_a.device.name in routers_list) and (interface.interface_b.device.name in routers_list):
                entry = {'source': interface.interface_b.device.name,
                         'target': interface.interface_a.device.name,
                         'local_ip': interface.interface_b.name,
                         'remote_ip': interface.interface_a.name}
                network_map.insert(0, entry)
    logger.info('done with router connections')
    logger.info('get all circuits info')
    circuits = nb.circuits.circuit_terminations.all()
    logger.info('filter connected circuits')
    circuits_connected = [
        circ for circ in circuits if circ.connected_endpoint]
    parse_circuits = []
    entry = {}
    for circ in circuits_connected:
        if str(circ) in parse_circuits:
            entry[str(circ)].update(
                {'target': circ.connected_endpoint.device.name, 'remote_ip': circ.connected_endpoint.name})
        else:
            entry[str(circ)] = {'source': circ.connected_endpoint.device.name,
                                'local_ip': circ.connected_endpoint.name}
            parse_circuits.insert(0, str(circ))
    connected_circuits = [key for key in entry if (
        'target' in entry[key].keys())]
    logger.info('filter connected circuits between routers only')

    for n in connected_circuits:
        if entry[n]['source'] and entry[n]['target'] in routers_list:
            reverse_entry = {'source': entry[n]['target'],
                             'local_ip': entry[n]['remote_ip'],
                             'target': entry[n]['source'],
                             'remote_ip': entry[n]['local_ip']}
            #print(reverse_entry)
            network_map.insert(0, entry[n])
            network_map.insert(0, reverse_entry)
    df = pd.DataFrame.from_records(network_map)
    logger.info('Fill NA values with 0')
    df = df.fillna(0)
    return df

if __name__ == '__main__':
    try:
        df = get_netbox_connections('c93e6fc5f72646641c9ca52c7e849ca2feaf9b3b','http://X.X.X.X/')
        #dummy metric
        df['metric'] = 10
        #dummy capacity
        df['capacity'] = 10000
        #below is used later in the group to assign correct local/remote_ip
        df.loc[:, 'l_ip_r_ip'] = pd.Series([tuple(sorted(each)) for each in list(
            zip(df.local_ip.values.tolist(), df.remote_ip.values.tolist()))])
        df.loc[:, 'rtr_pair'] = pd.Series([tuple(sorted(each)) for each in list(
            zip(df.source.values.tolist(), df.target.values.tolist()))])
        #group by rtr_pair and local_remote_ip
        grouped = df.groupby(['rtr_pair','l_ip_r_ip'])
        grouped_dict = grouped.apply(lambda x: x.to_dict(orient='records')).to_dict()
        links_placeholder = []
        for entry in grouped_dict:
            subnet = random.sample(range(0,210),3)
            ip1 = '{}.{}.{}.{}'.format(*subnet+[1])
            ip2 = '{}.{}.{}.{}'.format(*subnet+[2])
            for number, links in enumerate(grouped_dict[entry]):
                if number == 0:
                    links['local_ip'] = ip1
                    links['remote_ip'] = ip2
                else:
                    links['local_ip'] = ip2
                    links['remote_ip'] = ip1
                links_placeholder.append(links)
        network_map = {}
        network_map['links'] = links_placeholder
        network_map['nodes'] = [{}]
        path = "lnetd_qt_netbox_topo.json"
        with open(path, "w") as file:
            json.dump(network_map, file, sort_keys=True, indent=4)
    except Exception as e:
        print(e)
