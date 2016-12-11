select Country.Name from
Country left join City on Country.Code = City.CountryCode and Country.Population > 0
group by Country.Code
having Country.Population > 2 * sum(City.Population)
order by Country.Name;
 
