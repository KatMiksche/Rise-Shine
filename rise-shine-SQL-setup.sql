create database RISESHINE;
use RISESHINE;

/*Portfolio - ID (auto-increment primary key), name (varchar 55), create stamp, last update stamp*/
CREATE TABLE Portfolio (
    PortfolioID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(55) NOT NULL,
    StartDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Value DECIMAL(12 , 4 ) DEFAULT 0,
    LastUpdate TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (PortfolioID)
);

/*Trigger to insert initial record to historic records of values after creating new portfolio*/
CREATE TRIGGER add_historic_value
	AFTER INSERT
    ON Portfolio FOR EACH ROW
    insert into value (portfolioid, date, value) values (new.portfolioID,DATE_SUB(curdate(), INTERVAL 1 DAY),0);

/*Hold - Ticker (Max 5 chars) volume (positive integer), portfolio ID (foreign key)*/
CREATE TABLE Hold (
	Ticker VARCHAR(5) NOT NULL,
    Volume INT NOT NULL,
    PortfolioID INT NOT NULL,
    Value DECIMAL(10 , 4 ) DEFAULT 0,
    LastUpdate TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (PortfolioID) REFERENCES PORTFOLIO (PortfolioID),
    CONSTRAINT test_volume_positive CHECK (Volume >= 0)
    );
    
/* Value - portfolio ID (foreign key), date, value (float, round 0.2), calculated % difference against previous day (round 0.2) */
CREATE TABLE Value (
	PortfolioID INT NOT NULL,
    Date date NOT NULL,
    Value decimal(12,4) NOT NULL,
    Difference decimal(10,4) NOT NULL,
    FOREIGN KEY (PortfolioID) REFERENCES PORTFOLIO (PortfolioID)
    );

/* function to find the last value */
DELIMITER $$
CREATE FUNCTION LastValue (Portfolio int, NewDate date) returns decimal(10,2)
deterministic
BEGIN
	DECLARE LastValue decimal(10,4);
    SET LastValue = (select Value from value WHERE PortfolioID=Portfolio AND DATE=(select max(date) from value where PortfolioID=Portfolio));
    IF LastValue is null then set LastValue = 0;
    end if;
RETURN LastValue;
END$$
DELIMITER ;

/* trigger to get Difference for new day */
DELIMITER $$
CREATE TRIGGER insert_new_value 
	BEFORE INSERT 
    ON Value FOR EACH ROW
    BEGIN
    IF LastValue(new.PortfolioID, new.Date)=0 THEN SET new.Difference=0;
    ELSE SET new.Difference=(new.Value/LastValue(new.PortfolioID, new.Date))-1;
    END IF;    
END$$
DELIMITER ;

/* trigger to update value and difference for the same day */
DELIMITER $$
CREATE TRIGGER update_new_value 
	BEFORE UPDATE 
    ON Value FOR EACH ROW
    BEGIN
    IF LastValue(old.PortfolioID, old.Date)=0 THEN SET new.Difference=0;
    ELSE SET new.Difference=(new.Value/LastValue(old.PortfolioID, old.Date))-1;
    END IF;    
END$$
DELIMITER ;

/* Wallet - description (varchar 255), value (float), first line wallet itself, below log of transactions
wallet - amount, date (auto update stamp), description */
CREATE TABLE Wallet (
	CurrentWallet decimal(10,2) NOT NULL,
    ValueChange decimal(10,2) NOT NULL,
    Date timestamp default current_timestamp,
    Description VARCHAR(255) NOT NULL
    );

/*triggers to protect records in wallet*/
CREATE TRIGGER no_amend
	BEFORE UPDATE ON Wallet FOR EACH ROW
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'records cannot be amended or deleted';

CREATE TRIGGER no_delete
	BEFORE DELETE ON Wallet FOR EACH ROW
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'records cannot be amended or deleted';
    
INSERT INTO Wallet (CurrentWallet, ValueChange, Description)
VALUES (0.00, 0.00, 'Start of the wallet');