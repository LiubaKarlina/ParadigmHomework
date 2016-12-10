select Country.Name from
Country left join City on Country.Code = City.CountryCode and Country.Population > 0
group by Country.Code
order by (Country.Population - sum(City.Population)) desc, Country.Name;
 
