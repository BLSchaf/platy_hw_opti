
def extract_comp_origin(original_hgdata):
    '''Extract compliance of original model from .hgdata'''
    
    with open('{}'.format(original_hgdata)) as ifile:
      lines = list(ifile)
      comp_origin = float(lines[-1])
      return comp_origin

def extract_comp_new(path_temp):
    '''Extract compliance of new model from .hgdata'''

    with open('{}.hgdata'.format(path_temp)) as ifile:
      lines = list(ifile)
      comp_new = float(lines[-1])
      return comp_new
