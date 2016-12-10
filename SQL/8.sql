select Country.Name, Country.Population, Country.SurfaceArea from 
Country left join Capital on Country.Code = Capital.CountryCode left join City on Country.Code = City.CountryCode
group by Country.Code
having count(*) > 0 and max(City.Population) == City.Population and City.Id != Capital.CityId
order by (1.0 * Country.Population / Country.SurfaceArea) desc, Country.Name; 
