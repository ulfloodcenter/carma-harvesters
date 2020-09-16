import sqlite3


def get_huc12_mean_annual_flow(huc12_flowline_db):
    flowline_conn = sqlite3.connect(huc12_flowline_db)
    flowline = flowline_conn.cursor()

    query = 'select max(qe_ma) from nhdflowline_network'
    flowline.execute(query)
    r = flowline.fetchone()
    if r is None:
        return None
    return r[0]

def get_huc12_max_stream_order(huc12_flowline_db):
    flowline_conn = sqlite3.connect(huc12_flowline_db)
    flowline = flowline_conn.cursor()

    query = 'select max(streamorde) from nhdflowline_network'
    flowline.execute(query)
    r = flowline.fetchone()
    if r is None:
        return None
    return r[0]
