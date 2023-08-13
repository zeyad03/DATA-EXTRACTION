"""
Please write your name
@author: ZEYAD BASSYOUNI

"""

# Reminder: You are only allowed to import the csv module (done it for you).
# OTHER MODULES ARE NOT ALLOWED (NO OTHER IMPORT!!!).

import csv


class Leopard:

    def __init__(self, filepath: str) -> None:

        self.filepath = filepath
        self.lst = []       # Main list of all data in csv file.
        self.pos = []       # Holds positions of columns with numerical values.
        self.num = []       # Numerical values to extract maximum and minimum.
        self.count = []     # List holds the count of data in a coloumn.
        self.dic = {}       # Stores count, mean, maximum, minimum of data.
        error = 0           # Error stores 1 if the file does not exists.

        try:
            # Read file
            with open(filepath, 'r') as fileObject:
                reader = csv.reader(fileObject)
                i = 0   # Row number.
                j = 0   # Column number.

                # Reading data from reader and store them in form of lists.
                for row in reader:
                    self.lst.append(row)

                    for col in row:
                        # Ignore non-existant values.
                        if col == '' or col == '-' or col == 'NA':
                            self.lst[i][j] = '-1'
                        else:
                            j += 1

                    # Reset the index of column to start from 0 again.
                    j = 0
                    i += 1
        except Exception:
            error = 1
            return

        # Check if the file exists or empty and print the proper message.
        if error == 1:
            print('file not found.')
        elif self.lst == []:
            print('empty file.')
        else:
            return

    def get_header(self) -> list:
        # Check that the file isn't empty and if so return the header.
        if self.lst != []:
            return self.lst[0]
        else:
            return None

    def get_data(self) -> list:
        # Check that the file isn't empty and if so return the rest of data.
        if self.lst != []:
            return self.lst[1:]
        else:
            return None

    def stats(self) -> list:

        try:
            col_num = 0
            # Iterate over row no.2 returned from get_data() method.
            for col in self.get_data()[1]:
                # Store numerical columns in self.pos list.
                if col.isnumeric() is True:
                    self.pos.append(col_num)
                col_num += 1

            # Loop to go through rows.
            for num in range(len(self.pos)):

                # Define/reset sum and count values when starting new column.
                count = 0
                sum = 0

                # loop to go through columns.
                for row in range(1, len(self.lst)):
                    # Store each column in a nested list.
                    self.num.append(self.lst[row][self.pos[num]])
                    # Summation of all data in a column.
                    sum += int(self.lst[row][self.pos[num]])
                    count += 1  # Count the number of data in a column.

                    # Decrease count if there is a value need to be ignored.
                    if self.lst[row][self.pos[num]] == '-1':
                        count -= 1

                # Store the count of values in a list for each column.
                self.count.append(count)

                # Nested dictionary for needed output values.
                self.dic[self.lst[0][self.pos[num]]] = {
                    'count': count,
                    'mean': round(sum/count, 2),
                    'min': min(mini for mini in self.num if int(mini) > 0),
                    'max': max(self.num, key=lambda value: int(value))
                    }

                # Reset self.num list to store new data for new columns.
                self.num = []
            return self.dic
        except Exception:
            return None

    def html_stats(self, stats: dict, filepath: str) -> None:

        try:
            # Open new file and append it.
            with open("filepath.html", 'a') as html:
                html.write('<html>\n')
                html.write('<title>filepath</title>\n')
                html.write('<center>\n')
                html.write('<h1>')
                html.write(str(filepath.replace('.html', '')))
                html.write('</h1>\n')

                # Create table.
                html.write('<style>\n')
                html.write('table, th, td {\n border: 1px solid black;\n')
                html.write('border-collapse: collapse; text-align:center\n')
                html.write('}\n')
                html.write('</style>\n')
                html.write('<table>\n')

                # Presentig the headers at the top of the table.
                html.write('<th style= "background-color:black;"></th>\n')
                for key in stats:
                    html.write('<td\n')
                    html.write('style=')
                    html.write('"background-color:green;color:white;">\n')
                    html.write('<b>' + key + '</b>\n')
                    html.write('</td>\n')

                # Get data from the method stats().
                nested_list = []    # Main list.
                item_list = []      # Smaller lists.
                for key in stats:
                    for data in stats[key]:
                        item_list.append(stats[key][data])
                    nested_list.append(item_list)
                    item_list = []      # Reset to store new data.

                # Presenting the rest of data in the table.
                name = ['count', 'mean', 'minimum', 'maximum']
                num = 0
                # Names to the very left column.
                for item in name:
                    html.write('<tr>\n')
                    html.write('<td')
                    html.write('style="background-color:red;color:white;">\n')
                    html.write('<b>' + str(item) + '</b>\n')
                    html.write('</td>\n')
                    # Data in from of those names.
                    for row in nested_list:
                        html.write('<td style="background-color:yellow;">')
                        html.write(str(row[num]))
                        html.write('</td>\n')
                    html.write('</tr>\n')
                    num += 1

                # Close HTML.
                html.write("</table>\n\n")
                html.write('</center>\n')
                html.write('</html>\n')
                return html
        except Exception:
            return None

    def count_instances(self, criteria) -> int:

        """This method accepts only strings where the string is in
        the format of the header that is required searching for,
        and the instances are also in the same format. To trigger
        this method, just call it and enter the required search
        with the header in the same format as it is in the csv
        file, then the equal sign, then the instances you
        looking for. Using ex1it will return the number of
        times that there are ages of 20s in that column.
        Ex1, count_instances('age=20').
        Ex2, count_instances('school=GP').
        Ex3, count_instances('Medu=teacher')."""

        try:
            input = []                      # List to store the input.
            input = criteria.split('=')     # Separate before and after = sign.
            col_num = 0                     # Column number of header required.
            count = 0                       # Count of instances.

            # Find the header matches the required instance.
            for item in self.get_header():
                if item != input[0]:
                    col_num += 1
                else:
                    break

            # Loop to count the number of instance in a column.
            for row in self.get_data():
                if input[1] == row[col_num]:
                    count += 1

            return count
        except Exception:
            return None


if __name__ == "__main__":
    # DO NOT COMMENT ALL WHEN SUBMIT YOUR FILE, cannot have an if statement
    # with nothing afterwards.

    # test diabetes_data.csv
    test = Leopard("diabetes_data.csv")
    print(test.get_header())
    print(test.get_data())
    stats = test.stats()
    print(stats)
    test.html_stats(stats, "diabetes_data.html")
    print()

    # test fide2021.csv
    test2 = Leopard("fide2021.csv")
    print(test2.get_header())
    print(test2.get_data())
    stats2 = test2.stats()
    print(stats2)
    test2.html_stats(stats2, "fide2021.html")
    print()

    # test student.csv
    test3 = Leopard("student.csv")
    print(test3.get_header())
    print(test3.get_data())
    stats3 = test3.stats()
    print(stats3)
    test3.html_stats(stats3, "student.html")
