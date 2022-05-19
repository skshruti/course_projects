CREATE TABLE IF NOT EXISTS train_info (
    train_no bigint ,
    train_name text,
    distance bigint,
    source_station_name  text,
    departure_time time,
    day_of_departure  text,
    destination_station_name  text,
    arrival_time  time,
    day_of_arrival  text,
    CONSTRAINT train_no PRIMARY KEY (train_no)
);

--PROJECT WORK

CREATE TABLE IF NOT EXISTS users (
    userid text ,
    username text ,
    password text,
    emailid text,
    mobile bigint,
    wallet  bigint,
    CONSTRAINT userid PRIMARY KEY (userid)
);

INSERT INTO users 
VALUES ('skshruti', 'Shruti', 'abc', 'skshruti084@gmail.com', '9354249345', 500);


CREATE TABLE IF NOT EXISTS addresses (
    userid text ,
    addressname text ,
    address text,
    CONSTRAINT address PRIMARY KEY (userid, addressname)
);

INSERT INTO addresses 
VALUES ('skshruti', 'Home', 'abc');

INSERT INTO addresses 
VALUES ('pla', 'Office', 'pqr');

INSERT INTO addresses 
VALUES ('skshruti', 'work', 'acf');

CREATE TABLE IF NOT EXISTS cart (
    userid text ,
    category text ,
    itemid text,
    quantity bigint,
    CONSTRAINT cartkey PRIMARY KEY (userid, itemid)
);
INSERT INTO cart 
VALUES ('pla', 'accessories', '1671872', 5);

INSERT INTO cart 
VALUES ('skshruti', 'accessories', '1671872', 5);

INSERT INTO cart 
VALUES ('skshruti', 'bags', '1704506', 2);


CREATE TABLE IF NOT EXISTS accessory_temp (
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
    CONSTRAINT accessoryt PRIMARY KEY (id)
);

INSERT INTO accessory_temp 
VALUES ('accessories', 'Chapeaux & Bonnets', 'Masques disolation de protection du visage Masques anti-buée anti-éclaboussures', 9.99, 16.99, 'USD', 41, 373, false, '' ,'' ,'ID,MY,PH,SG,TH,VN', 'Gray', 'Blue', 'https://imgaz1.chiccdn.com/thumb/list_grid/oaupload/newchic/images/09/FD/e8204e98-8e30-41ca-a599-c8ed90469e08.jpg', 'https://imgaz1.chiccdn.com/thumb/view/oaupload/newchic/images/09/FD/e8204e98-8e30-41ca-a599-c8ed90469e08.jpg', 'https://imgaz1.chiccdn.com/thumb/list_grid/oaupload/newchic/images/2E/72/1c322075-7a7a-474d-976e-6bcbc45daaec.jpg', 'https://imgaz1.chiccdn.com/thumb/view/oaupload/newchic/images/2E/72/1c322075-7a7a-474d-976e-6bcbc45daaec.jpg', 'https://imgaz1.chiccdn.com/thumb/view/oaupload/newchic/images/2E/72/1c322075-7a7a-474d-976e-6bcbc45daaec.jpg', 'https://fr.newchic.com/hats-and-caps-4192/p-1671872.html', 1671872, 'SKUF08305');

CREATE TABLE IF NOT EXISTS bag_temp (
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
    CONSTRAINT bagt PRIMARY KEY (id)
);

INSERT INTO bag_temp 
VALUES ('bags', 'Portefeuilles', 'Gaine multi-outils en cuir véritable EDC ceinture boucle taille', 22.99, 45, 'USD', 49, 174, false,'','', 'ID,MY,PH,SG,TH,VN', 'Noir', 'café', 'https://imgaz1.chiccdn.com/thumb/list_grid/oaupload/newchic/images/40/E1/ad8b6f95-a182-4b6c-9fbe-e5f9c8dba4e5.jpg','https://imgaz1.chiccdn.com/thumb/view/oaupload/newchic/images/40/E1/ad8b6f95-a182-4b6c-9fbe-e5f9c8dba4e5.jpg','https://imgaz1.chiccdn.com/thumb/list_grid/oaupload/newchic/images/90/D7/f0c21c5f-22de-4443-8576-9be533a9532c.jpg','https://imgaz1.chiccdn.com/thumb/view/oaupload/newchic/images/90/D7/f0c21c5f-22de-4443-8576-9be533a9532c.jpg','https://imgaz1.chiccdn.com/thumb/view/oaupload/newchic/images/6F/BD/6d143095-4942-4ec1-b4ca-c73522f5e3a1.jpg','https://fr.newchic.com/chic-wallet-3614/p-1704506.html', 1704506, 'SKUF57496');


with acc as (select image_url,name,raw_price, discount, quantity, current_price*quantity as subtotal,itemid, subcategory, userid from cart, accessory_temp where accessory_temp.id=cart.itemid and userid='skshruti'),
bag as (select image_url,name,raw_price, discount, quantity, current_price*quantity as subtotal,itemid, subcategory, userid as total from cart, bag_temp where bag_temp.id=cart.itemid and userid='skshruti'),
alltables as (select * from acc union (select * from bag))
select image_url,name,raw_price, discount, quantity, subtotal, sum(subtotal) over (partition by userid) as total, itemid, subcategory from alltables;

CREATE TABLE IF NOT EXISTS orders (
    userid text ,
    itemid text 
);

with acc as (select image_url,name,raw_price, discount, quantity, current_price*quantity as subtotal,itemid, subcategory, userid from orders, accessory_temp where accessory_temp.id=orders.itemid and userid='skshruti'), 
bag as (select image_url,name,raw_price, discount, quantity, current_price*quantity as subtotal,itemid, subcategory, userid as total from orders, bag_temp where bag_temp.id=orders.itemid and userid='skshruti'), 
alltables as (select * from acc union (select * from bag)) 
select * from alltables
select image_url,name,raw_price, discount, quantity, subtotal, sum(subtotal) over (partition by userid) as total, itemid, subcategory from alltables;



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
    CONSTRAINT woment PRIMARY KEY (id)
);

\copy women from '~/Desktop/sem/dbms/data/women.csv' delimiter ',' csv header;   