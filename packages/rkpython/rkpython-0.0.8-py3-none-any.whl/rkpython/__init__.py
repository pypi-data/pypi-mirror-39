# rk.get_mem()
def get_mem(nb_objects = 10):

#Docstring
    '''
    Prints out a list of the largest objects stored in memory, as well as the total memory usage of global variables. Returns a string.
    
    --------------
        
    nb_objects : int, default =  10
        Maximum number of items to be printed out.
        
    --------------

    Examples :
    
    get_mem(5)
    >> Total usage : 25.3 Gb
    >>
    >>  5 largest objects :
    >>  _477  :  1.7 Gb
    >>  _529  :  1.7 Gb
    >>  _437  :  1.4 Gb
    >>  _412  :  1.3 Gb
    >>  _415  :  1.3 Gb
    '''
    if type(nb_objects) != int:
        raise ValueError('Expected an integer.')
    elif  nb_objects < 0:
        raise ValueError('nb_objects needs to be positive')
    else:
        obj_dict = {}
        for var in globals():
            try: 
                obj_dict[var] = sys.getsizeof(eval(var))
            except:
                pass

        sorted_dict = sorted(obj_dict.items(), key=operator.itemgetter(1), reverse=True)

        mem_total = sum(obj_dict.values())

        mem_total = to_size(mem_total)

        print(f'Total usage : {mem_total}')
        nb_objects = min(nb_objects, len(sorted_dict))

        print(f'\n{nb_objects} largest objects :')
        for i in range(nb_objects):
            print(sorted_dict[i][0], ' : ', to_size(sorted_dict[i][1]))
			
# rk.h_size()
def h_size(size):
    
# Docstring
    '''
    Converts a size in bytes to a humanly readable size, with 1 decimal number. Input an integer, returns a string.
    
    --------------
        
    size : float, int
        Size of the object you want to convert, in bytes.
        
    --------------

    Examples :
    
    h_size(67108864)
    >>  '64.0 Mb'
    '''
    
    for unit in ['b','Kb','Mb','Gb','Tb','Pb','Eb','Zb']:
        if abs(size) < 1024.0:
            return "%3.1f %s" % (size, unit)
        size /= 1024.0
    return "%.1f %s" % (size, 'Yb')

# rk.csv_info()
class csv_info:

    '''
    Returns information about a csv or text file, such as the encoding and separators infered using csv's Sniffer() function.
    
    --------------
        
    file : str
        Path to the file you want to read.
        
    --------------
    
    csv_info().size :
        Returns the size of the file as a string.

    csv_info().separator :
        Returns the infered separator as a string.
        
    csv_info().quotechar :
        Returns the infered quote character as a string, defaults to ["].
        
    csv_info().encoding :
        Returns the infered encoding using chardet. Defaults to ascii.
        
    csv_info().rawdata :
        Returns a 8192 byte sample of the file, unencoded.

    csv_info().rows :
        Returns the number of rows in the csv file.        
        
    csv_info().columns :
        Returns the columns of the csv file.
            
    csv_info().parameters :
        Returns the separator, quotechar and encoding of the file to plug them in pandas or dask.        
            
    csv_info().info() :
        Prints out the main characteristics of the file.

    --------------

    Examples :
    
    csv_info("table.csv").encoding
    >>  'utf-8'
    
    sep, quotechar, encoding = csv_info("table.csv").parameters
    df = pandas.read_csv("table.csv", sep=sep, quotechar=quotechar, encoding=encoding)
    print(sep, quotechar, encoding)
    >>  ; " ISO-8859-1
    '''

    def __init__(self, file):
        self.size = h_size(os.path.getsize(file))

        with open(file, 'rb') as f:
            self.rawdata = f.read(8192)

            self.encoding = chardet.detect(self.rawdata)['encoding']

            self.dialect = csv.Sniffer().sniff(rawdata[:2048].decode(self.encoding))

            self.separator = self.dialect.delimiter
            self.quotechar = self.dialect.quotechar
            self.lineterminator = self.dialect.lineterminator

            self.columns = self.rawdata.decode(self.encoding).split('\n')[0].split(self.separator)

            self.parameters = iter([self.separator, self.quotechar, self.encoding])
            
            # Count rows
            for rows, l in enumerate(f):
                pass
            self.rows = rows + 1

        self.file = file

    def info(this):

        print(f"""---------- csv info ----------
size               : {this.size}
separator   : {this.separator}
quotechar  : {this.quotechar}
encoding    : {this.encoding}

{this.rows} rows, {len(this.columns)} columns""")