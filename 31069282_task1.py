"""
Program calculate stock and total revenue for one specific year.
Input is from txt file and output to another txt file.
Program checking year - is it leap or not, depends on it calculations are different.
Initial data - start year, stock, total revenue.

Author - Pavel Zemnukhov
Date the script was created - 25/04/2020
Date the last edit was made - 01/05/2020
"""
import math

def read_data():
    """
    read data from file AU_INV_START.txt
    store in variable start_dict which is a dictionary data type
    """
    start_year = open('AU_INV_START.txt', 'r')
    lines = start_year.readlines()
    start_year.close()
    dict_values = []
    for line in lines:
        dict_values.append(int(line))

    dict_keys = ['start_year', 'start_stock', 'start_revenue']
    start_dict = dict(zip(dict_keys, dict_values))
    return start_dict

start_dict = read_data()   #assigning function read_data() return to a variable

def cal_stock_revenue(start_dict):
    """
    Calculations of stock and revenue for one year

    :param start_dict: initial data in form of dictionary from AU_INV_START.txt
    :return: end_dict: dictionary with final results
    """
    # extracting data from library
    year = start_dict['start_year']  #year
    stock = start_dict['start_stock'] #stock at the begining of the year
    total_revenue = start_dict['start_revenue'] #total revenue at the begining for the year

    #declaring required variables
    restoking = 600                     #restoking qty, required for stock calculation
    stock_minimum = 400                 #stock minimum for restocking
    per1_dist = 36                      #distribution for first period
    per1_rrp = 705                      #RRP for first period
    deffect_price = 0.8                 #percentage for deffect products price
    deffect_percentage = 0.05           #percentage for deffect products qty
    normal_to_peak_percent_dist = 35    #increase percent for peak season distribution
    normal_to_peak_percent_rrp = 20     #increase percent for peak season RRP
    new_finacial_year_dist = 10         #increase percent for new fin. year distribution
    new_finacial_year_rrp = 5           #increase percent for new fin. year RRP
    jan_days = 31                       #number of days in january
    jan_dist = jan_days * per1_dist     #calculation of January distribution
    rev_jan = jan_dist * per1_rrp       #calculation of January revenue

    def stock_calc(month, period):
        """Calculate stock for specific month and distribution period.
            return: stock"""
        nonlocal stock              #declaring free variable
        for i in range(month):
            stock = stock - period
            if stock <= stock_minimum:
                # restocking, if stock goes below stock minimum
                stock += restoking
        return stock

    stock_calc(jan_days, per1_dist)                  #calculating stock for January
    deffects_jan = jan_dist * deffect_percentage     #calculating deffects items for January
    stock += deffects_jan                            #updating stock at the end of the month, adding deffects
    total_revenue += rev_jan                         #updating total_revenue

    # checking february for leap year
    # source https://en.wikipedia.org/wiki/Leap_year
    if year % 4 != 0:
        feb_days = 28
    elif year % 100 != 0:
        feb_days = 29
    elif year % 400 != 0:
        feb_days = 28
    else:
        feb_days = 29

    stock_calc(feb_days, per1_dist)                                 #February stock before adding deffects
    feb_dist = feb_days * per1_dist                                 #February distribution
    feb_rev_normal = (feb_dist - deffects_jan) * per1_rrp           #February revenue new products
    feb_rev_discount = deffects_jan * per1_rrp * deffect_price      #February revenue deffect products
    feb_rev = feb_rev_discount + feb_rev_normal                     #February revenue total
    deffects_feb = (feb_dist - deffects_jan) * deffect_percentage   #February deffect products
    stock = stock + deffects_feb                                    #adding deffect to the stock
    total_revenue += feb_rev

    # period 2 from 1st of March till 30th of June, normal period
    period2_rrp = (per1_rrp / ((normal_to_peak_percent_rrp + 100) / 100))  #calculation rrp for period 2
    period2_dist = per1_dist / ((normal_to_peak_percent_dist + 100) / 100) #calculation distribution for period 2

    # calculations of other months are similar to January and February
    march_days = 31      #number of days in March
    stock = stock_calc(march_days, period2_dist)
    march_dist = march_days * period2_dist
    march_rev_normal = (march_dist - deffects_feb) * period2_rrp
    # March revenue deffect products, calculated based on previous period product RRP, when it was returned
    march_rev_discount = deffects_feb * per1_rrp * deffect_price
    march_rev_total = march_rev_discount + march_rev_normal
    deffects_march = (march_dist - deffects_feb) * deffect_percentage
    stock += deffects_march
    total_revenue += march_rev_total

    april_days = 30  #number of days in April
    stock = stock_calc(april_days, period2_dist)
    april_dist = april_days * period2_dist
    april_rev_normal = (april_dist - deffects_march) * period2_rrp
    # April revenue deffect products, calculated based on current period product RRP
    # products were returned in March, which is current period
    april_rev_discount = deffects_march * period2_rrp * deffect_price
    april_rev_total = april_rev_discount + april_rev_normal
    deffects_april = (april_dist - deffects_march) * deffect_percentage
    stock += deffects_april
    total_revenue += april_rev_total

    may_days = 31 #number of days in May
    stock = stock_calc(may_days, period2_dist)
    may_dist = may_days * period2_dist
    may_rev_normal = (may_dist - deffects_april) * period2_rrp
    may_rev_discount = deffects_april * period2_rrp * deffect_price
    may_rev_total = may_rev_discount + may_rev_normal
    deffects_may = (may_dist - deffects_april) * deffect_percentage
    stock += deffects_may
    total_revenue += may_rev_total

    june_days = 30 #number of days in June
    stock = stock_calc(june_days, period2_dist)
    june_dist = june_days * period2_dist
    june_rev_normal = (june_dist - deffects_may) * period2_rrp
    june_rev_discount = deffects_may * period2_rrp * deffect_price
    june_rev_total = june_rev_discount + june_rev_normal
    deffects_june = (june_dist - deffects_may) * deffect_percentage
    stock += deffects_june
    total_revenue += june_rev_total

    # period 3, new financial year starts, July 1st - October 31(end of normal season)
    period3_rrp = (period2_rrp + period2_rrp * (new_finacial_year_rrp / 100))       #calculating period3 rrp
    period3_dist = period2_dist + period2_dist * (new_finacial_year_dist / 100)     #calculating period3 distribution

    july_days = 31 #number of days in July
    stock = stock_calc(july_days, period3_dist)
    july_dist = july_days * period3_dist
    july_rev_normal = (july_dist - deffects_june) * period3_rrp
    # July revenue deffect products, calculated based on previous period product RRP, when it was returned
    july_rev_discount = deffects_june * period2_rrp * deffect_price
    july_rev_total = july_rev_discount + july_rev_normal
    deffects_july = (july_dist - deffects_june) * deffect_percentage
    stock += deffects_july
    total_revenue += july_rev_total

    august_days = 31 #number of days in August
    stock = stock_calc(august_days, period3_dist)
    august_dist = august_days * period3_dist
    august_rev_normal = (august_dist - deffects_july) * period3_rrp
    # August revenue deffect products, calculated based on current period product RRP
    # products were returned in July, which is current period
    august_rev_discount = deffects_july * period3_rrp * deffect_price
    august_rev_total = august_rev_discount + august_rev_normal
    deffects_august = (august_dist - deffects_july) * deffect_percentage
    stock += deffects_august
    total_revenue += august_rev_total

    september_days = 30 #number of days in September
    stock = stock_calc(september_days, period3_dist)
    september_dist = september_days * period3_dist
    september_rev_normal = (september_dist - deffects_august) * period3_rrp
    september_rev_discount = deffects_august * period3_rrp * deffect_price
    september_rev_total = september_rev_discount + september_rev_normal
    deffects_september = (september_dist - deffects_august) * deffect_percentage
    stock += deffects_september
    total_revenue += september_rev_total

    october_days = 31 #number of days in October
    stock = stock_calc(october_days, period3_dist)
    october_dist = october_days * period3_dist
    october_rev_normal = (october_dist - deffects_september) * period3_rrp
    october_rev_discount = deffects_september * period3_rrp * deffect_price
    october_rev_total = october_rev_discount + october_rev_normal
    deffects_october = (october_dist - deffects_september) * deffect_percentage
    stock += deffects_october
    total_revenue += october_rev_total

    # period 4, beginning of peak season, Nov 1st - Dec 31
    period4_rrp = (period3_rrp + period3_rrp * (normal_to_peak_percent_rrp / 100))   #calculating period4 rrp
    period4_dist = period3_dist + period3_dist * (normal_to_peak_percent_dist / 100) #calculating period4 distribution
    november_days = 30
    stock = stock_calc(november_days, period4_dist)
    november_dist = november_days * period4_dist
    november_rev_normal = (november_dist - deffects_october) * period4_rrp
    # November revenue deffect products, calculated based on previous period product RRP, when it was returned
    november_rev_discount = deffects_october * period3_rrp * deffect_price
    november_rev_total = november_rev_discount + november_rev_normal
    deffects_november = (november_dist - deffects_october) * deffect_percentage
    stock += deffects_november
    total_revenue += november_rev_total

    december_days = 30 #number of days in December
    stock = stock_calc(december_days, period4_dist)
    december_dist = december_days * period4_dist
    december_rev_normal = (december_dist - deffects_november) * period4_rrp
    # December revenue deffect products, calculated based on current period product RRP
    # products were returned in November, which is current period
    december_rev_discount = deffects_november * period4_rrp * deffect_price
    december_rev_total = december_rev_discount + december_rev_normal
    deffects_december = (december_dist - deffects_november) * deffect_percentage

    stock += deffects_december              #total stock for the whole year
    total_revenue += december_rev_total     #total revenue for the whole year
    year += 1                               #year increment

    end_dict = {}        #creating dictionary for final outpur
    end_dict['end_year'] = year
    end_dict['end_stock'] = math.ceil(stock)
    end_dict['end_revenue'] = round(total_revenue,2)
    return end_dict

end_dict = cal_stock_revenue(start_dict)  #assigning function return to a variable


def write_data(end_dict):
    """
    Function write values from dictionary end_dict to file AU_INV_END.txt
    """
    end_year = open("AU_INV_END.txt", "w")
    end_year.write(str(end_dict['end_year']))
    end_year.write("\n")
    end_year.write(str(end_dict['end_stock']))
    end_year.write("\n")
    end_year.write(str(end_dict['end_revenue']))
    end_year.close()

write_data(end_dict)
