SELECT Car_Type, Price_Per_Day, Seating_Capacity
FROM car_type;
/*Functional Dependencies:
Car_Type_ID → Car_Type, Price_Per_Day, Seating_Capacity
Each car type is uniquely identified by its Car_Type_ID. The attributes Price_Per_Day and Seating_Capacity are functionally dependent on Car_Type_ID because a single Car_Type_ID value determines the car type name, price, and seating capacity.
Functional Requirement 2: Find users who have rented a car more than 3 times.*/

SELECT CU.FName, CU.LName, COUNT(*) AS Rental_Count
FROM Car_User CU
JOIN reservation R ON CU.User_ID = R.User_ID
GROUP BY CU.User_ID
HAVING Rental_Count > 3;
/*Functional Dependencies:
User_ID → FName, MName, LName, Email, License_No, Address, Phone
Each user is uniquely identified by User_ID, and their personal information is functionally dependent on it.
User_ID → COUNT(Reservations)
The total number of reservations made by a user is dependent on their User_ID. This FD is crucial for identifying users who have rented more than 3 times.
Functional Requirement 3: Calculate the total revenue generated from a specific car type.
Query:*/
SELECT CT.Car_Type, SUM(R.Tot_Amount) AS Total_Revenue
FROM car_type CT
JOIN reservation R ON CT.Car_Type_ID = R.Car_Type_ID
GROUP BY CT.Car_Type;
/*Functional Dependencies:

Car_Type_ID → Car_Type
The car type name is determined by its unique ID.
Reservation_ID → Car_Type_ID, Tot_Amount
Each reservation is uniquely identified by Reservation_ID, and the associated car type and total amount are functionally dependent on it.
Car_Type_ID → SUM(Tot_Amount)
The total revenue generated for a car type depends on the sum of all Tot_Amount values from reservations for that car type.
Functional Requirement 4: Display all reservations along with applied discounts and final amounts.
Query:*/
SELECT R.Reservation_ID, CU.FName, CU.LName, R.Tot_Amount, D.Discount_Amount, 
       (R.Tot_Amount - D.Discount_Amount) AS Final_Amount
FROM reservation R
JOIN Discount D ON R.Discount_ID = D.Discount_ID
JOIN Car_User CU ON R.User_ID = CU.User_ID;
/*Functional Dependencies:

Reservation_ID → User_ID, Tot_Amount, Discount_ID
Each reservation uniquely determines the user, total amount, and associated discount.
Discount_ID → Discount_Amount
The discount ID determines the discount amount applied.
(Tot_Amount, Discount_Amount) → Final_Amount
The final amount after applying the discount is determined by the total amount and the discount amount.
Functional Requirement 5: Show all active promo codes and their descriptions.
Query:*/
SELECT Promo_Code, Description
FROM Offer_Details
WHERE Status = 'Active';
/*Functional Dependencies:

Promo_Code → Description, Status, Is_One_Time
Each promo code is unique and determines its description, status (e.g., active/inactive), and whether it can be used only once.
Status = 'Active' → Promo_Code, Description
The condition Status = 'Active' filters only promo codes that are active, with their descriptions.*/