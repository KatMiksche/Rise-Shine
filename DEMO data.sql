use riseshine;

insert into portfolio (name) values ('DEMOx');

set @id=(select portfolioid from portfolio where name='DEMOx');
update value set Date=DATE_SUB(curdate(), INTERVAL 60 DAY) where portfolioid=@id;

insert into hold (ticker, volume, portfolioid) values 
('IBM',100,@id),
('MSFT',50,@id),
('AAPL',10,@id);

SET @var  = (select currentwallet from wallet order by date desc limit 1) ;
insert into wallet (currentwallet, valuechange, description) values (10000+@var,10000,'DEMO MONEY');

update portfolio set name='DEMO PORTFOLIO' where name='DEMOx';