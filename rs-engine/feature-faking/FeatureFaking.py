import pandas as pd
import csv
import random
import operator

#-------------------------------------------------------------------------
# This is a novel attempt for recommendation system.
# FILE FeatureFaking.py is intended for creating x amount of fake features
# The same feature is assigned for client and for the item. 
# Then percentage of feature is assigned to an item.
# For example Banna consists of 40% feature 1, 60% of feature 2 and 0% of feature 3.
# Then when user purchases the banana their first feature is raised by 40% and second is raised by 60%.
# This will cause a reduce in feature 3.
# Thus next item will be the most simmilar for the user features.
# During training/simulation when wrong ittem is recmmended the suggestion is scaled accordingly for item features.

# Work in progress:
# Change scaling.

#--------------------------------------------------------------------------

#-------------------------------------------------------
# Reading a file
#-------------------------------------------------------
def read_file(filename):
    try:
        dataframe = pd.read_excel(filename + '.xlsx')
    except:
        dataframe = pd.read_csv(filename + '.csv')
    return dataframe

#-------------------------------------------------------
# DROPPING UNNECCESSARY DATA
#-------------------------------------------------------
#df_product = read_file("nosh_product_data")
#df_purchase = read_file("_purchase_data")
#df_product = df_product.drop("shelf_life", axis = 1)
#df_product = df_product.drop("usual_storage", axis = 1)

#df_purchase = df_purchase.drop("customer_name", axis = 1)
#df_purchase = df_purchase.drop("invoice_id", axis = 1)
#df_purchase = df_purchase.drop("purchase_date_time", axis = 1)
#df_purchase = df_purchase.drop("Unnamed: 0", axis = 1)
#--------------------------------------------------------

#print(df_product.head().to_string())
#print(df_purchase.head().to_string())
#print(df_user.head().to_string())


#-------------------------------------------------------------------
# Product Struct/Class Main idea is to link datatypes
#-------------------------------------------------------------------

class Product:

    #Constructor
    def __init__(self, id, name, num_features):

        self.id = id
        self.name = name
        self.features = []

        total_percentage = 100
        
        for i in range(num_features):
            self.features.append(0)
   
        while total_percentage > 0:
            amount_to_add = random.randint(0, total_percentage)
            total_percentage -= amount_to_add
            feature = random.randint(0, len(self.features)-1)
            self.features[feature] += amount_to_add
    


    # Automatic To String
    def __repr__(self):
        """
        representation = "Product " + str(self.id) +": " + str(self.name) + " Features: ["
        for feature in self.features:
            representation += str(feature) + "% "

        return representation + "]"
        """
        return str(self.id)

    # Helper for updating the fake features
    def update_features(self, update_list):

        for index, item in enumerate(update_list):
            self.features[index] += item
            if self.features[index] < 0:
                self.features[index] = 0


    def adjust_features(self):
        new_percentage = sum(self.features)
        
        for index, customer_feature in enumerate(self.features):
            self.features[index] = customer_feature * 100 / new_percentage

    def crossover(self, other):
        new_product = Product(self.id, self.name, len(self.features))
        features = []
        for index in range(self.features):
            R = random.uniform()
            features.append(R*self.features[index] + (1-R) * other.features[index])
        new_product.features = features
        return new_product
    
    def mutate(self):
        offspring = Product(self.id, self.name, len(self.features))
        sigma = 0.8
        for index in range(len(self.features)):
            offspring.features[index] = self.features[index] + random.uniform(-1, 1) * sigma
#-------------------------------------------------------------------------
# Customer/User Struct/Class Main idea is to link datatypes
#-------------------------------------------------------------------------
class Customer:

    def __init__(self, id, num_features):
        self.id = id
        self.features = []
        for i in range(num_features):
            self.features.append(100/num_features)

    # When buying update features
    def purchase(self, product):
        product_features = product.features

        for index, customer_feature in enumerate(self.features):
            product_feature = product_features[index]
            self.features[index] += product_feature

    def adjust_features(self):
        new_percentage = sum(self.features)
        
        for index, customer_feature in enumerate(self.features):
            self.features[index] = customer_feature * 100 / new_percentage

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):

        representation = "Customer " + str(self.id) +": Features: ["
        for feature in self.features:
            representation += str(feature) + "% "

        return representation + "]"
#-------------------------------------------------------
# Manhattan Distance between feature differences.
#-------------------------------------------------------
def getSimmilarityDistance(product, customer):

    simmilarity_distance = 0
    for index, product_feature in enumerate(product.features):
        simmilarity_distance += abs(product_feature - customer.features[index])

    return simmilarity_distance
#-------------------------------------------------------        
# Output {num} recommendations for customer.
#-------------------------------------------------------
def recommend_item(user_id, products, customers, num = 1):

    customer = customers[user_id]
    customer.adjust_features()
    features = customer.features

    best_product_distance = {}
    
    for product in products:
        simmilarity = getSimmilarityDistance(product, customer)
        if len(best_product_distance) < num:
            best_product_distance[product] = simmilarity

        else:
            best_product_distance = dict(sorted(best_product_distance.items(), key=operator.itemgetter(1), reverse=True))
            for worst_current_product in best_product_distance:
                if simmilarity < best_product_distance[worst_current_product]:
                    del best_product_distance[worst_current_product]
                    best_product_distance[product] = simmilarity
                break

    return best_product_distance

#-------------------------------------------------------          
# Testing outputs the accuracy of recommendations.
#-------------------------------------------------------
def test(custormer_id, product_list, products, customers, test_data, verbose = False):

    num_items_to_recommend = 3
    items = recommend_item(custormer_id, product_list, customers, num_items_to_recommend)

    output = []
    for item in items:
        for _ in item.features:
            output.append(0)
        break

    try:
        x = products[test_data[custormer_id]]

        if verbose:
            print("Suggest", items)
            print("Actual", x)
        
    except:
        return output, 0
    
    includes = 0

    for i, item in enumerate(items):
        if item == products[test_data[custormer_id]]:
            includes = 1
        for index, feature in enumerate(item.features):
            difference = feature - products[test_data[custormer_id]].features[index]
            output[i] = (output[i] + difference)/2
    
    return output, includes

#-------------------------------------------------------
# Training Functions
#-------------------------------------------------------

def average_adjustment(product_list, products, customers, customer_wants_to_buy):
    averages = None
    recommended_correctly = 0 
    for customer in customers:
        results, didRecommendDesiredItem = test(customer, product_list, products, customers, customer_wants_to_buy)
        recommended_correctly += didRecommendDesiredItem    
        if averages is None:
            averages = results
        else:
            for index, result in enumerate(results):
                averages[index] = (result + averages[index])/2

    for product in product_list:
        product.update_features(averages)
        products[product.id] = product

    for product in product_list:
        product.adjust_features()
        products[product.id] = product
    return recommended_correctly

def genetic_search(product_list, products, customers, customer_wants_to_buy, verbose = False):
    num_generations = 100 
    fitness_old = 0
    fitness_new = 0
    for customer in customers:
        results, didRecommendDesiredItem = test(customer, product_list, products, customers, customer_wants_to_buy)
        fitness_old += didRecommendDesiredItem    
    alternative_list = []
    alternative_prod = {}
    for product in product_list:
        offspring = product.mutate()
        alternative_list.append(offspring)
        alternative_prod[product.id] = offspring

    for customer in customers:
        results, didRecommendDesiredItem = test(customer, product_list, products, customers, customer_wants_to_buy)
        fitness_new += didRecommendDesiredItem    
    
    if fitness_new > fitness_old:
        if verbose:
            print(fitness_new)
        return altenative_prod, alternative_list
    else:
        if verbose:
            print(fitness_old)
        return products, product_list


#-------------------------------------------------------
# Simulation/Training method
#-------------------------------------------------------
def simulate(num_features, df_product, df_purchase):

    products = {}
    product_list = []
    customers = {}
    for index, line in df_product.iterrows():

        id = line['product_id']
        product = Product(id, line['product'], num_features)
        product_list.append(product)
        products[id] = product

    for index, line in df_purchase.iterrows():
        id = line['user_id']
        customer = Customer(id, num_features)
        customers[id] = customer



    for i in range(100):
        costumer_id_already_purchased = []
        costumer_id_testing_data = []

        customer_wants_to_buy = {} # Testing data

        for index, line in df_purchase.iterrows():
            customer_id = line['user_id']
            customer = customers[customer_id]
            product_id = line['product_id_purchased']
            product_purchased = products[product_id]

            if customer_id not in costumer_id_already_purchased or customer_id in costumer_id_testing_data:
                costumer_id_already_purchased.append(customer_id)
                customer.purchase(product_purchased)
            else:
                costumer_id_testing_data.append(customer_id)
                customer_wants_to_buy[customer_id] = product_id
        
        generation_num = 20

        #for generation in range(generation_num):
            #products, product_list = genetic_search(product_list, products, customers, customer_wants_to_buy, generation == generation_num)
        recommended_correctly = average_adjustment(customer, product_list, products, customers, customer_wants_to_buy)
        print("Recommended Correctly: ", recommended_correctly)

    test(2, product_list, products, customers, customer_wants_to_buy, True)

class FeatureFaker:

    def __init__(self, train_df, test_df, num_features = 5):
        self.products = {}
        self.product_list = []
        self.customers = {}
        self.num_features = num_features
        self.train = train_df
        #self.test = test_df
        self.path = "recommendations_feature.csv"
        self.initialise(train_df)
        #self.initialise(test_df)

    def initialise(self, df):

        for index, line in df.iterrows():

            id = line['product_id']
            product = Product(id, "", self.num_features)
            self.product_list.append(product)
            self.products[id] = product
            id = line['user_id']
            customer = Customer(id, self.num_features)
            self.customers[id] = customer
        

    def fit(self, num_iterations):

        for i in range(num_iterations):
            
            for index, line in self.train.iterrows():

                customer_id = line['user_id']
                customer = self.customers[customer_id]
                product_id = line['product_id']
                product = self.products[product_id]

                customer.purchase(product)

    def recommend(self, customer_id, num):
        output = [customer_id]
        products = recommend_item(customer_id, self.product_list, self.customers, num = 1)
        for p in products:
            output.append(p.id)
        return output
    
    def recommend_all(self, num_recommendations):
        output_file = open(self.path, 'w', newline='')
        line = csv.writer(output_file)
        for user_id in self.customers:
            recommendations = recommend_item(user_id, self.product_list, self.customers, num_recommendations)
            output = [user_id]
            for key in recommendations:
                output.append(key)
            line.writerow(output)
        output_file.close()
        return output_file


def feature_faker_to_file(path_training_data, num_recommendations):
    interaction = read_file(path_training_data)
    
    m = FeatureFaker(interaction, test, 10)
    m.fit(1)
    m.recommend_all(num_recommendations)

#feature_faker_to_file("interactions_train", 10)













