def column(matrix, i):
    return [row[i] for row in matrix]
def time_zone(dt,diff):
    from datetime import datetime, timedelta
    date = dt + timedelta(hours=diff)
    return date.strftime("%Y.%m.%d %H:%M:%S")
def footer():
    from handler import datetime
    now = datetime()
    current_time = time_zone(now,-8)
    print(current_time)
    print("---------------------")
def transfer_trades(magic,orders,prev_orders,diff,status,new_trades,mt5):
    #print(orders)
    
    if status != "full close" and status != "full close permanent":
        index = 0
        #order opened
        if status != "other symbol full close":
            prev_orders_tickets = column(prev_orders,0)
            for order in orders:
                index+=1
                if order[0] not in prev_orders_tickets:
                    print("TRANSFER: ORDER OPEN DETECTED")
                    footer()
                    lst = order
                    volume = order[3]
                    lst = [order[0],order[1],order[2],volume,order[4],order[5],order[6],"open"]
                    new_trades.append(lst)
        #Order closed
        orders_tickets = column(orders,0)
        for order in prev_orders:
            if order[0] not in orders_tickets:
                print("TRANSFER: ORDER CLOSE DETECTED")
                footer()
                lst = order
                lst = [order[0],order[1],order[2],order[3],order[4],order[5],order[6],"close"]
                lst.append("close")
                new_trades.append(lst)
    return new_trades
