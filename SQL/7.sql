select Country.Name from
Country left join City on Country.Code = City.CountryCode
group by Country.Code
having Country.Population > 2 * sum(City.Population) and Country.Population > 0
order by Country.Name;
 
