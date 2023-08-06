# this is the configuration file for OSEM
import os
import json

############################################################
# default variables for all the modules
# data_folder = "data"
dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
data_folder = os.path.join(dir_path, 'osem/general/data')
cutoff = 0.45  # used to compare string, 1 is a perfect match on the string, with 0 all string match.

##############################################################
# default variables for the acesss data feature

# kbob
version_default = '2016'
data_folder_kbob = os.path.join(data_folder, 'data_kbob')
basename_unit = "kbob_unit"  # filename for the unit file: basename + version +'.csv'
basename_kbob = "kbob_data"  # filename for the kbob file: basename + version +'.csv'
filename_trans_ind = "kbob_translation_indicator.csv"   # name of the file with the translation data

# political objectives
basename_pol = "political_obj.csv"
column_not_print_pol = ['reference_year', 'objective_year', 'note', 'reference']  # columns which are not objectives

# price
precision_price = 5  # to which precision the price in CHF must be calculated
basename_price = "price_database.db"
name_tableunit = 'UNIT_TECHNO'
column_not_print_price = ["units", "reference", "note"]  # columns which are not a type of price
ref_col = "reference"
myind = "myind"
nb_point_graph = 50
interp_lim = 0.3
warning_ignore = '.*Covariance of the parameters could not be estimated.*'
opex_name = 'maintenance'

# kpi
temp_building = [[50, 25, 25], [70, 60, 50]]  # # [[%percent building], [temperature]]
filename_eff = 'kpi_efficiency_heating.csv'
temp_ext = 22  # exterior temperature °C

# meteo data
data_folder_meteo = os.path.join(data_folder, 'data_meteo_swiss')
filenames = [i for i in os.listdir(data_folder_meteo) if i != 'data_source.txt']
nbline_header = 5  # the number of lines which compsed the header (no empty line)
line_with_unit = 6  # the index of the line where the unit is (with empty line)
col_name = ['station_name', 'elev_m', 'coordinates_CH', 'period_reference', 'january', 'february', 'march', 'april',
            'may', 'june','july', 'august', 'september', 'october', 'november', 'december', 'annual']
month_name = ['january', 'february', 'march', 'april', 'may', 'june','july', 'august', 'september', 'october',
              'november', 'december']


###############################################################
# default value for the plot

# plot kpi
xlabel = 'Years'
ylabelco2 = 'CO$_{2}$ emission [kg]'
ylabelfinal = 'Final Energy [kWh]'
ylabelprimary = 'Primary Energy [kWh]'
ylabelrenew = 'Primary Energy [kWh]'
renew_colname = ['years', 'scenarios','renewable', 'non-renewable']
fontsize =12
width = 0.2
figsize = (8,8)


#############################################################
# default value for network

# pandangas

default_levels = {"HP": 5.0E5, "MP": 1.0E5, "BP+": 0.1E5, "BP": 0.025E5}  # Pa
lhv = 38.1E3  # kJ/kg
v_max = 2.0  # m/s
temperature = 10 + 273.15  # K
p_atm = 101325
scaling = 1
min_p_pa = 0.022E5
mat_default = 'steel'
corr_pnom = 1 # the ratio between the max pressure (p_nom) and the average pressure of the network

default_solver_option= {'tol_mat_mass': 1e-10,
                        'tol_mat_pres': 1e-10,
                        'maxiter': 1e7,
                        'gtol': 1e-5,
                        'round_num': 5,
                        'disp' : False,
                        'min_residual': 3,
                        'iter_print': 50
}

filename_info_solver = 'pandangas_info_solver_option.json'

#############################
data_folder_enerapi = os.path.join(data_folder, 'enerapi_data')
file_per = 'period_RegBL.json'
file_affect = 'affect_RegBL.json'
file_ratio = 'ratio_base.json'
year_period = [1,1919,1946,1961,1971,1981,1986,1991,1996,2001,2006,2011,2015]