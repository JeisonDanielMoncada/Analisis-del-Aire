SELECT p.City  , c2.CO , c2.overall_aqi ,p."Total Population" 
FROM ciudades c, poblacion p
JOIN ciudades c2 on c2.City_1 == p.City 
GROUP BY p."Total Population"  
ORDER BY p."Total Population"  DESC 
LIMIT 10;