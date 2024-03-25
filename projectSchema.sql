CREATE SCHEMA project;
CREATE TABLE project.user (
user_id int AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(40),
last_name VARCHAR(40),
title VARCHAR(40));

CREATE TABLE project.course(
course_id int AUTO_INCREMENT PRIMARY KEY,
user_id int,
FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE SET NULL,
course_name VARCHAR(40),
subject VARCHAR(40));

CREATE TABLE project.enrollment(
enrollment_id int AUTO_INCREMENT PRIMARY KEY,
user_id int,
FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE SET NULL,
course_id int,
FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE SET NULL,
progress VARCHAR(20));

CREATE TABLE project.compensation(
compensation_id int AUTO_INCREMENT PRIMARY KEY,
user_id int,
FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE SET NULL,
course_id int,
FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE SET NULL,
compensation_amount DECIMAL(10,2));
