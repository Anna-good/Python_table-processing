import csv
import pickle
import io
import pandas
from tabulate import tabulate
from tkinter import filedialog as fd

class TablePackage():
    def __init__(self, csv = None): #инит нужен для подразделения для указания показаний для подгрузки файла с таблицей.
        if csv is None:
            self.load_table()
        else:
            self.csv = csv

    def load_table(self): # open_file
        files = [('CSV Files', '*.csv'),
                 ('Text Document', '*.txt'),
                 ('Pickle Files', '*.pkl')] 
        self.file_name = fd.askopenfilename(filetypes=files, defaultextension=files)
        expected_file_format = self.file_name[-4:] # обрезание у строки последние 4 символа (формат файла)

        try:
            if '.csv' == expected_file_format:
                self.csv = pandas.read_csv(self.file_name)
            elif '.pkl' == expected_file_format:
                self.csv = pandas.read_pickle(self.file_name)
            elif '.txt' == expected_file_format:
                self.csv = pandas.read_csv(self.file_name)
        except:
            print("Unable to read the file") # обработка исключений для каждого типа файла

        try:
            pandas.options.display.max_rows = len(self.csv)
        except:
            print("The file was not opened")
    
    def save_table(self):
        files = [('CSV Files', '*.csv'),
                 ('Text Document', '*.txt'),
                 ('Pickle Files', '*.pkl')]
        file_name = fd.asksaveasfile(filetypes=files, defaultextension=files)
        expected_file_format = file_name[-4:]

        if '.csv' == expected_file_format:
            self.csv.to_csv(file_name)
        elif '.pkl' == expected_file_format:
            with open(file_name.name, 'wb') as file_obj:
                self.csv.to_pickle(file_obj)
        elif '.txt' == expected_file_format:
            with open(file_name.name, 'a') as file_obj:
                file_obj.write(
                    self.csv.to_string(header=True, index=False)
                )

    def print_table(self, ):
        try:
            print(tabulate(self.csv, headers=self.csv.columns, tablefmt="rounded_grid"))
        except:
            print("Unable to print the table, try re-uploading it")

    def get_rows_by_number(self, start, stop, copy_table=False):
        info = '\n\n\nget_rows_by_number(start, [stop], copy_table=False) – получение таблицы из одной строки или из строк из интервала по номеру строки.' \
               ' Функция либо копирует исходные данные, либо создает новое представление таблицы, работающее с исходным набором данных (copy_table=False),' \
               ' таким образом изменения, внесенные через это представления будут наблюдаться и в исходной таблице.'
        try:
            new_csv = self.csv[start:stop + 1]
        except:
            if start < 0:
                print("The start argument is less than zero aka out of range")
            elif stop > self.csv.__len__():
                print("The end argument is out of range")
            else:
                print("The arguments aren't correct")

        if not copy_table:
            self.csv = new_csv

        return new_csv

    # The first required argument (`tabular_data`) can be a
    # list-of-lists (or another iterable of iterables)
    def get_rows_by_index(self, tabular_data, copy_table=False):
        info = '\n\n\nget_rows_by_index(val1, … , copy_table=False) – получение новой таблицы из одной строки или из строк со' \
               ' значениями в первом столбце, совпадающими с переданными аргументами val1, … , valN. Функция либо копирует ' \
               'исходные данные, либо создает новое представление таблицы, работающее с исходным набором данных (copy_table=False),' \
               ' таким образом изменения, внесенные через это представления будут наблюдаться и в исходной таблице.' \
               '\n\n\nВводить стольцы через запятую!'
        
        try:
            if type(tabular_data) == int:
                new_csv = self.csv.loc[[tabular_data],:]
            else:
                new_csv = self.csv.loc[tabular_data,:]
        except KeyError:
            print('Something happened wrong')
        except AttributeError:
            print('Enter the rows that are in the table')
        except IndexError:
            print('Enter the rows that are in the table')

        if not copy_table:
            self.csv = new_csv

        return new_csv

    def get_column_types(self, by_number=True):
        #by_number - built-in
        info='\n\n\nget_column_types(by_number=True) – получение словаря вида столбец:тип_значений. ' \
             'Тип значения: int, float, bool, str (по умолчанию для всех столбцов). Параметр by_number ' \
             'определяет вид значения столбец – целочисленный индекс столбца или его строковое представление.' \
             '\n\n\n'

        self.csv.dtypes()

        buffer = io.StringIO()
        self.csv.info(buf=buffer, show_counts=False, memory_usage=False)
        column_types = buffer.getvalue()

        print(column_types)

        return column_types

    def get_values(self, column = 0):
        info='\n\n\nget_values(column=0) – получение списка значений ' \
             '(типизированных согласно типу столбца) таблицы из ' \
             'столбца либо по номеру столбца (целое число, значение ' \
             'по умолчанию 0, либо по имени столбца)'

        try:
            type_verified_column = int(column)
        except:
            type_verified_column = column

        try:
            if type(type_verified_column) == str:
                new_csv = self.csv[column]
            elif type(type_verified_column) == int:
                column_index = self.csv.columns[type_verified_column]
                new_csv = self.csv[column_index]
        except KeyError:
            print('Something happened wrong')
        except TypeError:
            print('The columns that being compared should not be string and numbers')
        except IndexError:
            print('Enter the rows that are in the table')

        print(new_csv)

        return(new_csv)

    def set_values(self, values, column):
        info = '\n\n\nset_values(values, column=0) – задание списка значений values для столбца таблицы' \
               ' (типизированных согласно типу столбца) либо по номеру столбца (целое число, значение по умолчанию 0, либо по имени столбца).'
        frame = self.csv
        try:
            type_verified_column = int(column)
        except:
            type_verified_column = column
        try:
            if type(type_verified_column) == str:
                frame.loc[:, type_verified_column] = values  # Set value for an entire column
                new_csv = frame
            elif type(type_verified_column) == int:
                column_index = frame.columns[type_verified_column]
                frame.loc[:, column_index] = values
                new_csv = frame
        except KeyError:
            print('Something happened wrong')
        except TypeError:
            print('The columns that being compared should not be string and numbers')
        except IndexError:
            print('Enter the rows that are in the table')
        
        print(new_csv)

        return(new_csv)
    
    def column_types_auto_setting(self):
        for column_name in self.csv.columns():
            self.csv[column_name] = pandas.to_datetime
    
    def split(self, row_number):
        new_csv = self.get_rows_by_number(row_number + 1, self.csv.__len__() - 1, copy_table=True)
        self.get_rows_by_number(0, row_number)

        return TablePackage(new_csv)

    def concat(self, attached_table_package):
        self.csv = pandas.concat([self.csv, attached_table_package.csv], axis=0)

    def calculate_average_total_votes(self):
        average_total_votes = self.get_values("total_votes").sum() / self.csv.__len__()
        
        print(average_total_votes)

        return average_total_votes
class TableManager():
    def __init__(self):
        self.table_packages = list()
    
    def load_table(self):
        self.table_packages.append(TablePackage())

def main():

    tp = TablePackage() #контейнер для содержания таблиц
    # tp2 = TablePackage()
    # tp.concat(tp2)
    tp.split(50)
    tp.print_table()
    tp.calculate_average_total_votes()
    # tp.load_table()
    # tp.get_rows_by_number(2, 110)
    # tp.get_rows_by_index(6)
    # tp.get_rows_by_index((6, 7, 8))
    # tp.print_table()
    # tp.get_column_types()
    # tp.get_values("county")
    input()
if __name__ == '__main__':
    main()