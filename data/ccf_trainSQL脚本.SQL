-- 创建数据库
CREATE DATABASE IF NOT EXISTS O2O;
USE O2O;

-- 创建表
CREATE TABLE IF NOT EXISTS ccf_train (
    User_id INT NOT NULL,
    Merchant_id INT NOT NULL,
    Coupon_id INT,
    Discount_rate VARCHAR(10),
    Distance INT,
    Date_received DATE,
    Date DATE,
    PRIMARY KEY (User_id, Merchant_id, Coupon_id, Date_received)
);

-- 插入数据
LOAD DATA INFILE 'path/to/your/ccf_train.csv'
INTO TABLE ccf_train
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(User_id, Merchant_id, Coupon_id, Discount_rate, Distance, @Date_received, @Date)
SET 
    Date_received = STR_TO_DATE(@Date_received, '%Y%m%d'),
    Date = STR_TO_DATE(@Date, '%Y%m%d');
