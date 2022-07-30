create database RISESHINE;
use RISESHINE;

/*Portfolio - ID (auto-increment primary key), name (varchar 55), create stamp, last update stamp*/
CREATE TABLE Portfolio (
    PortfolioID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(55) NOT NULL,
    StartDate timestamp default current_timestamp,
    Value decimal(10,2) default 0,
    LastUpdate timestamp default null on update current_timestamp,
    PRIMARY KEY (PortfolioID)
);

insert into portfolio (name) values('all');
select * from portfolio;

/*Hold - Ticker (Max 5 chars) volume (positive integer), portfolio ID (foreign key)*/
CREATE TABLE Hold (
	Ticker VARCHAR(5) NOT NULL,
    Volume INT NOT NULL,
    PortfolioID INT NOT NULL,
    FOREIGN KEY (PortfolioID) REFERENCES PORTFOLIO (PortfolioID),
    CONSTRAINT test_volume_positive CHECK (Volume >= 0)
    );

/* remove tickers with 0 volume */    
CREATE TRIGGER ticker_remove
    AFTER UPDATE 
    ON Hold FOR EACH ROW
    DELETE FROM HOLD WHERE Volume=0;
    
/* Value - portfolio ID (foreign key), date, value (float, round 0.2), calculated % difference against previous day (round 0.2) */
CREATE TABLE Value (
	PortfolioID INT NOT NULL,
    Date date NOT NULL,
    Value decimal(10,2) NOT NULL,
    Difference decimal(10,4) NOT NULL,
    FOREIGN KEY (PortfolioID) REFERENCES PORTFOLIO (PortfolioID)
    );

insert into value values (1,'2022-07-28',123.58,0),(1,'2022-07-29',123.58,0);
select * from value WHERE PORTFOLIOID=1 AND DATE=DATE_SUB(CURDATE(), INTERVAL 1 DAY);



/* function to find the last value */
DELIMITER $$
CREATE FUNCTION LastValue (Portfolio int, NewDate date) returns decimal(10,2)
deterministic
BEGIN
	DECLARE LastValue decimal(10,4);
    SET LastValue = (select Value from value WHERE PortfolioID=Portfolio AND DATE=DATE_SUB(NewDate, INTERVAL 1 DAY));
    IF LastValue is null then set LastValue = 0;
    end if;
RETURN LastValue;
END$$
DELIMITER ;

select Value from value WHERE PortfolioID=1 AND DATE=DATE_SUB('2022-07-30', INTERVAL 1 DAY);
select LastValue(1,'2022-07-25');

/* trigger to get Difference for new day */
DELIMITER $$
CREATE TRIGGER insert_new_value 
	BEFORE INSERT 
    ON Value FOR EACH ROW
    IF LastValue(new.PortfolioID, new.Date)=0 THEN SET new.Difference=0;
    ELSE SET new.Difference=(new.Value/LastValue(new.PortfolioID, new.Date))-1;
    END IF;    
END$$
DELIMITER ;

insert into value values (1,'2022-07-30',150,0),(1,'2022-07-15',123.58,0);
SELECT * FROM VALUE;

/* trigger to update value and difference for the same day */
DELIMITER $$
CREATE TRIGGER update_new_value 
	BEFORE UPDATE 
    ON Value FOR EACH ROW
    IF LastValue(old.PortfolioID, old.Date)=0 THEN SET new.Difference=0;
    ELSE SET new.Difference=(new.Value/LastValue(old.PortfolioID, old.Date))-1;
    END IF;    
END$$
DELIMITER ;

UPDATE VALUE SET VALUE=50 WHERE DATE='2022-07-30';
SELECT * FROM VALUE;


/* Wallet - description (varchar 255), value (float), first line wallet itself, below log of transactions
wallet - amount, date (auto update stamp), description */
CREATE TABLE Wallet (
	CurrentWallet decimal(10,2) NOT NULL,
    ValueChange decimal(10,2) NOT NULL,
    Date timestamp default current_timestamp,
    Description VARCHAR(255) NOT NULL
    );

CREATE TRIGGER no_amend
	BEFORE UPDATE ON Wallet FOR EACH ROW
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'records cannot be amended or deleted';

CREATE TRIGGER no_delete
	BEFORE DELETE ON Wallet FOR EACH ROW
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'records cannot be amended or deleted';
    
INSERT INTO Wallet (CurrentWallet, ValueChange, Description)
VALUES (0.00, 0.00, 'Start of the wallet');