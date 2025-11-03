from enum import Enum

class Compare(Enum):
    EQUAL = 1
    NOT_EQUAL = 2
    GREATER = 3
    GREATER_EQUAL = 4
    LESS = 5
    LESS_EQUAL = 6

def _isInt(s):
    """
        Function to check if a given value can be converted to an int
    """
    if s is None:
        return False
    try:
        int(s)
        return True
    except ValueError:
        return False

def _isFloat(s):
    """
        Function to check if a given value can be converted to an float
    """
    if s is None:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

def _isBool(s):
    """
        Function to check if a given value can be converted to a bool
    """
    if s is None:
        return False
    if type(s) == str:
        return s.lower() in ["true", "false", "1", "0"]
    if type(s) == bool:
        return True
    return False

def print_dict(d: dict):
    for key in d:
        print(key)
        print(d[key])
        print()

class DatasetReader:
    """
        DatasetReader is a class that will ask for a csv file and process it internally to populate a dataset. This dataset can be used alongside helper functions to be given a dictionary of filtered or sorted results
    """
    def __init__(self, filename=""):
        self.filename = filename
        self.dataset = {}

    def set_file(self, filename):
        """
            set the file to a new file
        """
        self.filename = filename

    def _formatToTypes(self):
        checkInt = False
        checkBool = False
        checkFloat = False
        copy = self.dataset.copy()
        for key in copy.keys():
            first = copy[key][0]
            if _isBool(first):
                checkBool = True
            if _isFloat(first):
                checkFloat = True
            if _isInt(first):
                checkInt = True
            for v in copy[key][1:]:
                if checkFloat and not _isFloat(v):
                    checkFloat = False
                if checkInt and not _isInt(v):
                    checkInt = False
                if checkBool and not _isBool(v):
                    checkBool = False
            if checkBool:
                temp = [True if v == '1' or v.lower() == "true" else False for v in copy[key]]
                copy[key] = temp
            elif checkFloat:
                temp = [float(v) for v in copy[key]]
                copy[key] = temp
            elif checkInt:
                temp = [int(v) for v in copy[key]]
                copy[key] = temp
        self.dataset = copy

    def _parse_internal(self):
        separator = ""
        if self.filename.endswith(".csv"):
            separator = ","
        file = open(self.filename)
        lines = file.readlines()
        for header in lines[0].split(separator):  #split on our separator for the very first line to get the header
            self.dataset[header.strip()] = [] # Instantiate that column in the dictionary as empty, we will append to this later

        keys = list(self.dataset) # Get our keys as a list for faster lookups when we go through the data

        for line in lines[1::]: # Going through line-by-line of the file starting with index 1 (second line) to end
            dataArr = line.split(separator) # split out each column of data to go through it
            for i in range(len(dataArr)):
                datum = dataArr[i].strip() # Get our specific data element we are moving in
                self.dataset[keys[i]].append(datum) # Append our datum to a list
        file.close()
        self._formatToTypes()

    def __str__(self):
        ans = self.filename + "\n"
        for key, val in self.dataset.items():
            ans += key+"\n"
            ans += str(val)+"\n\n"
        return ans

    def parse_csv(filename):
        """
            Helper function that will give back a parsed reader given a filename
        """
        ds = DatasetReader(filename)
        ds.__parse_internal()
        return ds
    
    def parse(self):
        """
            Function that will take the given internal filename and parse it into the internal dataset structure
        """
        self._parse_internal()

    def filter_columns(self, columns: list) -> dict:
        """
            filter down to a list of columns and return the filtered dictionary
        """
        filtered = {k: self.dataset[k] for k in columns if k in self.dataset}
        return filtered

    def filter_results(self, key, comp: Compare, val) -> dict:
        """
            Create a filter on the loaded in dataset, return as a dictionary
        """
        indices = []
        ans = {}
        col = self.dataset[key]
        for i in range(len(col)):
            match comp:
                case Compare.EQUAL:
                    if col[i] == val:
                        indices.append(i)
                case Compare.NOT_EQUAL:
                    if col[i] != val:
                        indices.append(i)
                case Compare.GREATER:
                    if col[i] > val:
                        indices.append(i)
                case Compare.GREATER_EQUAL:
                    if col[i] >= val:
                        indices.append(i)
                case Compare.LESS:
                    if col[i] < val:
                        indices.append(i)
                case Compare.LESS_EQUAL:
                    if col[i] <= val:
                        indices.append(i)
                case _:
                    continue
        for k, v in self.dataset.items():
            ans[k] = [v[i] for i in indices]
        return ans

    def sort_dict(dset: dict, key, descending:bool=False) -> dict:
        """
            Sort the given dataset, return as a dictionary
        """
        ans = {}
        indexed_list = list(enumerate(dset[key]))
        sorted_ilist = sorted(indexed_list, key=lambda item: item[1], reverse=descending)
        indices = [idx for idx, _ in sorted_ilist]
        for k, v in dset.items():
            ans[k] = [v[i] for i in indices]
        return ans

    def sort_results(self, key, descending:bool=False) -> dict:
        """
            return a sorted representation of the internal dataset
        """
        ans = {}
        indexed_list = list(enumerate(self.dataset[key]))
        sorted_ilist = sorted(indexed_list, key=lambda item: item[1], reverse=descending)
        indices = [idx for idx, _ in sorted_ilist]
        for k, v in self.dataset.items():
            ans[k] = [v[i] for i in indices]
        return ans


if __name__ == '__main__':
    ds = DatasetReader("courses/data/earthquake_data_tsunami.csv")
    ds.parse()
    print(ds)
    print()
    print("-"*15)
    print()
    print("Column Filter")
    col_filtered = ds.filter_columns(["tsunami", "magnitude", "latitude", "longitude", "Month", "Year"])
    print_dict(col_filtered)
    print()
    print("-"*15)
    print()
    print("Value Filter")
    val_filtered = ds.filter_results("magnitude", Compare.GREATER_EQUAL, 7.5)
    print_dict(val_filtered)
    print()
    print("-"*15)
    print()
    print("Sorting")
    print_dict(ds.sort_results("magnitude"))
    