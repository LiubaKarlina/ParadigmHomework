select City.Name from City, Capital, Country
where City.Id = Capital.CityId and City.CountryCode = Country.code and Country.Name = "Belgium";
