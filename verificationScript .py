import csv
from abc import ABC, abstractmethod
from openpyxl import Workbook

class CSVReader(ABC):
    @abstractmethod
    def read_csv_file(self, filename_csv):
        pass

class ExcelCSVReader(CSVReader):
    def read_csv_file(self, filename_csv):
        with open(filename_csv) as file:
            csv_data = csv.reader(file)
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
        with open(filename_csv) as file:
            csv_data = csv.reader(file)
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

class ExcelCreator:
    def __init__(self, workbook):
        self.workbook = workbook

    def create_excel(self, file_name, data, source_of_comparison):
        try:
            sheet = self.workbook.active

            total_records, match, no_match = self.get_matches(data)
            print("Result", file_name, total_records, match, no_match)

            sheet['A1'] = 'Nombre'
            sheet['B1'] = '¿Se encuentra en %s?' % source_of_comparison
            sheet['D1'] = "Total de personas"
            sheet['E1'] = "Coincidencias"
            sheet['F1'] = "No Coincidencias"
            sheet['D2'] = total_records
            sheet['E2'] = match
            sheet['F2'] = no_match

            for i, dato in enumerate(data, start=2):
                sheet[f'A{i}'] = dato[0]
                sheet[f'B{i}'] = dato[1]

            full_file_name = file_name + ".xlsx"
            self.workbook.save(full_file_name)
            print("Archivo %s creado con éxito\n" % full_file_name)
        except Exception as e:
            print("Error:", str(e))

    def get_matches(self, data):
        match = 0
        no_match = 0
        for item in data:
            if item[1]:
                match += 1
            else:
                no_match += 1

        return len(data), match, no_match


def main():
    excel_csv_reader = ExcelCSVReader()
    odoo_csv_reader = OdooCSVReader()

    csv_semana_cruda_client, csv_semana_cruda_aval = excel_csv_reader.read_csv_file("BD DINERO XPRESS 2023. CRUDA SEMANA 25 CSV.csv")

    csv_odoo_client = odoo_csv_reader.read_csv_file("Préstamo (dev.loan.loan).csv")
    csv_odoo_aval = odoo_csv_reader.read_csv_file("Contacto (res.partner).csv")

    excel_clients_with_odoo = ListComparer().compare_lists(csv_semana_cruda_client, csv_odoo_client)
    odoo_clients_with_excel = ListComparer().compare_lists(csv_odoo_client, csv_semana_cruda_client)

    excel_avals_with_odoo = ListComparer().compare_lists(csv_semana_cruda_aval, csv_odoo_aval)
    odoo_avals_with_excel = ListComparer().compare_lists(csv_odoo_aval, csv_semana_cruda_aval)

    workbook = Workbook()
    excel_creator = ExcelCreator(workbook)

    excel_creator.create_excel("excel_clients_in_odoo", excel_clients_with_odoo, "Odoo")
    excel_creator.create_excel("excel_avals_in_odoo", excel_avals_with_odoo, "Odoo")

    excel_creator.create_excel("odoo_clients_in_excel", odoo_clients_with_excel, "Excel")
    excel_creator.create_excel("odoo_avals_in_excel", odoo_avals_with_excel, "Excel")

    workbook.close()


if __name__ == "__main__":
    main()
