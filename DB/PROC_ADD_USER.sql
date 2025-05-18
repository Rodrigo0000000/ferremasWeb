CREATE DEFINER=`root`@`localhost` PROCEDURE `PROC_ADD_USER`(
    IN p_nombre VARCHAR(50),
    IN p_apellido VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_password VARCHAR(50)
)
BEGIN
	INSERT INTO USERS (NOMBRE, APELLIDO, EMAIL, PASSWORD)
	VALUES (p_nombre, p_apellido, p_email, p_password);
END