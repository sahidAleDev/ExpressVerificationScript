import csv
from abc import ABC, abstractmethod

class CSVReader(ABC):
    @abstractmethod
    def read_csv_file(self, filename_csv):
        pass

class ExcelCSVReader(CSVReader):
    def read_csv_file(self, filename_csv):
        csv_data = csv.reader(open(filename_csv))
        next(csv_data)
        next(csv_data)
        next(csv_data)

        client_names = set()
        aval_names = set()
        for row in csv_data:
            full_name_client = row[2] + " " + row[3] + " " + row[4]
            full_name_aval = row[408] + " " + row[409] + " " + row[410]
            client_names.add(full_name_client)
            aval_names.add(full_name_aval)

        return client_names, aval_names

class OdooCSVReader(CSVReader):
    def read_csv_file(self, filename_csv):
        csv_data = csv.reader(open(filename_csv))
        next(csv_data)

        rows = set()
        for row in csv_data:
            rows.add(row[0])

        return rows

class ListComparer:
    def compare_lists(self, list1, list2):
        result = []
        common_names = list1.intersection(list2)
        for name in list1:
            result.append([name, name in common_names])

        return result

class ResultPrinter:
    def print_match(self, result):
        match = 0
        no_match = 0
        for item in result:
            if item[1]:
                match += 1
            else:
                no_match += 1

        print("Matches:", match)
        print("No matches:", no_match)

excel_csv_reader = ExcelCSVReader()
odoo_csv_reader = OdooCSVReader()

csvExcelClient, csvExcelAval = excel_csv_reader.read_csv_file("BD DINERO XPRESS 2023. CRUDA SEMANA 25 CSV.csv")

csvOdooClient = odoo_csv_reader.read_csv_file("Préstamo (dev.loan.loan).csv")
csvOdooAval = odoo_csv_reader.read_csv_file("Contacto (res.partner).csv")

len(csvExcelAval)


print("Total de clientes en el csv crudo:", len(csvExcelClient))
print("Total de clientes en el csv de Odoo:", len(csvOdooClient))
print("Total de avales en el csv crudo:", len(csvExcelAval))
print("Total de avales en el csv de Odoo", len(csvOdooAval))

resultExcelClient = ListComparer().compare_lists(csvExcelClient, csvOdooClient)
resultOdooClient = ListComparer().compare_lists(csvOdooClient, csvExcelClient)
resultExcelAval = ListComparer().compare_lists(csvExcelAval, csvOdooAval)
resultOdooAval = ListComparer().compare_lists(csvOdooAval, csvExcelAval)

result_printer = ResultPrinter()

print("\nClientes en el Excel:")
result_printer.print_match(resultExcelClient)
print("\nClientes en Odoo:")
result_printer.print_match(resultOdooClient)
print("\nAvales en el Excel:")
result_printer.print_match(resultExcelAval)
print("\nAvales en el Odoo: ")
result_printer.print_match(resultOdooAval)


#print(resultOdooAval)