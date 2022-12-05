from Helpers import Excel
import os


class Orbico:
    files = []
    nameTitles = ['ПРОДУКТ']
    price = ['Цена без ДДС']
    priceTx = ['Доставна  цена с ДДС']

    def __init__(self, rootDir='./ToSort/ORBICO/'):
        for dateFolder in os.listdir(rootDir):
            print(dateFolder)
            i = 0
            for filename in os.listdir(rootDir + dateFolder + '/'):
                print(filename)
                self.files.append(Excel.Excel(rootDir + dateFolder + '/' + filename))
                i += 1
                if i == 1:
                    break

    def run(self):
        for excel in self.files:
            sh = excel.sh
            for i in range(1, sh.max_row + 1):
                if i == 8:
                    break
                data = []
                for j in range(1, sh.max_column + 1):
                    cell_obj = sh.cell(row=i, column=j)
                    data.append(cell_obj.value)

                excel.checkIfPositionsSet()
                if not excel.positionsSet:
                    for key, value in enumerate(data):
                        columnName = value
                        if isinstance(value, str):
                            columnName = str.join(" ", value.splitlines())
                        # print('value: ')
                        # print(columnName)
                        if columnName in self.nameTitles:
                            excel.setPosition('name', key)
                        if columnName in self.price:
                            excel.setPosition('price', key)

                        if columnName in self.priceTx:
                            excel.setPosition('price_tx', key)
                # print(excel.positions)
                # print(excel.positionsSet)
                if excel.positionsSet:
                    item = []
                    for value in excel.positions:
                        print(value)
                        print('asd')
                        print(excel.positions[value])
                        item.append(data[excel.positions[value]])
                    print(item)
                    # exit()
                    # self.insertItem(i, item)

                # break
            # break

    def insertItem(self, data):
        for item in data:
            print(item)
