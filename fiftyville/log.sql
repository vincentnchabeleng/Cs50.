-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Retrieve description from crime_scene_reports table for a specific date
SELECT description
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28;

-- Retrieve interview transcripts mentioning "bakery" for a specific date
SELECT transcript
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28
AND transcript LIKE "%bakery%";

-- Retrieve bakery security logs activity, license plate, and person name for a specific date and time range
SELECT bakery_security_logs.activity, bakery_security_logs.license_plate, people.name
FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2023
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25;

-- Retrieve person name and ATM transaction type for withdrawals at a specific ATM location on a specific date
SELECT people.name, atm_transactions.transaction_type
FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2023
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw";

-- Update caller_name in phone_calls table based on matching phone numbers in the people table
UPDATE phone_calls
SET caller_name = (
    SELECT name FROM people WHERE phone_calls.caller = people.phone_number
);

-- Update receiver_name in phone_calls table based on matching phone numbers in the people table
UPDATE phone_calls
SET receiver_name = (
    SELECT name FROM people WHERE phone_calls.receiver = people.phone_number
);

-- Retrieve phone calls made or received on a specific date with a duration of less than 60 seconds
SELECT caller, caller_name, receiver, receiver_name
FROM phone_calls
WHERE year = 2023
AND month = 7
AND day = 28
AND duration < 60;

-- Retrieve the ID, hour, minute, origin airport, and destination airport of the first flight on a specific date
SELECT f.id, f.hour, f.minute, a_origin.city AS origin_city, a_destination.city AS destination_city
FROM flights f
JOIN airports a_origin ON f.origin_airport_id = a_origin.id
JOIN airports a_destination ON f.destination_airport_id = a_destination.id
WHERE f.year = 2023
AND f.month = 7
AND f.day = 29
ORDER BY f.hour ASC
LIMIT 1;

-- Retrieve destination airport, person name, phone number, and license plate of passengers on a specific flight
SELECT a_destination.city AS destination_city, p.name, p.phone_number, p.license_plate
FROM people p
JOIN passengers pa ON p.passport_number = pa.passport_number
JOIN flights f ON f.id = pa.flight_id
JOIN airports a_destination ON f.destination_airport_id = a_destination.id
WHERE f.id = 36
ORDER BY f.hour ASC;

-- Retrieve the city of an airport with a specific ID
SELECT city FROM airports
WHERE id = 4;

-- Retrieve person name who meets specific criteria related to phone calls, ATM transactions, and bakery security logs, and who was a passenger on a specific flight
SELECT p.name
FROM people p
JOIN passengers pa ON p.passport_number = pa.passport_number
JOIN flights f ON f.id = pa.flight_id
WHERE
(f.year = 2023 AND f.month = 7 AND f.day = 29 AND f.id = 36)
AND p.name IN
(SELECT pc.caller_name FROM phone_calls pc
WHERE pc.year = 2023
AND pc.month = 7
AND pc.day = 28
AND pc.duration < 60)
AND p.name IN
(SELECT people.name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2023
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw")
AND p.name IN
(SELECT people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2023
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25);
