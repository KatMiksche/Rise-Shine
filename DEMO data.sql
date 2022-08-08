use riseshine;

insert into portfolio (name) values ('DEMO PORTFOLIO');

update value set Date='2022-01-01' where portfolioid=(select portfolioid from portfolio where name='DEMO PORTFOLIO');

insert into hold (ticker, volume, portfolioid) values 
('IBM',100,(select portfolioid from portfolio where name='DEMO PORTFOLIO')),
('MSFT',50,(select portfolioid from portfolio where name='DEMO PORTFOLIO')),
('AAPL',10,(select portfolioid from portfolio where name='DEMO PORTFOLIO'));

insert into wallet (currentwallet, valuechange, description) values (10000,10000,'DEMO MONEY');
