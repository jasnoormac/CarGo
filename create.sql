CREATE TABLE `car_type` (
  `Car_Type_ID` int NOT NULL AUTO_INCREMENT,
  `Car_Type` varchar(50) DEFAULT NULL,
  `Price_Per_Day` decimal(10,2) DEFAULT NULL,
  `Seating_Capacity` int DEFAULT NULL,
  PRIMARY KEY (`Car_Type_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=889 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Car_User` (
  `User_ID` int NOT NULL AUTO_INCREMENT,
  `FName` varchar(50) DEFAULT NULL,
  `MName` varchar(50) DEFAULT NULL,
  `LName` varchar(50) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `License_No` varchar(20) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`User_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Discount` (
  `Discount_ID` int NOT NULL AUTO_INCREMENT,
  `Promo_Code` varchar(10) DEFAULT NULL,
  `Percentage` decimal(5,2) DEFAULT NULL,
  `Discount_Amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Discount_ID`),
  KEY `Promo_Code` (`Promo_Code`),
  CONSTRAINT `discount_ibfk_1` FOREIGN KEY (`Promo_Code`) REFERENCES `Offer_Details` (`Promo_Code`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `insurance` (
  `Insurance_ID` int NOT NULL AUTO_INCREMENT,
  `Insurance_Type` varchar(50) DEFAULT NULL,
  `Collision_Coverage` decimal(10,2) DEFAULT NULL,
  `Car_Coverage` decimal(10,2) DEFAULT NULL,
  `Medical_Coverage` decimal(10,2) DEFAULT NULL,
  `Insurance_Price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Insurance_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Insurance_Coverage` (
  `Car_Type_ID` int NOT NULL,
  `Insurance_ID` int NOT NULL,
  PRIMARY KEY (`Car_Type_ID`,`Insurance_ID`),
  KEY `Insurance_ID` (`Insurance_ID`),
  CONSTRAINT `insurance_coverage_ibfk_1` FOREIGN KEY (`Car_Type_ID`) REFERENCES `Car_Type` (`Car_Type_ID`),
  CONSTRAINT `insurance_coverage_ibfk_2` FOREIGN KEY (`Insurance_ID`) REFERENCES `Insurance` (`Insurance_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `login` (
  `admin_id` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Offer_Details` (
  `Promo_Code` varchar(10) NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Status` varchar(50) DEFAULT NULL,
  `Is_One_Time` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Promo_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Payment` (
  `Payment_ID` int NOT NULL AUTO_INCREMENT,
  `Card_No` varchar(16) DEFAULT NULL,
  `Name_On_Card` varchar(50) DEFAULT NULL,
  `Expiry_Date` date DEFAULT NULL,
  `CVV` int DEFAULT NULL,
  `Billing_Address` varchar(255) DEFAULT NULL,
  `Amount_Paid` decimal(10,2) DEFAULT NULL,
  `Paid_By_Cash` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Payment_ID`),
  KEY `Card_No` (`Card_No`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`Card_No`) REFERENCES `Card_Details` (`Card_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Rental_Location` (
  `Rental_Location_ID` int NOT NULL AUTO_INCREMENT,
  `Phone` varchar(15) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Street_Name` varchar(100) DEFAULT NULL,
  `State` varchar(50) DEFAULT NULL,
  `Zip_Code` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Rental_Location_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `reservation` (
  `Reservation_ID` int NOT NULL AUTO_INCREMENT,
  `User_ID` int DEFAULT NULL,
  `Rental_Location_ID` int DEFAULT NULL,
  `Tot_Amount` decimal(10,2) DEFAULT NULL,
  `Insurance_Amount` decimal(10,2) DEFAULT NULL,
  `Status` varchar(50) DEFAULT NULL,
  `Accessory_ID` int DEFAULT NULL,
  `Insurance_ID` int DEFAULT NULL,
  `Discount_ID` int DEFAULT NULL,
  `Car_Type_ID` int DEFAULT NULL,
  `Payment_ID` int DEFAULT NULL,
  PRIMARY KEY (`Reservation_ID`),
  KEY `User_ID` (`User_ID`),
  KEY `Rental_Location_ID` (`Rental_Location_ID`),
  KEY `Accessory_ID` (`Accessory_ID`),
  KEY `Insurance_ID` (`Insurance_ID`),
  KEY `Discount_ID` (`Discount_ID`),
  KEY `Car_Type_ID` (`Car_Type_ID`),
  KEY `fk_payment_id` (`Payment_ID`),
  CONSTRAINT `fk_payment_id` FOREIGN KEY (`Payment_ID`) REFERENCES `payment` (`Payment_ID`),
  CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `Car_User` (`User_ID`),
  CONSTRAINT `reservation_ibfk_3` FOREIGN KEY (`Rental_Location_ID`) REFERENCES `Rental_Location` (`Rental_Location_ID`),
  CONSTRAINT `reservation_ibfk_4` FOREIGN KEY (`Accessory_ID`) REFERENCES `Accessories` (`Accessory_ID`),
  CONSTRAINT `reservation_ibfk_5` FOREIGN KEY (`Insurance_ID`) REFERENCES `Insurance` (`Insurance_ID`),
  CONSTRAINT `reservation_ibfk_6` FOREIGN KEY (`Discount_ID`) REFERENCES `Discount` (`Discount_ID`),
  CONSTRAINT `reservation_ibfk_7` FOREIGN KEY (`Car_Type_ID`) REFERENCES `Car_Type` (`Car_Type_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Vehicle_Details` (
  `VIN` varchar(17) NOT NULL,
  `Reg_No` varchar(20) DEFAULT NULL,
  `Model` varchar(50) DEFAULT NULL,
  `Year` int DEFAULT NULL,
  `Color` varchar(30) DEFAULT NULL,
  `Disable_Friendly` varchar(30) DEFAULT NULL,
  `Car_Type_ID` int DEFAULT NULL,
  PRIMARY KEY (`VIN`),
  KEY `Car_Type_ID` (`Car_Type_ID`),
  CONSTRAINT `vehicle_details_ibfk_1` FOREIGN KEY (`Car_Type_ID`) REFERENCES `Car_Type` (`Car_Type_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Accessories` (
  `Accessory_ID` int NOT NULL AUTO_INCREMENT,
  `Type` varchar(50) DEFAULT NULL,
  `Amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Accessory_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
;
