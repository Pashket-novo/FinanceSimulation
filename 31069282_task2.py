"""
Program do simulation over years.
Input is from txt file and output to another txt file.
For each year, program calculate stock and total revenue, as well as RRP and distribution rate.
Crisis is taking into consideration, it frequency could be changed.
Program checking year - is it leap or not, depends on it calculations are different.
Initial data - start year, stock, total revenue.
Program calculating stock and revenue based on calculations from foundation year.

Author - Pavel Zemnukhov
Date the script was created - 29/04/2020
Date the last edit was made - 01/05/2020
"""
import math     #importing math library, required for final rounding

#defining constant variables referencing to assignment requirements
NO_YEAR_SIM = 3
PER_DEF = 5
CRIS_RECUR_FREQUENCY = 9


def read_data():
    """
    read data from file AU_INV_START.txt
    store in variable start_dict, which is a dictionary data type
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


start_dict = read_data()        #assigning function read_data() return to a variable


def cal_stock_revenue(start_dict):
    """
    Calculations of stock and revenue over the years

    :param start_dict: initial data in form of dictionary from AU_INV_START.txt
    :return: end_dict: dictionary with final results
    """

    #extracting data from library
    year = str(start_dict['start_year'])
    stock = start_dict['start_stock']
    total_revenue = start_dict['start_revenue']

    company_found_year = 2000      #defining a company foundation year
    company_found_stock = 1000     #defining a company foundation stock
    company_found_rev = 0          #defining a company foundation revenue
    company_found_dist = 36        #defining a company foundation distribution qty per day
    company_found_rrp = 705        #defining a company foundation RRP for product

    year_sim_start = int(year[0:4])                 #defining the year, starting point for our simulation
    month_sim_start = year[4:6]                     #defining the month, starting point for our simulation
    day_sim_start = year[6:8]                       #defining the day, starting point for our simulation

    # calculating the difference between year of the beginning of simulation and company foundation year
    year_dif = year_sim_start - company_found_year

    def year_list():
        """
        Creating list of years, from company found. year till simulation start point
        """
        nonlocal year_dif           #declaring free variable
        company_found_year = 2000   #declaring local variable to use inside function
        years = []
        for i in range(year_dif):               #iterating in range of year difference
            years.append(company_found_year)
            company_found_year = company_found_year + 1

        return years        #return list of years for initial calculations till simulation starting point

    years = year_list()    #assigning function year_list() return to a variable

    start_data = []                         #creating a list of company foundation values
    start_data.append(company_found_year)
    start_data.append(company_found_stock)
    start_data.append(company_found_rev)
    start_data.append(company_found_dist)
    start_data.append(company_found_rrp)

    def sim_start_numbers(start_data):
        """
        Main calculations for specific year, starting from foundation year
        :param start_data: as starting data it accepts list of initial values
        :return: list of values for specific year
        """
        year = start_data[0]            #year
        stock = start_data[1]           #stock at the begining of the year
        total_revenue = start_data[2]   #total revenue at the begining for the year
        per1_dist = start_data[3]       #first period peak (Jan 1st - till end of February distribution)
        per1_rrp = start_data[4]        #first period peak (Jan 1st - till end of February RRP)

        restoking = 600                 # restoking qty, required for stock calculation
        stock_minimum = 400             # stock minimum for restocking

        deffect_price = 0.8                             # percentage for deffect products price
        deffect_percentage = (PER_DEF / 100)            # percentage for deffect products qty
        normal_to_peak_percent_dist = 35                # increase percent for peak season distribution
        normal_to_peak_percent_rrp = 20                 # increase percent for peak season RRP
        new_finacial_year_dist = 10                     # increase percent for new fin. year distribution
        new_finacial_year_rrp = 5                       # increase percent for new fin. year RRP
        jan_days = 31                                   # number of days in january
        jan_dist = jan_days * per1_dist                 # calculation of January distribution
        rev_jan = jan_dist * per1_rrp                   # calculation of January revenue

        def stock_calc(month, period):
            """
            Calculate stock for specific month and distribution period.
            return: stock
            """
            nonlocal stock          #declaring free variable
            for i in range(month):
                if period > stock:
                    #generating error message, if distribution higher than stock available
                    #company should consider increase of restocking and min stock
                    print("You should increase restocking qty and stock minimum, at the begining"
                          " of this year", year)
                stock = stock - period
                if stock <= stock_minimum:
                    #restocking, if stock goes below stock minimum
                    stock += restoking

            return stock

        stock_calc(jan_days, per1_dist)  # calculating stock for January
        deffects_jan = jan_dist * deffect_percentage  # calculating deffects items for January
        stock += deffects_jan  # updating stock at the end of the month, adding deffects
        total_revenue += rev_jan  # updating total_revenue

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

        stock_calc(feb_days, per1_dist)  # February stock before adding deffects
        feb_dist = feb_days * per1_dist  # February distribution
        feb_rev_normal = (feb_dist - deffects_jan) * per1_rrp  # February revenue new products
        feb_rev_discount = deffects_jan * per1_rrp * deffect_price  # February revenue deffect products
        feb_rev = feb_rev_discount + feb_rev_normal  # February revenue total
        deffects_feb = (feb_dist - deffects_jan) * deffect_percentage  # February deffect products
        stock = stock + deffects_feb  # adding deffect to the stock
        total_revenue += feb_rev

        #period 2 from 1st of March till 30th of June, normal period
        period2_rrp = (per1_rrp / ((normal_to_peak_percent_rrp + 100) / 100))  # calculation rrp for period 2
        period2_dist = per1_dist / ((normal_to_peak_percent_dist + 100) / 100)  # calculation distribution for period 2

        #calculations of other months are similar to January and February
        march_days = 31                                 #number of days in March
        stock = stock_calc(march_days, period2_dist)
        march_dist = march_days * period2_dist
        march_rev_normal = (march_dist - deffects_feb) * period2_rrp
        # March revenue deffect products, calculated based on previous period product RRP, when it was returned
        march_rev_discount = deffects_feb * per1_rrp * deffect_price
        march_rev_total = march_rev_discount + march_rev_normal
        deffects_march = (march_dist - deffects_feb) * deffect_percentage
        stock += deffects_march
        total_revenue += march_rev_total

        april_days = 30    #number of days in April
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

        may_days = 31   #number of days in May
        stock = stock_calc(may_days, period2_dist)
        may_dist = may_days * period2_dist
        may_rev_normal = (may_dist - deffects_april) * period2_rrp
        may_rev_discount = deffects_april * period2_rrp * deffect_price
        may_rev_total = may_rev_discount + may_rev_normal
        deffects_may = (may_dist - deffects_april) * deffect_percentage
        stock += deffects_may
        total_revenue += may_rev_total

        june_days = 30  #number of days in June
        stock = stock_calc(june_days, period2_dist)
        june_dist = june_days * period2_dist
        june_rev_normal = (june_dist - deffects_may) * period2_rrp
        june_rev_discount = deffects_may * period2_rrp * deffect_price
        june_rev_total = june_rev_discount + june_rev_normal
        deffects_june = (june_dist - deffects_may) * deffect_percentage
        stock += deffects_june
        total_revenue += june_rev_total

        # period 3, new financial year starts, July 1st - October 31(end of normal season)
        period3_rrp = (period2_rrp + period2_rrp * (new_finacial_year_rrp / 100))  # calculating period3 rrp
        period3_dist = period2_dist + period2_dist * (new_finacial_year_dist / 100)  # calculating period3 distribution

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

        august_days = 31     #number of days in August
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

        september_days = 30     #number of days in September
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
        period4_rrp = (period3_rrp + period3_rrp * (normal_to_peak_percent_rrp / 100))  # calculating period4 rrp
        period4_dist = period3_dist + period3_dist * (
                normal_to_peak_percent_dist / 100)  # calculating period4 distribution
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

        stock += deffects_december          #total stock for the whole year

        total_revenue += december_rev_total  #total revenue for the whole year
        year += 1                            #year increment for later calculations

        per1_rrp = period4_rrp          #defining period 1 RRP for next year
        per1_dist = period4_dist        #defining period 1 distribution for next year

        # clear list with initial values, in order to put values based of calculations, will be initials
        # for next year calculations
        start_data.clear()
        start_data.append(year)
        start_data.append(stock)
        start_data.append(total_revenue)
        start_data.append(per1_dist)
        start_data.append(per1_rrp)

    crisis = 2009               #defining crisis first year
    crisis_1st_year_dist = 20   #defining crisis first year drop in distribution
    crisis_1st_year_rrp = 10    #defining crisis first year increse in RRP
    crisis_2nd_year_dist = 10   #defining crisis 2nd year drop in distribution
    crisis_2nd_year_rrp = 5     #defining crisis 2nd year increse in RRP
    crisis_3rd_year_dist = 5    #defining crisis 3rd year drop in distribution
    crisis_3rd_year_rrp = 3     #defining crisis 3rd year increse in RRP

    def calculation(years):
        """
        Calculations over the list of years, considering possible crisis
        :param years: list of years
        :return: all values required for the simulation
        """
        nonlocal crisis                 #defining free variable
        nonlocal start_data             #defining free variable
        nonlocal crisis_1st_year_rrp    #defining free variable
        nonlocal crisis_1st_year_dist   #defining free variable
        nonlocal crisis_2nd_year_dist   #defining free variable
        nonlocal crisis_2nd_year_rrp    #defining free variable
        nonlocal crisis_3rd_year_dist   #defining free variable
        nonlocal crisis_3rd_year_rrp    #defining free variable
        for i in years:
            if i == crisis:
                # checking year for crisis first year and appliyng required amendments to distribution
                # and RRP
                #calculating crisis distribution and RRP
                dist = start_data[3] - start_data[3] * (crisis_1st_year_dist / 100)
                rrp = start_data[4] * ((crisis_1st_year_rrp + 100) / 100)
                start_data[3] = dist        #changing distribution to crisis
                start_data[4] = rrp         #changing RRP to crisis
            if i == crisis + 1:     #crisis 2nd year
                dist = start_data[3] - start_data[3] * (crisis_2nd_year_dist / 100)
                rrp = start_data[4] * ((crisis_2nd_year_rrp + 100) / 100)
                start_data[3] = dist
                start_data[4] = rrp
            if i == crisis + 2:  #crisis 3rd year
                dist = start_data[3] - start_data[3] * (crisis_3rd_year_dist / 100)
                rrp = start_data[4] * ((crisis_3rd_year_rrp + 100) / 100)
                start_data[3] = dist
                start_data[4] = rrp
                crisis += 2 + CRIS_RECUR_FREQUENCY   #changing crisis year to next crisis

            sim_start_numbers(start_data)       #calling function to calculate specific year

    # final calculations till the beginning of simulation, return list of values, amended start_data
    calculation(years)

    year = start_data[0]            #amending variable with calulated value
    stock = start_data[1]           #amending variable with calulated value
    total_revenue = start_data[2]   #amending variable with calulated value
    distr = start_data[3]           #amending variable with calulated value
    rrp = start_data[4]             #amending variable with calulated value

    def year_list_sim():
        """
        Simulation over number of years, start point - value from AU_INV_START.txt, end point - depends
        on NO_YEAR_SIM value
        Creating list of years for final simulation
        :
        """
        nonlocal year               #declaring free variable
        years_sim = []              #defining list for final results
        for i in range(NO_YEAR_SIM):
            years_sim.append(year)
            year += 1
        return years_sim

    years_sim = year_list_sim()     #assigning list of years to variable

    # Final simulation over number of years, start point - value from AU_INV_START.txt, end point - depends
    # on NO_YEAR_SIM value
    calculation(years_sim)

    year = str(start_data[0]) + month_sim_start + day_sim_start    #contatination strings for futher output
    stock = start_data[1]
    total_revenue = start_data[2]

    end_dict = {}                    #creating dictionary for final outpur
    end_dict['end_year'] = int(year)
    end_dict['end_stock'] = math.ceil(stock)
    end_dict['end_revenue'] = round(total_revenue, 2)
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