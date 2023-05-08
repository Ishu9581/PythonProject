import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="Ishu@80742683",database = "Inventory_Management")
cur=mydb.cursor()
manufacture_table='create table manufacture(manufacture_id integer(5) primary key,manufacture_date date,item_name varchar(30),no_of_items integer(5),defective_items integer(5),item_color varchar(20),company varchar(30))'
goods_table="create table goods(goods_id integer(5) primary key,manufacture_id integer(5),item_name varchar(30),item_color varchar(20),item_price integer(5),manufactured_date date)"
purchase_table='create table purchase (purchase_id integer(5) primary key,goods_id integer(5),purchase_date date,purchase_amount integer(5),purchase_store varchar(50))'
sales_table='create table sales(sale_id integer(5) primary key,goods_id integer(5),sale_date date,sale_amount integer(5),sale_store varchar(50),profit_margin integer(5))'
cur.execute(manufacture_table)
cur.execute(goods_table)
cur.execute(purchase_table)
cur.execute(sales_table)
t1='insert into manufacture(manufacture_id,manufacture_date,item_name,no_of_items,defective_items,item_color,company) values(%s,%s,%s,%s,%s,%s,%s)'
a=[ (1, '2023-04-01', 'Shirt', 1000, 30,'Red','SS Exports'),
    (2, '2023-04-02', 'Toy Car', 600, 20,'Red','VR Exports'),
    (3, '2023-04-01', 'Toy Car',  850, 35,'Yellow','RR Exports'),
    (4, '2023-04-02', 'Wooden Chair', 200, 15,'Orange','SS Exports'),
    (5, '2023-04-03', 'Wooden Table', 150, 12,'White','SS Exports'),
    (6,'2023-04-04','Bottle',1500,40,'Black','RR Exports')]
cur.executemany(t1,a)
print("manufacture inserted successfully")
t2='insert into goods(goods_id,manufacture_id,item_name,item_color,item_price,manufactured_date) values(%s,%s,%s,%s,%s,%s)'
b=[(1, 1, 'Shirt', 'Red', 150, '2023-04-01'),
   (2, 2, 'Toy Car', 'Red', 200, '2023-04-02'),
   (3, 3, 'Toy Car', 'Yellow', 200, '2023-04-01'),
   (4, 4, 'Wooden Chair', 'Orange', 300, '2023-04-02'),  
   (5, 5, 'Wooden Table', 'White', 300, '2023-04-03'),
   (6,6,'Bottle','Black',100,'2023-04-04')]
cur.executemany(t2,b)
print("Goods inserted successfully")
t3='insert into purchase(purchase_id,goods_id,purchase_date,purchase_amount,purchase_store) values(%s,%s,%s,%s,%s)'
c=[ (1, 1, '2023-04-06', 26500, 'ORay'),
   (2, 2, '2023-04-07', 5600, 'MyKids'),
   (3, 3, '2023-04-08', 13050, 'LuckyStores'),
   (4, 4, '2023-04-09', 6500, 'V-mart'),
   (5, 5, '2023-04-10', 4750, 'MyCare')]
cur.executemany(t3,c)
print("purchase inserted successfully")
t4='insert into sales(sale_id,goods_id,sale_date,sale_amount,sale_store,profit_margin) values(%s,%s,%s,%s,%s,%s)'
d=[ (1, 1, '2023-04-16', 30000, 'MyCare', 5000),
(2, 2, '2023-04-17', 9000, 'MyKids', 1500),
(3, 3, '2023-04-18', 13500, 'LuckyStores', 2250),
(4, 4, '2023-04-19', 6000, 'V-mart', 1000),
(5, 5, '2023-04-20', 4500, 'MyCare',750)]
cur.executemany(t4,d)
print("Sales inserted successfully")
mydb.commit()
        
#Delete the defective item, e.g., the shirt which was accidentally purchased by the “ORay” store, manufactured on the date ‘01-04-23’.
dele='DELETE FROM goods WHERE goods.goods_id in(SELECT goods_id from(SELECT goods.goods_id FROM goods JOIN manufacture ON goods.manufacture_id = manufacture.manufacture_id JOIN purchase ON goods.goods_id = purchase.goods_id WHERE goods.item_name = "Shirt" AND purchase.purchase_store = "ORay" AND manufacture.manufacture_date = "2023-04-01" AND manufacture.defective_items >0 limit 1)as c)'
cur.execute(dele)
print("Deleted successfully")
mydb.commit()
#Update the manufacture details of all the red-colored toys which are purchased by the “MyKids” store.
upd="UPDATE manufacture m JOIN goods g ON m.manufacture_id = g.manufacture_id JOIN purchase p ON g.goods_id = p.goods_id SET m.no_of_items = m.no_of_items + p.purchase_amount, m.defective_items = m.defective_items + (p.purchase_amount * 0.05) WHERE g.item_name = 'Toy Car' AND g.item_color = 'Red' AND p.purchase_store='MyKids'"
cur.execute(upd)
print("Updated successfully")
mydb.commit()
#Display all the “wooden chair” items that were manufactured before the 1st May 2023. 
dis="SELECT * FROM goods WHERE item_name = 'Wooden Chair' AND manufactured_date < '2023-05-01'"
cur.execute(dis)
print("Displayed Successfully")
my_result=cur.fetchall()
for x in my_result:
    print(x)
mydb.commit()
# Display the profit margin amount of the “wooden table” that was sold by the “MyCare” store, manufactured by the “SS Export” company.

cur.execute("SELECT profit_margin FROM sales,goods, manufacture WHERE goods.goods_id = sales.goods_id AND goods.item_name = 'wooden table' AND manufacture.company = 'SS Export' AND sales.sale_store = 'MyCare'")
print("Profit margin displayed successfully")
my_result2=cur.fetchall()
for i in my_result2:
    print(i)
mydb.commit()
