select First.Year, Second.Year, Country.Name, 1.0 * (Second.Rate - First.Rate) / (Second.Year - First.Year) from
Country inner join LiteracyRate First on Country.Code = First.CountryCode 
inner join LiteracyRate Second on Country.Code = Second.CountryCode and Second.Year > First.Year
group by First.Year, Country.Code
having min(Second.Year) = Second.Year 
order by 1.0 * (Second.Rate - First.Rate) / (Second.Year - First.Year) desc;
