drop table accessories;
drop table bags;
drop table beauty;
drop table house;
drop table jewelry;
drop table kids;
drop table men;
drop table shoes;
drop table women;

CREATE TABLE IF NOT EXISTS accessories (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT a PRIMARY KEY (id)
);

\copy accessories from '~/Desktop/sem/dbms/newdata/accessories.csv' delimiter ',' csv header;   

CREATE TABLE IF NOT EXISTS bags (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT b PRIMARY KEY (id)
);

\copy bags from '~/Desktop/sem/dbms/newdata/bags.csv' delimiter ',' csv header;   

CREATE TABLE IF NOT EXISTS beauty (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT c PRIMARY KEY (id)
);

\copy beauty from '~/Desktop/sem/dbms/newdata/beauty.csv' delimiter ',' csv header;   

CREATE TABLE IF NOT EXISTS house (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT d PRIMARY KEY (id)
);

\copy house from '~/Desktop/sem/dbms/newdata/house.csv' delimiter ',' csv header;   

CREATE TABLE IF NOT EXISTS jewelry (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT e PRIMARY KEY (id)
);

\copy jewelry from '~/Desktop/sem/dbms/newdata/jewelry.csv' delimiter ',' csv header;   

CREATE TABLE IF NOT EXISTS kids (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT f PRIMARY KEY (id)
);

\copy kids from '~/Desktop/sem/dbms/newdata/kids.csv' delimiter ',' csv header;   

CREATE TABLE IF NOT EXISTS men (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT m PRIMARY KEY (id)
);

\copy men from '~/Desktop/sem/dbms/newdata/men.csv' delimiter ',' csv header;   

CREATE TABLE IF NOT EXISTS shoes (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT s PRIMARY KEY (id)
);

\copy shoes from '~/Desktop/sem/dbms/newdata/shoes.csv' delimiter ',' csv header;   

CREATE TABLE IF NOT EXISTS women (
    category text ,
    subcategory text ,
    name text,
    current_price decimal,
    raw_price decimal,
    currency text,
    discount bigint,
    likes_count bigint, 
    is_new boolean,
    brand text,
    brand_url text,
    codcountry text,
    variation_0_color text,
    variation_1_color text,
    variation_0_thumbnail text,
    variation_0_image text,
    variation_1_thumbnail text,
    variation_1_image text,
    image_url text,
    url text,
    id text,
    model text,
    quantity bigint,
    CONSTRAINT w PRIMARY KEY (id)
);

\copy women from '~/Desktop/sem/dbms/newdata/women.csv' delimiter ',' csv header;   

