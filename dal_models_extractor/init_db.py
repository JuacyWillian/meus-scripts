import sqlite3
from pprint import pprint


sql_list = (
    'CREATE TABLE IF NOT EXISTS "category" ('
    '"id" INTEGER CONSTRAINT "pk_category" PRIMARY KEY AUTOINCREMENT,'
    '"name" TEXT UNIQUE NOT NULL'
    ');'
    ,
    'CREATE TABLE IF NOT EXISTS "product" ('
    '"id" INTEGER CONSTRAINT "pk_product" PRIMARY KEY AUTOINCREMENT,'
    '"name" TEXT NOT NULL,'
    '"description" TEXT NOT NULL,'
    '"picture" BLOB,'
    '"price" DECIMAL(12, 2) NOT NULL,'
    '"quantity" INTEGER NOT NULL'
    ');'
    ,
    'CREATE TABLE IF NOT EXISTS "category_products" ('
    '  "product_id" INTEGER NOT NULL REFERENCES "product" ("id"),'
    '  "category_id" INTEGER NOT NULL REFERENCES "category" ("id"),'
    '  CONSTRAINT "pk_category_products" PRIMARY KEY ("product_id", "category_id")'
    ');'
    ,
    'CREATE INDEX "idx_category_products" ON "category_products" ("category");'
    ,
    'CREATE TABLE IF NOT EXISTS "user" ('
    '  "id" INTEGER CONSTRAINT "pk_user" PRIMARY KEY AUTOINCREMENT,'
    '  "email" TEXT UNIQUE NOT NULL,'
    '  "password" TEXT NOT NULL,'
    '  "classtype" TEXT NOT NULL,'
    '  "name" TEXT,'
    '  "country" TEXT,'
    '  "address" TEXT'
    ');'
    ,
    'CREATE TABLE IF NOT EXISTS "cartitem" ('
    '  "id" INTEGER CONSTRAINT "pk_cartitem" PRIMARY KEY AUTOINCREMENT,'
    '  "quantity" INTEGER NOT NULL,'
    '  "customer" INTEGER NOT NULL REFERENCES "user" ("id"),'
    '  "product" INTEGER NOT NULL REFERENCES "product" ("id")'
    ');'
    ,
    'CREATE INDEX "idx_cartitem__customer" ON "cartitem" ("customer");'
    ,
    'CREATE INDEX "idx_cartitem__product" ON "cartitem" ("product");'
    ,
    'CREATE TABLE IF NOT EXISTS "order" ('
    '  "id" INTEGER CONSTRAINT "pk_order" PRIMARY KEY AUTOINCREMENT,'
    '  "state" TEXT NOT NULL,'
    '  "date_created" DATETIME NOT NULL,'
    '  "date_shipped" DATETIME,'
    '  "date_delivered" DATETIME,'
    '  "total_price" DECIMAL(12, 2) NOT NULL,'
    '  "customer" INTEGER NOT NULL REFERENCES "user" ("id"),'
    '  "processed_by" INTEGER REFERENCES "user" ("id")'
    ');'
    ,
    'CREATE INDEX "idx_order__customer" ON "order" ("customer");'
    ,
    'CREATE INDEX "idx_order__processed_by" ON "order" ("processed_by");'
    ,
    'CREATE TABLE IF NOT EXISTS "orderitem" ('
    '  "quantity" INTEGER NOT NULL,'
    '  "price" DECIMAL(12, 2) NOT NULL,'
    '  "order" INTEGER NOT NULL REFERENCES "order" ("id"),'
    '  "product" INTEGER NOT NULL REFERENCES "product" ("id"),'
    '  CONSTRAINT "pk_orderitem" PRIMARY KEY ("order", "product")'
    ');'
    ,
    'CREATE INDEX "idx_orderitem__product" ON "orderitem" ("product")'
)

def init_db(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    for sql in sql_list:
        try:
            cur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
    cur.close()