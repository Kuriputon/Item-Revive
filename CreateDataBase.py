import sqlite3

# connection = sqlite3.connect("users.db")
# cursor = connection.cursor()
#
# cursor.execute('''
# CREATE TABLE users (
#     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL,
#     contact_info TEXT,
#     registration_time DATETIME DEFAULT (datetime('now'))
# );
# ''')
#
# connection.close()


connection2 = sqlite3.connect("databases/items.db")
cursor2 = connection2.cursor()

# cursor2.execute('''
# CREATE TABLE items (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     category TEXT NOT NULL CHECK(category IN ('#书籍', '#数码', '#居家', '#食品', '#衣饰', '#鞋包','#运动', '#文具', '#周边', '#其他')),               -- 物品分类
#     description TEXT,
#     image_path TEXT,
#     upload_time DATETIME DEFAULT (datetime('now')),
#     uploaded_by TEXT NOT NULL,
#     price DECIMAL(10, 2),
#     status TEXT NOT NULL CHECK(status IN ('闲置中', '求物中', '已出', '已得')),                  -- 物品状态，闲置中、求物中、已出、已得
#     FOREIGN KEY (uploaded_by) REFERENCES users(username)
# );
# ''')

cursor2.execute('''
CREATE TABLE items_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                   
    category TEXT NOT NULL CHECK(category IN ('#书籍', '#数码', '#居家', '#食品', '#衣饰', '#鞋包','#运动', '#文具', '#周边', '#其他')),
    description TEXT,                     
    image_path TEXT DEFAULT NULL,
    upload_time DATETIME DEFAULT (datetime('now')),  
    uploaded_by TEXT NOT NULL,               
    price DECIMAL(10, 2),                 
    status TEXT NOT NULL CHECK(status IN ('闲置中', '求物中', '已出', '已得')),
    FOREIGN KEY (uploaded_by) REFERENCES users(username)  
);
''')


cursor2.execute('''
INSERT INTO items_new (id, name, category, description, image_path, upload_time, uploaded_by, price, status)
SELECT id, name, category, description, image_path, upload_time, uploaded_by, price, status
FROM items;
''')

cursor2.execute('DROP TABLE items;')

cursor2.execute('ALTER TABLE items_new RENAME TO items;')

connection2.close()