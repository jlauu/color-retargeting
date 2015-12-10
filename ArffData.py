"""
Johnny Lau

Summary: ARFF Data Class

"""
class ArffData:
        def __init__(self, name, *attr):
                self.name = name
                self.attr = {}
                for a in attr:
                        self.attr[a[0]] = a[1]
                self.data = []


        def add_point(self, vector):
                self.data.append(vector)

        def pprint(self):
                print(self.name)
                self.print_attr()
                self.print_data()

        def print_attr(self):
                for k,v in self.attr.items():
                        print("@attribute " + k + " " + v)

        def print_data(self):
                for point in self.data:
                        print(point)
