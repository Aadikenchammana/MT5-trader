#---------------------------------
# F U N C T I O N S
#---------------------------------
def filter_orders_magic(magic,mt5):
            output = []
            orders=mt5.positions_get(magic=magic)
            #orders=mt5.positions_get()
            for order in orders:
                if int(order[6]) == magic:
                    output.append(order)
            orders = output
            output = []
            for order in orders:
                ticket = order[0]
                price = order[10]
                position = order[5]#0 if buy and 1 if sell
                if position ==0:
                    position = "buy"
                elif position == 1:
                    position = "sell"
                volume = order[9]
                symbol = order[16]
                profit = order[15]
                trade_magic =  order[6]
                output.append([ticket,price,position,volume,symbol,trade_magic,profit])
            return output
def message(key, message,typ):
    import json
    if typ.upper() == "READ":
        with open('messages.txt', 'r') as f:
            dct = json.loads(f.read())
        if key in dct.keys():
            return dct[key]
        else:
            return "bad key"
    elif typ.upper() == "SEND":
        with open('messages.txt', 'r') as f:
            dct = json.loads(f.read())
        dct[key] = message
        with open('messages.txt', 'w') as f:
            json.dump(dct, f)
        return "sent"
    return "error"
def calculate_spread_magic(magic,mt5,hi=False):
    orders = filter_orders_magic(magic,mt5)
    spread = 0
    for order in orders:
        profit = order[6]
        spread-= profit
    return spread
def calculate_spread_magic1(magic,mt5,hi=False):
    return calculate_spread_magic(magic,mt5)
def time_zone(dt,diff):
    from datetime import datetime, timedelta
    date = dt + timedelta(hours=diff)
    return date.strftime("%Y.%m.%d %H:%M:%S")
def footer():
    from datetime import datetime
    now = datetime.now()
    current_time = time_zone(now,-8)
    print(current_time)
    print("---------------------")
def calc_balance(switch,symbol,mt5,around=False):
    from datetime import datetime
    from_date=datetime(2020,11,17)
    to_date=datetime(2024,12,30)
    orders=mt5.history_deals_get(from_date, to_date)
    venus_orders = []
    server_orders = []
    obscure_orders = []
    for order in orders:
        if int(order[5]) == 1 and order[15] == symbol or around:
            if order[9] != 0.01:
                server_orders.append(order)
            elif int(order[6]) == 100:
                venus_orders.append(order)
            else:
                obscure_orders.append(order)
    if switch == "server":
        orders = server_orders
    elif switch == "client":
        orders = venus_orders
    elif switch == "obscure":
        orders = obscure_orders
    elif switch == "total":
        orders = obscure_orders+venus_orders+server_orders
    total_profit = 0
    for order in orders:
        profit = order[13]
        total_profit+=profit
    return total_profit
def calc_vc(vc,values,symbol,magic,orders,diff,mt5):
    """
    assume = 1.5
    prev_server_balance = values["server_balance"]
    prev_server_equity = values["server_equity"]
    server_balance = calc_balance("server",symbol,mt5)
    
    spread = prev_server_balance - server_balance 
    """
    volume_coefficient = diff*10/len(orders)
    print("RESTART:",volume_coefficient)
    return volume_coefficient
    
#---------------------------------
# M A I N 
#---------------------------------
def restart(magic,replace_magic,symbol,orders,prev_orders,status,new_trades,values,volume_coefficient,diff,mt5):
    spread = calculate_spread_magic1(magic,mt5)
    #---------------------------------
    # R E S T A R T
    #---------------------------------
    allow_flag = message("allow_restart", "","READ")
    if len(prev_orders) >4:
        net = len(prev_orders)/10
        new_diff = -1*(len(prev_orders)/2-net)
    else:
        new_diff = -2
    if status == "full close" and spread < new_diff and True:
        print("RESTART: RESTART DETECTED")
        volume_coefficient  = calc_vc(volume_coefficient,values,symbol,replace_magic,orders,diff,mt5)
        for order in orders:
            lst = order
            if len(lst) >= 8:
                lst[7] = "restart"
            else:
                lst.append("restart")
            new_trades.append(lst)
        status = "restart"
        print("RESTART: RESTART COMPLETED")
        footer()

    #---------------------------------
    # R E S T A R T   O N   C O M M A N D
    #---------------------------------
    flag = message("restart_flag", "","READ")
    if flag.upper() == "TRUE":
        message("restart_flag","FALSE","SEND")
        print("RESTART: RESTART DETECTED ON COMMAND")
        volume_coefficient  = calc_vc(volume_coefficient,values,symbol,replace_magic,mt5)
        for order in orders:
            lst = order
            if len(order) == 8:
                lst[7] = "restart"
            else:
                lst.append("restart")
            new_trades.append(lst)
        status = "restart"
        print("RESTART: RESTART COMPLETED ON COMMAND")
        footer()
    return new_trades, status, volume_coefficient
