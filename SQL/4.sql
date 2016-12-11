select Country.Name, count(distinct City.Id) from 
Country left join City on Country.Code = City.CountryCode and City.Population >= 1000000
group by Country.Code
order by count(distinct City.Id) desc, Country.Name;
