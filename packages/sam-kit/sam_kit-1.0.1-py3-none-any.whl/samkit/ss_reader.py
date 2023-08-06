import csv





def read_csv(filename, types, is_header=False):
  '''
  I read a CSV and do the required type conversion and return a list
  '''

  converted_list = []
  with open(filename) as csv_file:
    rows = csv.reader(csv_file)
    if(is_header):
      headers = next(rows) # skip the header row
    
    try:
      for no, row in enumerate(rows, start=1):
        converted_list = [func(val) for func, val in zip(types, row)]      
    except ValueError as err:
      raise

  return converted_list



