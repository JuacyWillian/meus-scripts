CREATE TABLE "category" (
  "id" INTEGER CONSTRAINT "pk_category" PRIMARY KEY AUTOINCREMENT,
  "name" TEXT UNIQUE NOT NULL
);

CREATE TABLE "product" (
  "id" INTEGER CONSTRAINT "pk_product" PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL,
  "description" TEXT NOT NULL,
  "picture" BLOB,
  "price" DECIMAL(12, 2) NOT NULL,
  "quantity" INTEGER NOT NULL
);

CREATE TABLE "category_products" (
  "product" INTEGER NOT NULL REFERENCES "product" ("id"),
  "category" INTEGER NOT NULL REFERENCES "category" ("id"),
  CONSTRAINT "pk_category_products" PRIMARY KEY ("product", "category")
);

CREATE INDEX "idx_category_products" ON "category_products" ("category");

CREATE TABLE "user" (
  "id" INTEGER CONSTRAINT "pk_user" PRIMARY KEY AUTOINCREMENT,
  "email" TEXT UNIQUE NOT NULL,
  "password" TEXT NOT NULL,
  "classtype" TEXT NOT NULL,
  "name" TEXT,
  "country" TEXT,
  "address" TEXT
);

CREATE TABLE "cartitem" (
  "id" INTEGER CONSTRAINT "pk_cartitem" PRIMARY KEY AUTOINCREMENT,
  "quantity" INTEGER NOT NULL,
  "customer" INTEGER NOT NULL REFERENCES "user" ("id"),
  "product" INTEGER NOT NULL REFERENCES "product" ("id")
);

CREATE INDEX "idx_cartitem__customer" ON "cartitem" ("customer");

CREATE INDEX "idx_cartitem__product" ON "cartitem" ("product");

CREATE TABLE "order" (
  "id" INTEGER CONSTRAINT "pk_order" PRIMARY KEY AUTOINCREMENT,
  "state" TEXT NOT NULL,
  "date_created" DATETIME NOT NULL,
  "date_shipped" DATETIME,
  "date_delivered" DATETIME,
  "total_price" DECIMAL(12, 2) NOT NULL,
  "customer" INTEGER NOT NULL REFERENCES "user" ("id"),
  "processed_by" INTEGER REFERENCES "user" ("id")
);

CREATE INDEX "idx_order__customer" ON "order" ("customer");

CREATE INDEX "idx_order__processed_by" ON "order" ("processed_by");

CREATE TABLE "orderitem" (
  "quantity" INTEGER NOT NULL,
  "price" DECIMAL(12, 2) NOT NULL,
  "order" INTEGER NOT NULL REFERENCES "order" ("id"),
  "product" INTEGER NOT NULL REFERENCES "product" ("id"),
  CONSTRAINT "pk_orderitem" PRIMARY KEY ("order", "product")
);

CREATE INDEX "idx_orderitem__product" ON "orderitem" ("product")
