#-------------------------------------
#F U N C T I O N S 
#-------------------------------------
def calc_profit(symbol,position,price,volume,current_prices):
    current_price = current_prices[symbol]
    if position == 1:
        #BUY
        return volume*100000*(float(current_price["sell"]) - price)
    elif position == 0:
        #SELL
        return volume*100000*(price - float(current_price["buy"]))
def format_order(order,current_prices):
    
    lst = []
    ticket = order[0]
    if order[2] == "buy":
        position = 1
    else:
        position = 0
    price = float(order[4])
    volume = float(order[3])
    symbol = ticket[:6]
    profit = calc_profit(symbol,position,price,volume,current_prices)
    if symbol == "EURUSD":
        magic = 100
    elif symbol == "USDCHF":
        magic = 200
    lst = [ticket,1,2,3,4,position,magic,7,8,volume,price,11,12,13,14,profit,symbol]
    return lst
def format_orders(orders,current_prices):
    lst = []
    for order in orders:
        if order != ['']:
            lst.append(format_order(order,current_prices))
    return lst

def format_request(request,new_ticket,variables):
    import json
    client_orders = variables["client_orders"]
    lst = []
    ticket = new_ticket
    position = request["type"]
    if position == "buy":
        position = 1
    elif position == "sell":
        position = 0
   # price = float(request["price"])
    magic = int(request["magic"])
    volume = float(request["volume"])
    profit = 0
    symbol = request["symbol"]  
    ticket_dict = variables["ticket_dict"]
    client_ticket = ticket_dict[ticket]
    #print(client_ticket,client_orders)
    if request["restart"] == False:
        for order in client_orders:
            if order[0] == client_ticket:
                price = order[10]
    else:
        price = float(request["price"])
    lst = [ticket,1,2,3,4,position,magic,7,8,volume,price,11,12,13,14,profit,symbol]
    return lst
def calc_balance(order,server_balance):
    import json
    with open("operations//variables", 'r') as f:
        variables = json.loads(f.read())
    with open("merged//close_prices", 'r') as f:
            close_prices = json.loads(f.read())
    dt = variables["dt"]
    prices = variables["current_prices"]
    if order[5] == 1:
        if dt in close_prices.keys():
            close_price = float(close_prices[dt]["close"])
        else:
            """
            #print(dt)
            quit()
            """
            close_price = float(prices[order[16]]["sell"])
        total =  float(order[9])*100000*(close_price - float(order[10]))
    elif order[5] == 0:
        if dt in close_prices.keys():
            close_price = float(close_prices[dt]["close"])
        else:
            """
            #print(dt)
            quit()
            """
            close_price = float(prices[order[16]]["buy"])
        total = float(order[9])*100000*(float(order[10]) - close_price)
    
    else:
        print("errororororo")
    
    #print("thing",close_price,order[10])
    #print(order)
    server_balance = server_balance-total
    #print("server_balance",total)
    #quit()
    return server_balance
def string_to_table (string,sep1,sep2):
    string = string.split(sep2)
    for i in range(len(string)):
        string[i] = string[i].split(sep1)
    return string
def dict_string_to_table(dct,sep1,sep2):
    output = {}
    for key in dct.keys():
        item = dct[key]
        output[key] = string_to_table(item,sep1,sep2)
    return output
def column(i,lst):
    output = []
    for item in lst:
        output.append(item[i])
    return output
def calc_client_balance(orders,prev_orders,client_balance,dt,current_prices):
    import json
    with open("merged//close_prices", 'r') as f:
            close_prices = json.loads(f.read())
    total_profit = 0
    ticket_list = column(0,orders)
    for order in prev_orders:
        if order[0] not in ticket_list:
            #print("ORDER CLOSED:")
            #print(order)
            #print("-----------------------------------------")
            if order[5] == 1:
                close_price = float(close_prices[dt]["close"])
                profit =  float(order[9])*100000*(close_price - float(order[10]))
            elif order[5] == 0:
                close_price = float(close_prices[dt]["close"])
                profit =  float(order[9])*100000*(float(order[10]) - close_price)
            total_profit += profit
    client_balance = total_profit+client_balance
    return client_balance
def calc_equity(typ,current_prices,server_balance,client_balance,server_orders,client_orders):
    total_profit = 0
    if typ == "server":
        orders = server_orders
        balance = server_balance
    else:
        orders = client_orders
        balance = client_balance
    for order in orders:
        profit = float(order[15])
        total_profit += profit
    if typ == "server":
        server_equity = balance + total_profit
        return server_equity
    else:
        client_equity =  balance + total_profit
        return client_equity
def format_server_orders(orders):
    import json
    with open("operations//variables", 'r') as f:
        variables = json.loads(f.read())
    current_prices = variables["current_prices"]
    lst = []
    for order in orders:
        symbol = str(order[16])
        prices = current_prices[symbol]
        temp = order
        if order[5] == 1:
            price = float(prices["sell"])
            profit = float(order[9])*(float(order[10])-price)*100000
        elif order[5] == 0:
            price = float(prices["buy"])
            profit = float(order[9])*(price - float(order[10]))*100000
        temp[15] = profit
        lst.append(temp)
    return lst


def metatrader():
    class mt5:
        import json
        #-------------------------------------------------
        #  C R E A T I N G   M T 5 
        #----------------------------------------------
        # A C C E S S I N G   V A R I A B L E S
        with open("operations//variables", 'r') as f:
            variables = json.loads(f.read())
        with open("merged//close_prices", 'r') as f:
            close_prices = json.loads(f.read())
        dt = variables["dt"]
        client_orders = variables["client_orders"]
        orders = variables["orders"]
        current_prices = variables["current_prices"]
        server_orders = variables["server_orders"]
        prev_server_orders = server_orders
        prev_client_orders = variables["prev_client_orders"]
        server_balance = variables["server_balance"]
        client_balance = variables["client_balance"]
        client_balance = calc_client_balance(client_orders,prev_client_orders,client_balance,dt,current_prices)
        variables["client_balance"] = client_balance
        server_ticket = variables["server_ticket"]
        with open("operations//variables", 'w') as f:
            json.dump(variables, f)
        # O R D E R   V I E W I N G
        def positions_get(magic=None,symbol=None):
            lst = []
            import json
            with open("operations//variables", 'r') as f:
                variables = json.loads(f.read())
            total_orders = variables["orders"]
            if magic != None:
                for order in total_orders:
                    if order[6] == magic:
                        lst.append(order)
            elif symbol != None:
                for order in total_orders:
                    if order[16] == symbol:
                        lst.append(order)
            else:
                lst = total_orders
            return lst

        # O R D E R   E D I T I N G
        ORDER_TYPE_BUY = "buy"
        ORDER_TYPE_SELL = "sell"
        TRADE_ACTION_DEAL = "wtv"
        ORDER_TIME_GTC = "wtv"
        ORDER_FILLING_IOC = "wtv"
        def order_send(request):
            print("ORDER SEND", request)
            print("----")
            import json
            with open("operations//variables", 'r') as f:
                variables = json.loads(f.read())
            server_orders = variables["server_orders"]
            if "position" in request.keys():
                #close
                #print("close")
                remove_order = "nvm"
                for order in server_orders:
                    if order[0] == request["position"]:
                        remove_order = order
                if remove_order != "nvm":
                    server_orders.remove(remove_order)
                    server_balance = variables["server_balance"]
                    server_balance = calc_balance(remove_order,server_balance)
                    variables["server_balance"] = server_balance
                else:
                    print("HANDLER: ORDER",request["position"],"NOT FOUND")
            else:
                ticket_dict = variables["ticket_dict"] 
                server_ticket = variables["server_ticket"]
                server_ticket += 1
                variables["server_ticket"] = server_ticket
                new_ticket = int("9907"+str(server_ticket))
                ticket_dict[new_ticket] = request["ticket"]
                variables["ticket_dict"] = ticket_dict
                #open
                server_orders.append(format_request(request,new_ticket,variables))
                #print("formated order",format_request(request,new_ticket,variables))
                #print("SERVER ORDERS")
                #print(server_orders)
                variables["server_orders"] = server_orders
            with open("operations//variables", 'w') as f:
                json.dump(variables, f)
            if "position" in request.keys():
                return 10009
            else:
                return new_ticket,10009

        def history_deals_get(from_date,to_date):
            import json
            with open("operations//variables", 'r') as f:
                variables = json.loads(f.read())
            server_balance = variables["server_balance"]
            client_balance = variables["client_balance"]
            server_order = [0,1,2,3,4,1,6,7,8,9,10,11,12,server_balance,14,"EURUSD"]
            client_order = [0,1,2,3,4,1,100,7,8,0.01,10,11,12,server_balance,14,"EURUSD"]
            return [client_order,server_order]
        # B A L A N C E   E Q U I T Y
        class account_info():
            def _asdict(filler):
                import json
                with open("operations//variables", 'r') as f:
                    variables = json.loads(f.read())
                server_balance = variables["server_balance"]
                server_equity = variables["server_equity"]
                client_balance = variables["client_equity"]
                client_equity = variables["server_balance"]
                equity = server_equity+client_equity- 1000
                dct = {"balance": server_balance+client_balance - 1000, "equity": equity,"leverage":500}
                return dct

        # S Y M B O L   I N F O
        def symbol_info_tick(symbol):
            class hello:
                import json
                with open("operations//variables", 'r') as f:
                    variables = json.loads(f.read())
                current_prices = variables["current_prices"]
                prices = current_prices[symbol]
                ask = float(prices["sell"])
                bid = float(prices["buy"])
                point = 1
            return hello
        def symbol_info(symbol):
            class hello:
                import json
                with open("operations//variables", 'r') as f:
                    variables = json.loads(f.read())
                current_prices = variables["current_prices"]
                prices = current_prices[symbol]
                ask = prices["sell"]
                bid = prices["buy"]
                point = 1
            return hello
        # U P L O A D I N G   V A R I A B L E S
        with open("operations//variables", 'r') as f:
            variables = json.loads(f.read())
        server_orders = variables["server_orders"]
        server_orders = format_server_orders(server_orders)
        variables["server_orders"] = server_orders
        client_orders = variables["client_orders"]
        server_balance = variables["server_balance"]
        client_balance = variables["client_balance"]
        server_equity = calc_equity("server",current_prices,server_balance,client_balance,server_orders,client_orders)
        client_equity = calc_equity("client",current_prices,server_balance,client_balance,server_orders,client_orders)
        variables["client_equity"] = client_equity
        variables["server_equity"] = server_equity
        variables["client_balance"] = client_balance
        variables["server_balance"] = server_balance
        with open("operations//variables", 'w') as f:
            json.dump(variables, f)
    return mt5




#-------------------------------------------------------
# E N D   O F   C R E A T I N G   M T 5
#-------------------------------------------------------