import pandas as pd
import random

def read_file(filename):
    dataframe = pd.read_excel(filename + '.xlsx')
    return dataframe

class Processor:

    def __init__(self, df, train_overlap_chance = 0, test_overlap_chance = 0):
        self.df = df
        self.train_overlap_chance = train_overlap_chance
        self.test_overlap_chance = test_overlap_chance
    
    def split(self, train_ratio, all_ids_in_training = True):

        train = []
        test = []

        counter = 0
        prev_id = None

        train_contains_ids = set()

        for index, line in self.df.iterrows():

            user_id = line[' customer_id']

            if (prev_id == None or user_id != prev_id):
                test.append(line)
                if(random.uniform(0, 1) < self.train_overlap_chance):
                    train.append(line)
                    train_contains_ids.add(user_id)
                prev_id = user_id
                counter = 0
            elif counter > train_ratio:
                test.append(line)
                if(random.uniform(0, 1) < self.train_overlap_chance):
                    train.append(line)
                    train_contains_ids.add(user_id)
                counter = 0
            else:
                train.append(line)
                train_contains_ids.add(user_id)
                if(random.uniform(0, 1) < self.test_overlap_chance):
                    test.append(line)
            
            counter += 1

        if all_ids_in_training:
            for index, line in self.df.iterrows():
                user_id = line[' customer_id']
                if user_id not in train_contains_ids:
                    train.append(line)


        train_data = pd.DataFrame(train)
        test_data = pd.DataFrame(test)

        train_data.to_excel("train_data.xlsx")  
        test_data.to_excel("test_data.xlsx")  

p = Processor(read_file("interaction"))
p.split(3)