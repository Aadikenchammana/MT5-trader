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

def calculate_spread_magic(magic,mt5,hi=False):
    orders = filter_orders_magic(magic,mt5)
    spread = 0
    for order in orders:
        profit = order[6]
        spread-= profit
    return spread, len(orders)
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
def store_values(symbol,magic,replace_magic,mt5,time,stored_values):
    if time == True:
        stored_values = {}
        spread,ln = calculate_spread_magic(replace_magic,mt5,True)
        balance = calc_balance("server",symbol,mt5)
        stored_values["server_equity"] = balance - spread
        stored_values["server_balance"] = balance
        stored_values["spread"] = spread
    return stored_values
#---------------------------------
# M A I N
#---------------------------------
def total_close(magic,volume_dict,ticket_dict,mt5):
    orders = filter_orders_magic(magic)
    new_trades = []
    for order in orders:
        for order in orders:
            lst = order
            if len(order) == 8:
                lst[7] = "full close"
            else:
                lst.append("full close")
            new_trades.append(lst)
    from send_orders import send_orders
    volume_dict,ticket_dict = send_orders(20,mt5,volume_dict,ticket_dict,1,1,new_trades)
    return volume_dict,ticket_dict
        


def full_close(magic,replace_magic,stored_values,symbol,orders,status,diff,new_trades,volume_coefficient,sc,max_orders,mt5):
    spread,ln = calculate_spread_magic(magic,mt5)
    stored_values = {}
    full_close_flag = False
    allow_flag = message("allow_full_close", "","READ")
    #---------------------------------
    # F U L L   C L O S E 
    #---------------------------------
    if status == "regular" and spread > diff and len(orders) >= 2 and allow_flag.upper()=="TRUE":
        full_close_flag = True
        print("FC: FULL CLOSE DETECTED")
        for order in orders:
            lst = order
            if len(order) == 8:
                lst[7] = "full close"
            else:
                lst.append("full close")
            new_trades.append(lst)
        status = "full close"
        stored_values = store_values(symbol,magic,replace_magic,mt5,True,stored_values)
        print("FC: FULL CLOSE COMPLETED")
        footer()
    #---------------------------------
    # F U L L   C L O S E   O N   R E S T A R T
    #---------------------------------
    if status == "restart" and spread > 0 and max_orders == len(orders) and allow_flag.upper()=="TRUE":
        full_close_flag = True
        print("FC: FULL CLOSE DETECTED ON RESTART")
        for order in orders:
            lst = order
            if len(order) == 8:
                lst[7] = "full close"
            else:
                lst.append("full close")
            new_trades.append(lst)
        status = "full close permanent"
        stored_values = store_values(symbol,magic,replace_magic,mt5,True,stored_values)
        print("FC: FULL CLOSE COMPLETED ON RESTART")
       
        footer()
    #---------------------------------
    # F U L L   C L O S E   O N   C O M M A N D
    #---------------------------------
    flag = message("full_close_flag", "","READ")
    if flag.upper() == "TRUE":
        message("full_close_flag","FALSE","SEND")
        full_close_flag = True
        print("FC: FULL CLOSE DETECTED ON COMMAND")
        for order in orders:
            lst = order
            if len(order) == 8:
                lst[7] = "full close"
            else:
                lst.append("full close")
            new_trades.append(lst)
        status = "full close"
        stored_values = store_values(symbol,magic,replace_magic,mt5,False,stored_values)
        print("FC: FULL CLOSE COMPLETED ON COMMAND")
        footer()
    return new_trades,status, stored_values,full_close_flag
