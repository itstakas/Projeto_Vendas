import xlwings as xw

wb = xw.Book('uploads\\Fechamento_preenchido.xlsx')

troca_data = wb.macro('LocalizarESubstituirVariasCelulas')
troca_data()

wb.save()
