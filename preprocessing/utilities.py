# Importing Required Libraries
import pandas as pd
from preprocessing.Connection import DBConnect

class Preprocess:
    def load_data(path):
        customer = pd.read_excel(path,sheet_name="CustomerDetail")
        orders = pd.read_excel(path,sheet_name="Jan")   
        return customer,orders        

    def data_cleaning(path):
        customer,orders = Preprocess.load_data(path)
        # Customer Dataset Cleaning
        customer = customer.drop(columns=['CustomerID','Month','MonthName','DateInText','Gender.1','Gender'])
        customer = customer.rename(columns={'CustomerID.1':'CustomerID','Gender.2':'Gender'})
        customer = customer.dropna()
        customer['Order Date'] = pd.to_datetime(customer['Order Date'])
        # Orders Dataset Cleaning
        orders = orders.rename(columns={'Quantity ordered new':'Qty'})
        orders = orders.dropna()
        customer.to_csv("dataset/customer.csv" , index=None)
        orders.to_csv("dataset/orders.csv" , index=None)
        return customer,orders
    
    def save_to_database(path):
        conn = DBConnect.getConnection()
        cur = conn.cursor()
        customer,orders = Preprocess.data_cleaning(path)
        for i in range(0,customer.shape[0]):
            cus = list(customer.loc[i]) 
            sql = "insert into customer value(%s,%s,%s,%s,%s,%s)"
            data = (int(cus[0]),cus[2],cus[3],cus[4],cus[5],cus[1])
            cur.execute(sql,data)
        for i in range(0,orders.shape[0]):
            ord = list(orders.loc[i]) 
            sql = "insert into orders value(%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (int(ord[0]),int(ord[1]),float(ord[2]),float(ord[3]),int(ord[4]),ord[5],ord[6],ord[7])
            cur.execute(sql,data)
        conn.commit()
        cur.close()
        conn.close()
        