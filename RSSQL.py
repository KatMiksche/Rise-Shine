import mysql.connector as connector

def connection():
  config = {
    "user": "python",
    "password": "python",
    "host": "localhost",
  }
  conn = connector.connect(**config)
  return conn


if __name__ == "__main__":
  con=connection()
  con.autocommit=True
  mycursor = con.cursor()

  mycursor.execute("""
  create database RISESHINE;
  use RISESHINE;
  
  /*Portfolio - ID (auto-increment primary key), name (varchar 55), create stamp, last update stamp*/
  CREATE TABLE Portfolio (
      PortfolioID INT NOT NULL AUTO_INCREMENT,
      Name VARCHAR(55) NOT NULL,
      StartDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      Value DECIMAL(10 , 2 ) DEFAULT 0,
      LastUpdate TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (PortfolioID)
  );
  
  /*Hold - Ticker (Max 5 chars) volume (positive integer), portfolio ID (foreign key)*/
  CREATE TABLE Hold (
      Ticker VARCHAR(7) NOT NULL,
      Volume INT NOT NULL,
      PortfolioID INT NOT NULL,
      Value DECIMAL(10 , 2 ) DEFAULT 0,
      LastUpdate TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
      FOREIGN KEY (PortfolioID) REFERENCES PORTFOLIO (PortfolioID),
      CONSTRAINT test_volume_positive CHECK (Volume >= 0)
      );
      
  /* Value - portfolio ID (foreign key), date, value (float, round 0.2), calculated % difference against previous day (round 0.2) */
  CREATE TABLE Value (
      PortfolioID INT NOT NULL,
      Date date NOT NULL,
      Value decimal(10,2) NOT NULL,
      Difference decimal(10,4) NOT NULL,
      FOREIGN KEY (PortfolioID) REFERENCES PORTFOLIO (PortfolioID)
      );
  
  /* function to find the last value */
  CREATE FUNCTION LastValue (Portfolio int, NewDate date) returns decimal(10,2)
  deterministic
  BEGIN
      DECLARE LastValue decimal(10,4);
      SET LastValue = (select Value from value WHERE PortfolioID=Portfolio AND DATE=(select max(date) from value));
      IF LastValue is null then set LastValue = 0;
      end if;
  RETURN LastValue;
  END;
  
  /* trigger to get Difference for new day */
  CREATE TRIGGER insert_new_value
      BEFORE INSERT
      ON Value FOR EACH ROW
  BEGIN
      IF LastValue(new.PortfolioID, new.Date)=0 THEN SET new.Difference=0;
      ELSE SET new.Difference=(new.Value/LastValue(new.PortfolioID, new.Date))-1;
      END IF;
  END; 
  
  /* trigger to update value and difference for the same day */
  CREATE TRIGGER update_new_value
      BEFORE UPDATE
      ON Value FOR EACH ROW
  BEGIN
      IF LastValue(old.PortfolioID, old.Date)=0 THEN SET new.Difference=0;
      ELSE SET new.Difference=(new.Value/LastValue(old.PortfolioID, old.Date))-1;
      END IF;
  END;
  
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
  VALUES (0.00, 0.00, 'Start of the wallet'); """)
