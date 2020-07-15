import pandas as pd
import xlsxwriter

# Creo el libro excel y una hoja
outWorkbook = xlsxwriter.Workbook("filterTwits.xlsx")
outSheet = outWorkbook.add_worksheet()


# Declaro los datos
names = ["kyle", "bob", "mary"]
values = [70, 80, 71]

# Escribo nombre de columnas
outSheet.write("A1", "Names")
outSheet.write("B1", "Scores")
outSheet.write("C1", "Promedio")

# 


# Lo cierro para que se cree
outWorkbook.close()


