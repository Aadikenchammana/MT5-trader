def merging():   
    import json
    import datetime
    import math
    import matplotlib.pyplot as plt
    import os
    import time
    symbol = "EURUSD"
    with open('test_case//params', 'r') as f:
        params = json.loads(f.read())
    start_dt = params["start_date"]
    end_dt = params["end_date"]
    merged_prices = {}

    print("hi")
    def column(matrix, i):
        return [row[i] for row in matrix]
    def keys_to_list(dct):
        lst = []
        for key in dct.keys():
            lst.append(key)
        return lst
    def table_to_string(table,sep1,sep2):
            table_string = ""
            row_string = ""
            for row in table:
                row_string = ""
                for item in row:
                    if row_string == "":
                        row_string = str(item)
                    else:
                        row_string+=sep1+str(item)
                if table_string == "":
                    table_string = row_string
                else:
                    table_string += sep2+row_string
            return table_string
    def format_order(order):
        price = float(order[4])
        if "buy" in order:
            return {"buy":price,"sell":price-0.00008}
        elif "sell" in order:
            return {"buy":price+0.00008,"sell":price}

    with open("resources//"+symbol+'//prices.txt', 'r') as f:
        prices = json.loads(f.read())
    with open("resources//"+symbol+'//orders.txt', 'r') as f:
        unmerged_orders = json.loads(f.read())
    with open("resources//"+symbol+'//prices_vvs.txt', 'r') as f:
        vvs_prices = json.loads(f.read())
    keys = list(prices.keys())
    trunc_keys = []
    location = {}
    flag = True
    for key in keys:
        if start_dt < key < end_dt and flag == True: 
            trunc_keys.append(key)
            location[key] = "price"
        elif key > end_dt:
            flag = False
    unmerged_orders_dct = {}
    vvs_keys = list(vvs_prices.keys())
    flag = True
    for key in vvs_keys:
        if start_dt < key < end_dt and key not in trunc_keys and flag == True:
            trunc_keys.append(key)
            location[key] = "vvs"
        elif key > end_dt:
            flag = False
    order_keys = column(unmerged_orders,1)
    flag = True
    for item in unmerged_orders:
        unmerged_orders_dct[item[1]] = item
    for key in order_keys:
        if start_dt < key < end_dt and key not in trunc_keys and flag == True:
            trunc_keys.append(key)
            location[key] = "order"
        elif key > end_dt:
            flag = False
        
    trunc_keys.sort()
    keys = trunc_keys

    for key in keys:
        print(key)
        os.system('clear')
        if location[key] == "price":
            merged_prices[key] = {symbol:prices[key]}
        elif location[key] == "vvs":
            merged_prices[key] = {symbol:vvs_prices[key]}
        elif location[key] == "order":
            merged_prices[key] = {symbol:format_order(unmerged_orders_dct[key])}
    with open("merged//prices", 'w') as f:
        json.dump(merged_prices, f)


        
    print("STARTING")
    close_prices = {}
    keys = list(merged_prices.keys())
    with open("merged//dt", 'w') as f:
        json.dump(keys, f)
    with open('test_case//variables', 'r') as f:
        variables = json.loads(f.read())
    index = variables["index"]
    order_list = variables["order_list"]
    orders = {}
    close_prices = {}
    order_dict = {}
    for date_time in merged_prices.keys():
        while True:
            if index < len(unmerged_orders):
                item = unmerged_orders[index]
                dt = item[1]#[:-2]+":00"
                #-----------------------------------------
                #updating open orders
                #-----------------------------------------
                if date_time == dt or date_time > dt:
                    index += 1
                    if "close" in item:
                        for thing in order_list:
                            if symbol+item[len(item)-1] in thing:
                                thing[0] = symbol+thing[0]
                                order_list.remove(thing)
                                thing
                                close_prices[date_time] = {"close":item[4]}
                    elif "open" in item:
                        item[0] = symbol+str(item[0])
                        order_list.append(item)
                else:
                    break
            else:
                dt = unmerged_orders[index-1][1]#[:-2]+":00"
                #order_dict[date_time] = table_to_string(order_list,"/",",")
                break
            
        print(date_time,dt)
        order_dict[date_time] = table_to_string(order_list,"/",",")
        os.system('clear')
    variables["index"] = index
    variables["order_list"] = order_list
    with open("test_case//variables", 'w') as f:
            json.dump(variables, f)
    with open("merged//orders", 'w') as f:
        json.dump(order_dict, f)
    with open("merged//close_prices", 'w') as f:
        json.dump(close_prices, f)
    print("DONE")

"""
merging()
from handler import prep
prep()
for i in range(16):
    from handler import change
    change()
"""