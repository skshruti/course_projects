--1--
with s_races as (select raceid, year, country 
                    from races as r
                    inner join circuits as c
                    on c.circuitid = r.circuitid
                    where year = 2017 and country = 'Monaco'),
     races_laptimes as (select * from s_races inner join lapTimes
                    on lapTimes.raceid = s_races.raceid),
     driverids as (select driverid, milliseconds from races_laptimes where milliseconds in 
                    (select max(milliseconds) from races_laptimes))
select drivers.driverid, forename, surname, nationality, milliseconds as time
     from driverids inner join drivers on drivers.driverid = driverids.driverid
order by forename, surname, nationality;

--2--
select c.name as constructor_name, cid as constructorid, c.nationality, sumpoints as points from 
    constructors as c
    inner join
    (select y.cid, sum(y.p) as sumpoints from
        (select cr.constructorId as cid, cr.points as p, r.year from constructorResults as cr
        inner join races as r 
        on r.raceId = cr.raceId
        where r.year = 2012) as y
        group by y.cid) as cids 
    on cids.cid = c.constructorId
order by 
    points desc, constructor_name, nationality, constructorid
    limit 5;

--3--
with driverIds(did, p) as 
    (select r.driverId, sum(r.points)
    from races
    inner join results as r
    on r.raceId = races.raceId
    where races.year between 2001 and 2020
    group by r.driverId)
select drivers.driverid, forename, surname, p as points from driverIds
    inner join drivers 
    on drivers.driverid = driverIds.did
    where p in (select max(p) from driverIds)
order by forename, surname, driverId;

--4--
with constructorids(cid, p) as 
    (select cr.constructorid, sum(cr.points)
    from constructorResults as cr
    inner join races
    on cr.raceId = races.raceId
    where races.year between 2010 and 2020
    group by cr.constructorid)
select cid as constructorid, name, nationality, p as points from constructorids
    inner join constructors 
    on constructors.constructorid = constructorids.cid
    where p in (select max(p) from constructorids)
order by name, nationality, cid;

--5--
with driverIds(did, c) as 
    (select driverid, count(*) from results where positionorder=1 group by driverid)
select driverId, forename, surname, c as race_wins from drivers, driverIds where 
    drivers.driverid=driverIds.did and
    driverid in 
    (select did from driverIds where c in (select max(c) from driverIds))
order by forename, surname, driverId;

--6--
with constructorIds(cid, c) as 
    (select constructorid, count(points) from constructorResults where (raceId, points) in 
    (select raceid,max(points) from constructorResults group by raceId)
    group by constructorid)
select constructorid, name, c as num_wins from constructors, constructorIds where 
    constructors.constructorId=constructorIds.cid and
    constructorid in 
    (select cid from constructorIds where c in (select max(c) from constructorIds))
order by name, constructorId;

--7--
with driverids(did) as 
    (select distinct(driverid) from drivers where drivers.driverId not in 
        (with totalpoints as (select year, driverid, sum(points) as p from results 
            inner join races
            on races.raceid = results.raceid
            group by year, driverid)
        select distinct(driverid) from totalpoints where (year,p) in (select year,max(p) from totalpoints group by year)
        ))
select drivers.driverid, forename, surname, total as points from (select results.driverid, sum(points) as total from drivers
    inner join results 
    on results.driverid=drivers.driverId
    group by results.driverid
    ) as t
    inner join drivers on drivers.driverid = t.driverid
    where t.driverid in (select * from driverids)
order by total desc, forename, surname, driverid
limit 3;

--8--
with driver_countries(nc,did) as 
    (select count(distinct(circuits.country)) as num_countries, winners.driverId from races 
    inner join 
    (select * from results where positionorder=1) as winners
    on winners.raceId = races.raceId
    inner join circuits 
    on circuits.circuitid=races.circuitid
    group by winners.driverId) 
select driverid, forename, surname, nc as num_countries from driver_countries
    inner join drivers on
    drivers.driverid = driver_countries.did
    where nc in (select max(driver_countries.nc) from driver_countries)
order by forename, surname, driverid;

--9--
with winners as (select drivers.driverid, results.raceid from drivers
        inner join results
        on results.driverid = drivers.driverid
        where results.positionOrder = 1 and grid = 1),
        topthree as (select winners.driverid, count(*) as nw from winners group by winners.driverid order by nw desc limit 3)
select drivers.driverId, forename, surname, nw as num_wins from topthree 
    inner join drivers 
    on drivers.driverid = topthree.driverid
order by num_wins desc, forename, surname, driverId;

--10--
with temp as (with didstoprid(rid,stops,did) as
(with pstaken(rid, stops, did) as 
(select winners.raceid, count(stop) as stops, max(pitStops.driverId) as did from pitStops 
inner join
(select driverid, raceid from results where positionorder=1) as winners
on winners.raceid = pitStops.raceid and winners.driverId = pitStops.driverId
group by winners.raceid) 
select * from pstaken
where (pstaken.did, pstaken.stops) in (select pstaken.did, max(stops) from pstaken group by pstaken.did))
select rid as raceid, stops as num_stops, did as driverid, forename, surname, circuits.circuitid as circuitId, circuits.name as name from didstoprid 
    inner join drivers 
    on drivers.driverid = didstoprid.did
    inner join races 
    on races.raceid = didstoprid.rid
    inner join circuits
    on circuits.circuitid = races.circuitid)
select * from temp where num_stops in (select max(num_stops) from temp)
order by forename, surname, name, circuitId, driverid;

--11--
with topridnc(rid,nc) as 
    (with ridnc(rid, nc) as 
    (select raceId, count(*) as nc from results where statusid = 4 group by raceId) 
    select * from ridnc where nc in (select max(nc) from ridnc))
select rid as raceid, circuits.name as name, circuits.location as location, nc as num_collisions from topridnc
    inner join races on 
    races.raceId = topridnc.rid
    inner join circuits on
    circuits.circuitid = races.circuitid;

--12--
with driverIds as (select driverid, count(*) as c from results where rank = 1 and positionOrder = 1 group by driverid)
select drivers.driverid, forename, surname, driverids.c as count
     from driverids inner join drivers on drivers.driverid = driverids.driverid
     where c in (select max(c) from driverIds)
order by forename, surname, drivers.driverid;

--13--
with toptwo(yr, cid, p, rn) as
    (select year, constructorid, sum(points), 
    ROW_NUMBER() OVER(partition by year order by sum(points) desc) AS rn
    from constructorResults 
    inner join races 
    on races.raceId = constructorResults.raceId
    group by constructorid, year
    order by year, sum(points) desc),
    first as (select * from toptwo where rn=1),
    second as (select * from toptwo where rn=2),
    diffs as (select first.yr as year, first.p-second.p as point_diff, first.cid as constructor1_id, second.cid as constructor2_id from first
                inner join second
                on first.yr = second.yr),
    topdiff as (select * from diffs where point_diff in (select max(point_diff) from diffs))
select year, point_diff, constructor1_id, c1.name as constructor1_name, constructor2_id, c2.name as constructor2_name from topdiff
    inner join constructors as c1 on c1.constructorid = topdiff.constructor1_id
    inner join constructors as c2 on c2.constructorid = topdiff.constructor2_id
order by constructor1_name, constructor2_name, constructor1_id, constructor2_id;
    
--14--
with race2018 as (select * from races where year = 2018),
    raceresults as (select race2018.raceid, race2018.circuitid, results.driverid, results.grid from race2018 inner join results on results.raceid = race2018.raceid where positionOrder=1),
    rrcircuit as (select raceresults.raceid, raceresults.circuitid, raceresults.driverid, raceresults.grid, circuits.country from raceresults inner join circuits on circuits.circuitid = raceresults.circuitid),
    driverids as (select * from rrcircuit where grid in (select max(grid) from rrcircuit))
select driverIds.driverid, forename, surname, driverids.circuitid, driverids.country, grid as pos from driverids inner join drivers on drivers.driverid = driverIds.driverid
order by forename, surname, country, driverid, circuitid;

--15--
with failures as (select constructors.constructorid, results.raceid, constructors.name 
                    from constructors inner join results 
                    on results.constructorid = constructors.constructorid 
                    where statusid = 5),
     count_failures as (select failures.constructorid, count(failures.raceid) as nf, max(failures.name) as name
                    from failures inner join races on races.raceid = failures.raceid
                    where races.year between 2000 and 2021
                    group by failures.constructorid)
select constructorid, name, nf as num from count_failures where nf in (select max(nf) from count_failures)
order by name, constructorid;

--16--
with americans as (select * from drivers where nationality='American'),
    american_winners as (select americans.driverid, americans.forename, americans.surname, results.raceid
                         from americans inner join results on results.driverid = americans.driverid 
                         where positionOrder = 1),
    winners_races as (select * from american_winners inner join races on races.raceid = american_winners.raceid)
select DISTINCT driverid, forename, surname from winners_races 
    inner join circuits on circuits.circuitid = winners_races.circuitid where country='USA'
order by forename, surname, driverid
limit 5;

--17--
with race as (select raceid from races where year >= 2014),
     first as (select results.raceid, constructorid, driverid, positionOrder from results inner join race on race.raceid = results.raceid where positionOrder = 1),
     second as (select results.raceid, constructorid, driverid, positionOrder from results inner join race on race.raceid = results.raceid where positionOrder = 2),
     cidnfs as (select first.constructorid, count(*) as nfs from first, second 
                where first.raceid = second.raceid and first.constructorid = second.constructorid 
                group by first.constructorid)
select constructors.constructorid, name, nfs as count from cidnfs inner join constructors on constructors.constructorid = cidnfs.constructorid
    where nfs in (select max(nfs) from cidnfs);

--18--
with nlaps as (select drivers.driverid, max(forename) as fn, max(surname) as sn, count(*) as nl from drivers
                inner join lapTimes on
                drivers.driverid = lapTimes.driverid
                where position = 1
                group by drivers.driverid)
select driverid, fn as forename, sn as surname, nl as num_laps from nlaps where nl in (select max(nl) from nlaps)
order by forename, surname, driverid;

--19--
with npodiums as (select driverid, count(*) as np from results where positionOrder in (1,2,3) group by driverid)
select drivers.driverid, forename, surname, np as count from npodiums inner join drivers
 on drivers.driverid = npodiums.driverid
 where np in (select max(np) from npodiums)
order by forename, surname, driverid;

--20--
with totalpoints as (select year, driverid, sum(points) as p from results 
    inner join races
    on races.raceid = results.raceid
    group by year, driverid),
    nwins as (select driverid, count(*) as nw from totalpoints where (year,p) in (select year,max(p) from totalpoints group by year) group by driverid)
select drivers.driverid, forename, surname, nw as num_champs from nwins inner join drivers on drivers.driverid = nwins.driverid
order by num_champs desc, forename, surname, drivers.driverid
limit 5;

