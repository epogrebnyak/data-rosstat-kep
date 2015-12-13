
#------------------------------------------------------------------------------
#  Testing
#------------------------------------------------------------------------------

def test_flat_emitter():
    lab_rows = [['I', 'bln_rub', '2014', '13527,7', '1863,8', '2942,0', '3447,6', '5274,3', '492,2', '643,2', '728,4', '770,4', '991,1', '1180,5', '1075,1', '1168,5', '1204,0', '1468,5', '1372,5', '2433,3']   
              , ['PROD_TRANS', 'rog', '2015', '31,1', '126,3', '139,8', '83,8', '94,6', '115,8', '', '', '', '', '', '']]
    
    flat_db_rows = [('a', 'I_bln_rub', 2014, SAFE_NONE, SAFE_NONE, 13527.7),
                    ('q', 'I_bln_rub', 2014, 1, SAFE_NONE, 1863.8),
                    ('q', 'I_bln_rub', 2014, 2, SAFE_NONE, 2942.0),
                    ('q', 'I_bln_rub', 2014, 3, SAFE_NONE, 3447.6),
                    ('q', 'I_bln_rub', 2014, 4, SAFE_NONE, 5274.3),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 1, 492.2),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 2, 643.2),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 3, 728.4),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 4, 770.4),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 5, 991.1),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 6, 1180.5),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 7, 1075.1),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 8, 1168.5),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 9, 1204.0),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 10, 1468.5),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 11, 1372.5),
                    ('m', 'I_bln_rub', 2014, SAFE_NONE, 12, 2433.3),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 1, 31.1),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 2, 126.3),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 3, 139.8),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 4, 83.8),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 5, 94.6),
                    ('m', 'PROD_TRANS_rog', 2015, SAFE_NONE, 6, 115.8)]    
    
    assert [x for x in stream_flat_data(lab_rows)] == flat_db_rows 
   
def get_test_flat_db_rows():
    from label_csv import get_test_labelled_rows
    lab_rows = get_test_labelled_rows()
    return stream_flat_data(lab_rows)
    
if __name__ == "__main__":
    test_flat_emitter()
    for i, x in enumerate(get_test_flat_db_rows()):
        print(i, x)