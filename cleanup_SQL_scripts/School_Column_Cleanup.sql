-- Detele duplicates in column title, school and text (489 records) in School Column
DELETE 
FROM policies
WHERE id IN
		(SELECT id 
		 FROM 
			(SELECT id, 
			ROW_NUMBER() OVER ( PARTITION BY title, school, text
			ORDER BY id ) AS row_num
			 FROM policies ) t
			 WHERE t.row_num > 1); 

-- Find typos of university
SELECT DISTINCT School
FROM public.policies
ORDER BY School;

-- Fix "american university": remove trailing whitespace (58 records)
UPDATE public.policies
SET school = 'american university'
WHERE school = 'american university ';

-- Fix "baylor university": remove typos (1 record)
UPDATE public.policies
SET school = 'baylor university'
WHERE school = 'baylor univesity';


-- Fix "binghamton university": remove superfluous locational data (260 records)
UPDATE public.policies
SET school = 'binghamton university'
WHERE school = 'binghamton university - state university of new york'
	or school = 'binghamton university -- suny' 
	or school = 'binghamton university – suny';

-- Fix "bowdoin college": remove simple nominal errors (5 records)
UPDATE public.policies
SET school = 'bowdoin college'
WHERE school = 'bowdoin university';

-- Fix "scripps college": remove simple nominal errors (1 record)
UPDATE public.policies
SET school = 'scripps college'
WHERE school = 'california';

-- Fix "carnegie mellon university": remove simple nominal errors (1 record)
UPDATE public.policies
SET school = 'carnegie mellon university'
WHERE school = 'carnegie mellon';

-- Fix "pomona college": remove simple nominal errors (1 record)
UPDATE public.policies
SET school = 'pomona college'
WHERE school = 'claremont';

-- Fix "colby college": remove simple nominal errors (27 records)
UPDATE public.policies
SET school = 'colby college'
WHERE SCHOOL = 'colby';

-- Fix "colgate univeristy": remove simple nominal errors (6 records)
UPDATE public.policies
SET school = 'colgate univeristy'
WHERE SCHOOL = 'colgate';

-- Fix "college of the ozarks": remove simple typos (4 records)
UPDATE public.policies
SET school = 'college of the ozarks'
WHERE SCHOOL = 'college of the ozark';

-- Fix "colorado state university": remove simple normal errors (30 records)
UPDATE public.policies
SET school = 'colorado state university'
WHERE SCHOOL = 'colorado state university, fort collins';

-- Fix "columbia university": remove simple normal errors (1 record)
UPDATE public.policies
SET school = 'columbia university'
WHERE SCHOOL = 'columbia';

-- Fix "dartmouth college": remove simple normal errors (5 records)
UPDATE public.policies
SET school = 'dartmouth college'
WHERE SCHOOL = 'dartmouth';

-- (58 records)
UPDATE public.policies 
SET school = 'dartmouth college'
WHERE SCHOOL = 'dartmouth university';

-- Fix "davidson college": remove simple normal errors (2 records)
UPDATE public.policies
SET school = 'davidson college'
WHERE SCHOOL = 'davidson university';

-- Fix "edgewood college": 
-- remove critical error (1 record of University of Maine was tagged as edgewood university)
UPDATE public.policies
SET school = 'university of maine'
WHERE id = '23008';

-- remove simple normal errors (3 records)
UPDATE public.policies
SET school = 'edgewood college'
WHERE SCHOOL = 'edgewood university';

-- Fix "fordham university": remove simple typos (1 record)
UPDATE public.policies
SET school = 'fordham university'
WHERE SCHOOL = 'fordham unversity';

-- Fix the City & State column for one of the "baylor university": (1 record)
UPDATE public.policies
SET state = 'texas', city = 'waco'
WHERE id = '3414';

-- Fix "depaul university": remove trailing whitespace (82 records)
UPDATE public.policies
SET school = 'depaul university'
WHERE school = 'depaul university ';

-- Fix "university of maine": critical errors that some of these records were tagged as "edgewood college"
-- (13 records)
UPDATE public.policies
SET school = 'university of maine'
WHERE school = 'edgewood college' AND state = 'maine';

-- Fix "biola university": normal typo (1 record)
UPDATE public.policies
SET school = 'biola university'
WHERE school = 'facilities management';

-- Fix "harvard university": simple normal errors 

-- (1 record)
UPDATE public.policies
SET school = 'harvard university'
WHERE school = 'harvard';

-- (1 record)
UPDATE public.policies
SET school = 'harvard university'
WHERE school = 'harvard college';

-- Fix state and city column of "harvey mudd college": (2 records)
UPDATE public.policies
SET state = 'california', city = 'claremont'
WHERE school = 'harvey mudd college' AND state = 'hawaii';

-- Fix "illinois state university": simple typos: (3 records)
UPDATE public.policies
SET school = 'illinois state university'
WHERE school = 'illinois state univesity' OR school = 'illinois state univresity';

-- Fix "binghamton university": simple typos: (1 record)
UPDATE public.policies
SET school = 'binghamton university'
WHERE school = 'information technology services (its)';

-- Fix "carnegie mellon university": 1 typo (1 record)
UPDATE public.policies
SET school = 'carnegie mellon university'
WHERE school = 'llo';

-- Fix city column of a record of "loyola university new orleans": (1 record)
UPDATE public.policies
SET city = 'new orleans'
WHERE school = 'loyola university new orleans' AND city = 'baton rouge';

-- Fix "michigan technological university": simple typo (1 record)
UPDATE public.policies
SET school = 'michigan technological university'
WHERE school = 'michgan technological university';

-- (1 record)
UPDATE public.policies
SET school = 'michigan technological university'
WHERE school = 'michigan state';

-- Fix "michigan state university": simple typos (2 records)
UPDATE public.policies
SET school = 'michigan state university'
WHERE school = 'michigan state univresity' OR school = 'michigan state unversity';

-- Fix "michigan technological university": simple normal error (1 record)
UPDATE public.policies
SET school = 'michigan technological university'
WHERE school = 'michigan technological institute';

-- Fix "montclair state university": simple normal error (1 error)
UPDATE public.policies
SET school = 'montclair state university'
WHERE school = 'montclair state';

-- Fix state and city in "northeastern university": (1 record)
UPDATE public.policies
SET state = 'massachusetts', city = 'boston'
WHERE school = 'northeastern university' AND state = 'virginia';

-- Fix "ohio state university": simple typos(2 records)
UPDATE public.policies
SET school = 'ohio state university'
WHERE school = 'ohio state' OR school = 'ohio statement';

-- Fix "miami university": simple typos(1 record)
UPDATE public.policies
SET school = 'miami university'
WHERE school = 'oxford university';

-- Fix "pomona college": simple normal error(6 records)
UPDATE public.policies
SET school = 'pomona college'
WHERE school = 'pomona' OR school = 'pomona university';

-- Fix "rochester institute of technolgy": simple typo (2 records)
UPDATE public.policies
SET school = 'rochester institute of technology'
WHERE school = 'rochester institute of technolgy' OR school = 'rochester university';

-- Fix "rowan university": simple typo(1 record)
UPDATE public.policies
SET school = 'rowan university'
WHERE school = 'rowan universtiy';

-- Fix "rutgers university": simple normal errors (188 records)
UPDATE public.policies
SET school = 'rutgers university'
WHERE school = 'rutgers' OR school = 'rutgers university - neward' 
OR school = 'rutgers university–newark';

-- Fix "southern methodist university": simple normal errors (1 record)
UPDATE public.policies
SET school = 'southern methodist university'
WHERE school = 'southern methodist';

-- Fix "san diego state university": simple normal typos (2 records)
UPDATE public.policies
SET school = 'san diego state university'
WHERE school = 'san diego state university`' OR school = 'san diego state unviersity';

-- Fix "spring hill college": simple normal typo (1 record)
UPDATE public.policies
SET school = 'spring hill college'
WHERE school = 'spring hill colelge';

-- Fix "spring hill college": simple normal errors (1 record)
UPDATE public.policies
SET school = 'spring hill college'
WHERE school = 'spring hill colelge';

-- Fix "university of nevada, las vegas": tagged as other university (2 records)
UPDATE public.policies
SET school = 'university of nevada, las vegas', state = 'nevada', city = 'las vegas'
WHERE id = '3104' OR id = '3105';

-- Fix "st. john's university": simple normal errors (8 records)
UPDATE public.policies
SET school = 'st. john''s university'
WHERE school = 'st john''s university queens campus' OR school = 'st. john university';

-- Fix "stanford university": simple typos (1 record)
UPDATE public.policies
SET school = 'stanford university'
WHERE school = 'stanford unviersity';

-- Fix "stony brook university": simple normal error (1 record)
UPDATE public.policies
SET school = 'stony brook university'
WHERE school = 'stony brook';

-- Fix "the university of montana western": simple normal error (1 record)
UPDATE public.policies
SET school = 'the university of montana western'
WHERE school = 'student political groups & campaigning';

-- Fix "suny college of environmental science and forestry": simple normal typos (1 record)
UPDATE public.policies
SET school = 'suny college of environmental science and forestry'
WHERE school = 'suny college of environmental science and forestry latitude and longitude';

-- Fix "syracuse university": simple normal errors (9 records)
UPDATE public.policies
SET school = 'syracuse university'
WHERE school = 'syracuse';

-- Fix "texas a&m university": simple normal errors (196 records)
UPDATE public.policies
SET school = 'texas a&m university'
WHERE school = 'texas' OR school = 'texas a&m university--college station';

-- Fix "boise state university": simple normal errors (1 record)
UPDATE public.policies
SET school = 'boise state university'
WHERE school = 'the boise state university';

-- Fix "florida state university": simple normal errors (51 records)
UPDATE public.policies
SET school = 'florida state university'
WHERE school = 'the florida state university';

-- Fix "loyola university new orleans": simple normal errors (1 record)
UPDATE public.policies
SET school = 'loyola university new orleans'
WHERE school = 'the loyola university new orleans';

-- Fix "savannah college of art and design": simple normal errors (2 records)
UPDATE public.policies
SET school = 'savannah college of art and design'
WHERE school = 'the savannah college of art and design';

-- Fix "the university of california berkeley": simple normal errors (1 record)
UPDATE public.policies
SET school = 'the university of california berkeley'
WHERE school = 'the university california berkeley';

-- Fix "the university of north carolina at chapel hill": simple normal errors (1 record)
UPDATE public.policies
SET school = 'the university of north carolina at chapel hill'
WHERE school = 'the university north carolina at chapel hill';

-- Fix "the university of north carolina at chapel hill": simple normal errors (1 record)
UPDATE public.policies
SET school = 'the university of north carolina at chapel hill'
WHERE school = 'the university north carolina at chapel hill';

-- Fix "the university of chicago": simple normal errors (3 records)
UPDATE public.policies
SET school = 'the university of chicago'
WHERE school = 'the university of alabama' and city = 'chicago';

-- (15 records)
UPDATE public.policies
SET school = 'the university of chicago'
WHERE school = 'university of chicago';

-- Fix "loyola university new orleans": simple normal errors (2 records)
UPDATE public.policies
SET school = 'loyola university new orleans'
WHERE school = 'the university of loyola new orleans';

-- Fix "the university of mississippi": simple normal errors (103 records)
UPDATE public.policies
SET school = 'the university of mississippi'
WHERE school = 'university of mississippi';

-- Fix "university of north texas at dallas": simple normal errors (64 records)
UPDATE public.policies
SET school = 'university of north texas at dallas'
WHERE school = 'the university of north texas at dallas';

-- Fix "university of rhode island": simple normal errors (36 records)
UPDATE public.policies
SET school = 'university of rhode island'
WHERE school = 'university of rhode island';

-- Fix "university of the pacific": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of the pacific'
WHERE school = 'the university of the pacific';

-- Fix "university of washington tacoma": simple normal errors (21 records)
UPDATE public.policies
SET school = 'university of washington tacoma'
WHERE school = 'the university of washington tacoma';

-- Fix "university system of maryland": simple normal errors (108 records)
UPDATE public.policies
SET school = 'university system of maryland'
WHERE school = 'towson';

-- Fix "university of illinois at urbana-champaign": simple normal errors (4 records)
UPDATE public.policies
SET school = 'university of illinois at urbana-champaign'
WHERE school = 'u of illinois urbana champaign' OR school = 'u of illinois urbana campaign';

-- Fix "university of vermont": simple normal errors (3 records)
UPDATE public.policies
SET school = 'university of vermont'
WHERE school = 'university fo vermont' or school = 'university if vermont';

-- Fix "university of maryland": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of maryland'
WHERE school = 'university libraries';

-- Fix "university of rhode island": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of rhode island'
WHERE school = 'university of	rhode island';

-- Fix "university of alaska fairbanks": simple normal errors (37 records)
UPDATE public.policies
SET school = 'university of alaska fairbanks'
WHERE school = 'university of alaska';

-- Fix "university of arkansas": simple normal errors (3 records)
UPDATE public.policies
SET school = 'university of arkansas'
WHERE school = 'university of arakansas' or school = 'university of akransas';

-- Fix "University of La Verne": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of la verne'
WHERE school = 'university of california' and city = 'la verne';

-- Fix "the university of california santa cruz": simple normal errors (1 record)
UPDATE public.policies
SET school = 'the university of california santa cruz'
WHERE school = 'university of california';

-- (351 records)
UPDATE public.policies
SET school = 'the university of california santa cruz'
WHERE school = 'university of california, santa cruz';

-- Fix "the university of california davis": simple normal errors (37 records)
UPDATE public.policies
SET school = 'the university of california davis'
WHERE school = 'university of california, davis';

-- Fix "the university of california los angeles": simple normal errors (14 records)
UPDATE public.policies
SET school = 'the university of california los angeles'
WHERE school = 'university of california--los angeles' or school = 'university of california-- los angeles';

-- Fix "the university of california merced": simple normal errors (167 records)
UPDATE public.policies
SET school = 'the university of california merced'
WHERE school = 'university of california--merced';

-- Fix "the university of california riverside": simple normal errors (458 records)
UPDATE public.policies
SET school = 'the university of california riverside'
WHERE school = 'university of california--riverside';

-- Fix "the university of chicago": simple normal errors (1 record)
UPDATE public.policies
SET school = 'the university of chicago'
WHERE school = 'university of chicago illinois';

-- Fix "university of cincinnati": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of cincinnati'
WHERE school = 'university of cininnati';

-- Fix "university of illinois at urbana-champaign": simple normal errors (29 records)
UPDATE public.policies
SET school = 'university of illinois at urbana-champaign'
WHERE school = 'university of illinois' OR school = 'university of illinois at urbana–champaign'
OR school = 'university of illinois urbana champaign';

-- Fix "university of illinois at urbana-champaign": simple normal errors (32 records)
UPDATE public.policies
SET school = 'university of illinois at urbana-champaign'
WHERE school = 'university of illinois' OR school = 'university of illinois at urbana–champaign'
OR school = 'university of illinois urbana champaign'
OR school = 'university of illinois urbana-champaign';



-- Fix "university of illinois chicago": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of illinois chicago'
WHERE school = 'university of illinois chicago     university of illinois chicago';

-- Fix "university of lincoln": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of lincoln'
WHERE school = 'university of lincoln, nebraska';

-- Fix "university of maine": simple normal errors (71 records)
UPDATE public.policies
SET school = 'university of maine'
WHERE school = 'university of maine, orone' or school = 'university of maine, orono';

-- Fix "university of massachusetts lowell": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of massachusetts lowell'
WHERE school = 'university of massachusetts medical school';


-- Fix "The University of Georgia": simple normal errors (1 record)
UPDATE public.policies
SET school = 'the university of georgia'
WHERE school = 'university of michigan' AND state = 'georgia';

-- Fix "rutgers university": simple normal errors (59 records)
UPDATE public.policies
SET school = 'rutgers university'
WHERE school = 'rutgers university - newark';

-- Fix "the university of vermont": simple normal errors (59 records)
UPDATE public.policies
SET school = 'the university of vermont'
WHERE school = 'university of washington' AND state = 'vermont';

-- Fix "university of minnesota, twin cities": simple normal errors (61 records)
UPDATE public.policies
SET school = 'university of minnesota, twin cities'
WHERE school = 'university of minnesota, twin cities ';

-- Fix "north carolina state university": simple normal errors (1 record)
UPDATE public.policies
SET school = 'north carolina state university'
WHERE school = 'university of minnesota, twin cities' AND state = 'north carolina';

-- (239 records)
UPDATE public.policies
SET school = 'north carolina state university'
WHERE school = 'north carolina state university--raleigh';

-- Fix "university of mississippi": simple normal errors (2 records)
UPDATE public.policies
SET school = 'university of mississippi'
WHERE school = 'university of missippi' OR school = 'university of mississipppi';

-- Fix "University System of New Hampshire": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university system of new hampshire'
WHERE school = 'university of new hampshire';

-- Fix "university of vermont": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of vermont'
WHERE school = 'university of vermotn';

-- Fix "university of wisconsin-madison": simple normal errors (47 records)
UPDATE public.policies
SET school = 'university of wisconsin-madison'
WHERE school = 'university of wisconsin madison' OR school = 'university of wisconsin';

-- Fix "University of Arkansas": simple normal errors (1 record)
UPDATE public.policies
SET school = 'university of arkansas'
WHERE school = 'uofarkansas';

-- Fix "arizona christian university": simple normal errors (5 records)
UPDATE public.policies
SET state = 'arizona'
WHERE school = 'arizona christian university' AND state = 'arkansas';

-- Fix "clarkson university": simple normal errors (1 record)
UPDATE public.policies
SET state = 'new york'
WHERE school = 'clarkson university' AND state = 'washington';

-- Fix "UNIVERSITY OF MICHIGAN-DEARBORN": simple normal errors (253 records)
UPDATE public.policies
SET school = 'university of michigan-dearborn'
WHERE school = 'um-dearnborn' OR school = 'university of michigan- dearborn';

-- Fix "university of illinois at urbana-champaign": simple normal errors (1 record)
UPDATE public.policies
SET state = 'illinois'
WHERE school = 'university of illinois at urbana-champaign' AND state = 'california';

-- Fix "wichita state university": simple normal errors (1 record)
UPDATE public.policies
SET state = 'kansas', city = 'wichita'
WHERE school = 'wichita state university' AND state = 'iowa';

SELECT DISTINCT School
FROM public.policies
ORDER BY School;
