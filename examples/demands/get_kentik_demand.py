
import requests
import json
import pandas as pd
from sqlalchemy import create_engine, text
import sqlite3


def map_ip_to_name(routers_dict, ip):
    try:
        ip = ip.split("/")[0]
        rtr_name = routers_dict[ip]
        return rtr_name
    except Exception as e:
        return "None"

def get_device_names():
    try:
        disk_engine = create_engine('sqlite:////opt/lnetd/web_app/database.db')
        sql_qry = "select name,ip from Routers"
        routers = pd.read_sql("SELECT name,ip FROM Routers ", disk_engine)
        routers_dict = dict(zip(routers['ip'], routers['name']))
        # router_name = disk_engine.execute(text(sql_qry).execution_options(autocommit=True))
        # router = router_name.fetchall()
        if not routers_dict:
            return [{}]
        else:
            return routers_dict
    except:
        return [{}]

def get_kentik_data():
    """Get Kentik Average bps from source bgp_next_hop to destination bgp_next_hop
    select only values with 1Gbps or more , see below
    "avg_bits_per_sec":1000000000
    """

    headers = {
        'X-CH-Auth-Email': '<email_address>',
        'X-CH-Auth-API-Token': '<api_token>',
        'Content-Type': 'application/json',
    }
    data ='{"queries":[{"bucket":"Flow","query":{"all_devices":true,"aggregateTypes":["avg_bits_per_sec"],"aggregateThresholds":{"avg_bits_per_sec":1000000000,"p95th_bits_per_sec":0,"max_bits_per_sec":0,"p99th_in_bits_per_sec":0,"p99th_bits_per_sec":1000000000},"bracketOptions":"","cidr":32,"cidr6":128,"customAsGroups":false,"cutFn":{},"cutFnRegex":{},"cutFnSelector":{},"depth":350,"descriptor":"","device_name":[],"device_labels":[],"device_sites":[],"device_types":[],"fastData":"Full","filterDimensionsEnabled":false,"filterDimensionName":"Total","filterDimensionOther":false,"filterDimensions":{"connector":"All","filterGroups":[]},"hostname_lookup":false,"isOverlay":false,"lookback_seconds":86400,"from_to_lookback":3600,"generatorDimensions":[],"generatorPanelMinHeight":250,"generatorMode":false,"generatorColumns":1,"generatorQueryTitle":"{{generator_series_name}}","generatorTopx":8,"matrixBy":[],"metric":["bytes"],"mirror":false,"mirrorUnits":true,"outsort":"avg_bits_per_sec","overlay_timestamp_adjust":false,"query_title":"","secondaryOutsort":"","secondaryTopxSeparate":false,"secondaryTopxMirrored":false,"show_total_overlay":true,"starting_time":null,"ending_time":null,"sync_all_axes":false,"sync_extents":true,"show_site_markers":false,"topx":40,"update_frequency":0,"use_log_axis":false,"use_secondary_log_axis":false,"aggregates":[{"value":"avg_bits_per_sec","column":"f_sum_both_bytes","fn":"average","label":"Bits/s Sampled at Ingress + Egress Average","unit":"bytes","group":"Bits/s Sampled at Ingress + Egress","origLabel":"Average","sample_rate":1,"raw":true,"name":"avg_bits_per_sec"}],"filters_obj":{"connector":"Any","filterGroups":[]},"dimension":["src_nexthop_ip","dst_nexthop_ip"]}}]}'

    response = requests.post('https://api.kentik.com/api/v5/query/topxdata', headers=headers, data=data)

    values = response.json()
    try:
        work_level = values['results'][0]['data']
        return work_level
    except:
        print(f'No Data from kentik, here is the request result {response.content}')
        return [{}]

work_level = get_kentik_data()
routers_dict = get_device_names()
#example for the router dict , if lnetd-web not available fill this manualy
#routers_dict = {'1.1.1.1': 'rtr_a', '2.2.2.2': 'rtr_b'}

if len(work_level) >1:
    df_netflow = pd.DataFrame(work_level)

    #drop key and timeseries
    df_netflow.drop(['timeSeries','key'], axis=1,inplace=True)

    #find router source name
    df_netflow['source'] = df_netflow.apply(
                lambda row: map_ip_to_name(routers_dict, row['inet_src_next_hop']), axis=1)
    #find router source name
    df_netflow['target'] = df_netflow.apply(
                lambda row: map_ip_to_name(routers_dict, row['inet_dst_next_hop']), axis=1)

    #drop if target/source router is -1
    df_netflow = df_netflow[df_netflow['target'].str.contains(
                "None") == False]
    df_netflow = df_netflow[df_netflow['source'].str.contains(
                "None") == False]

    #convert to mbps
    df_netflow['value'] = df_netflow.apply(
                lambda row: row['avg_bits_per_sec']/1000000 ,axis=1
        )
    #drop if source == target , ie local demand
    df_netflow = df_netflow[df_netflow.source != df_netflow.target]

    df_demand = df_netflow[['source','target','value']]
    json_output = {}
    json_output['demands'] = df_demand.to_dict(orient='records')
    #write demands to json file , this will be used to load demands into lnetd-qt
    with open('kentik_netflow_demands.json', 'w') as fp:
        json.dump(json_output, fp)
