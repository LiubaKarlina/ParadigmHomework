select Country.Name, count(*) from 
Country inner join City on Country.Code = City.CountryCode and City.population >= 1000000
group by City.CountryCode
order by count(*) desc, Country.Name;
