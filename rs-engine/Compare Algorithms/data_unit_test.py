import unittest
import pandas as pd

def read_file(filename):
    dataframe = pd.read_excel(filename + '.xlsx')
    return dataframe

class TestCalculations(unittest.TestCase):

    def test_training_data_exists(self):
        
        file_exists = False

        try:
            file = open("train_data.xlsx", "r")
            file.close()
            file_exists = True
        except:
            pass
        self.assertEqual(file_exists, True, 'Test Failed: Please Upload train_data.xlsx file to the Compare algorithms directory')

 
    def test_testing_data_exists(self):
        
        file_exists = False

        try:
            file = open("test_data.xlsx", "r")
            file.close()
            file_exists = True
        except:
            pass
        self.assertEqual(file_exists, True, 'Test Failed: Please Upload test_data.xlsx file to the Compare algorithms directory')

    def test_all_users_in_training_data(self):
         
       
        num_users = 209
        users_in_data = set()
        
        df = read_file("train_data")
        for index, line in df.iterrows():
            users_in_data.add(line[' customer_id'])

        self.assertEqual(len(users_in_data), num_users, 'Not all of the customer ids are in train data')


    def test_all_users_in_testing_data(self):
         
       
        num_users = 209
        users_in_data = set()
        
        df = read_file("test_data")
        for index, line in df.iterrows():
            users_in_data.add(line[' customer_id'])

        self.assertEqual(len(users_in_data), num_users, 'Not all of the customer ids are in test data')

if __name__ == '__main__':
    unittest.main()















