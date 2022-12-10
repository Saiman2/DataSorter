from Helpers import Excel
import os


class Orbico:
    files = []
    nameTitles = ['ПРОДУКТ']
    price = ['Цена без ДДС']
    # priceTx = ['Доставна  цена с ДДС']

    def __init__(self, rootDir='./ToSort/ORBICO/'):
        for dateFolder in os.listdir(rootDir):
            i = 0
            for filename in os.listdir(rootDir + dateFolder + '/'):
                self.files.append(Excel.Excel(rootDir + dateFolder + '/' + filename))
                i += 1
                if i == 1:
                    break

    def run(self):
        for excel in self.files:
            sh = excel.sh
            for i in range(1, sh.max_row + 1):
                if i == 12:
                    break
                data = []
                for j in range(1, sh.max_column + 1):
                    cell_obj = sh.cell(row=i, column=j)
                    data.append(cell_obj.value)
                print('toni')
                print(data)
                excel.checkIfPositionsSet()
                if not excel.positionsSet:
                    for key, value in enumerate(data):
                        columnName = value
                        if isinstance(value, str):
                            columnName = str.join(" ", value.splitlines())

                        if columnName in self.nameTitles:
                            excel.setPosition('name', key)
                        if columnName in self.price:
                            excel.setPosition('price', key)
                        # if columnName in self.priceTx:
                        #     excel.setPosition('price_tx', key)
                    continue
                # print(excel.positions)
                # print(excel.positionsSet)
                product = []
                print('Product:')
                for value in excel.positions:
                    print(value)
                    print(excel.positions[value])
                    product.append(data[excel.positions[value]])
                print(product)
                    # exit()
                    # self.insertItem(i, item)

                # break
            # break

    def insertItem(self, data):
        for item in data:
            print(item)
