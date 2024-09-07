from common.print_result import *
from common.utils import *
from core.calc import *

if __name__ == '__main__':
    start_date, end_date = gen_date_pair_by_days(366)
    show_result(calc_open_fund_gain_debug("167301", start_date, end_date, log=False))