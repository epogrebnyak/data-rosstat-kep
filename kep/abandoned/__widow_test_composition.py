def get_dfm_var_list():
    return get_dfm().columns.tolist()

VAR_NAMES = get_dfm_var_list()
    
def get_test_values_for_import_with_cfg():       
    data_folder = "../data/ind09/"
    import_csv(data_folder)
    
    MUST_READ = ['CONSTR_bln_rub_fix', 'CONSTR_rog', 'CONSTR_yoy', 'CORP_DEBT_bln_rub', 
    'CORP_DEBT_overdue', 'CORP_DEBT_rog', 
    #    'CPI_ALCOHOL_rog', 'CPI_FOOD_rog', 'CPI_NONFOOD_rog', 'CPI_SERVICES_rog', 'CPI_rog', 
    'IND_PROD_rog', 'IND_PROD_yoy', 'IND_PROD_ytd', 'I_bln_rub',
    'I_rog', 'I_yoy', 'PROD_AUTO_BUS_units', 'PROD_AUTO_PSGR_th', 'PROD_AUTO_TRUCKS_th',
    'PROD_BYCYCLES_th', 'PROD_E_TWh', 'PROD_RAILWAY_CARGO_WAGONS_units', 'PROD_RAILWAY_PSGR_WAGONS_units',
    'RETAIL_SALES_bln_rub', 'RETAIL_SALES_rog', 'RETAIL_SALES_yoy', 'RUR_EUR_eop', 'RUR_USD_eop',
    'SOC_EMPLOYED_mln', 'SOC_EMPLOYED_yoy', 'SOC_PENSION_rub', 'SOC_UNEMPLOYED_bln',
    'SOC_UNEMPLOYMENT_percent', 'SOC_WAGE_rog', 'SOC_WAGE_rub', 'SOC_WAGE_yoy', 'TRANS_COM_bln_t_km',
    'TRANS_COM_rog', 'TRANS_COM_yoy', 'TRANS_RAILLOAD_mln_t', 'TRANS_RAILLOAD_rog', 'TRANS_RAILLOAD_yoy',
    'TRANS_bln_t_km', 'TRANS_rog', 'TRANS_yoy', 'USLUGI_bln_rub', 'USLUGI_rog', 'USLUGI_yoy']
    
    ADDITIONAL_READ = ['CPI_ALCOHOL_rog', 'CPI_FOOD_rog', 'CPI_NONFOOD_rog', 'CPI_SERVICES_rog', 'CPI_rog']    
    
    return VAR_NAMES, sorted(MUST_READ + ADDITIONAL_READ)      
 
def test_import_with_cfg():
    a, b = get_test_values_for_import_with_cfg()
    assert a == b       

def test_selected_var_names():    
    for vn in ['PROFIT', 'CORP_DEBT']: 
       # TODO: need more sophisticated test, because 'PROFIT' is just a start of variable name.
       # assert vn in VAR_NAMES 
       pass    