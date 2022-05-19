--1--
with onehop as (select distinct destination_station_name from train_info where train_no=97131 and source_station_name='KURLA' and train_info.source_station_name<>train_info.destination_station_name),
    twohop as (select distinct destination_station_name from train_info where source_station_name in (select destination_station_name from onehop) and train_info.source_station_name<>train_info.destination_station_name),
    threehop as (select distinct destination_station_name from train_info where source_station_name in (select destination_station_name from twohop) and train_info.source_station_name<>train_info.destination_station_name),
    unionstations as (select * from onehop union (select * from twohop) union (select * from threehop))
select distinct * from unionstations order by destination_station_name;

--2--
with onehop as (select distinct destination_station_name, train_info.day_of_arrival from train_info 
        where train_no=97131 and source_station_name='KURLA' and train_info.day_of_arrival=train_info.day_of_departure
        and train_info.source_station_name<>train_info.destination_station_name),
    twohop as (select distinct train_info.destination_station_name, train_info.day_of_arrival
        from train_info inner join onehop on 
        train_info.source_station_name=onehop.destination_station_name and 
        train_info.day_of_arrival=train_info.day_of_departure and 
        train_info.day_of_departure=onehop.day_of_arrival
        and train_info.source_station_name<>train_info.destination_station_name
        ),
    threehop as (select distinct train_info.destination_station_name, train_info.day_of_arrival
        from train_info inner join twohop on 
        train_info.source_station_name=twohop.destination_station_name and 
        train_info.day_of_arrival=train_info.day_of_departure and 
        train_info.day_of_departure=twohop.day_of_arrival
        and train_info.source_station_name<>train_info.destination_station_name
        ),
    unionstations as (select * from onehop union (select * from twohop) union (select * from threehop))
select distinct destination_station_name from unionstations order by destination_station_name;

--3--
with RECURSIVE journey(dest, dist, day) as 
    (select destination_station_name, distance, day_of_arrival, 0 as hops, array[source_station_name, destination_station_name] as stations 
        from train_info 
        where source_station_name='DADAR' and 
        train_info.day_of_arrival=train_info.day_of_departure 
    union all
    select t.destination_station_name, t.distance+j.dist, t.day_of_arrival, j.hops+1, j.stations || t.destination_station_name
    from train_info t, journey j 
    where t.source_station_name=j.dest and 
        t.day_of_arrival=j.day and 
        t.day_of_departure=t.day_of_arrival and
        t.destination_station_name != all(j.stations) and
        t.source_station_name<>t.destination_station_name and 
        j.hops < 2)
select distinct dest as destination_station_name, dist as distance, day from journey 
where dest!='DADAR'
order by destination_station_name, distance, day;

--4--
with RECURSIVE 
    weekdays as (
        select 'Monday' as day, 1 as num union
        select 'Tuesday' as day, 2 as num union
        select 'Wednesday' as day, 3 as num union
        select 'Thursday' as day, 4 as num union
        select 'Friday' as day, 5 as num union
        select 'Saturday' as day, 6 as num union
        select 'Sunday' as day, 7 as num
    ),
    journey as 
        (select source_station_name, destination_station_name, day_of_arrival, arrival_time, 0 as hops, 
            array[source_station_name, destination_station_name] as stations 
            from train_info 
            where source_station_name='DADAR'
        union all
        select j.source_station_name, t.destination_station_name, t.day_of_arrival, t.arrival_time, j.hops+1, 
            j.stations || t.destination_station_name
            from train_info t, journey j, weekdays w1, weekdays w2 
            where t.source_station_name=j.destination_station_name and 
                t.source_station_name<>t.destination_station_name and
                t.destination_station_name != all(j.stations) and
                w1.day=j.day_of_arrival and w2.day=t.day_of_departure and
                (w1.num<w2.num or (w1.num=w2.num and j.arrival_time<=t.departure_time)) and
                j.hops < 2)
select distinct destination_station_name from journey
order by destination_station_name;

--5--
with RECURSIVE journey(dest, dist, day) as 
    (select destination_station_name, distance, day_of_arrival, 0 as hops, array[source_station_name, destination_station_name] as stations 
        from train_info 
        where source_station_name='CST-MUMBAI' 
    union all
    select t.destination_station_name, t.distance+j.dist, t.day_of_arrival, j.hops+1, j.stations || t.destination_station_name
    from train_info t, journey j 
    where t.source_station_name=j.dest and 
        t.source_station_name<>t.destination_station_name and
        t.destination_station_name != all(j.stations) and
        j.hops < 2),
result as (select dest as destination_station_name, dist as distance, day from journey 
where dest='VASHI')
select count(*) from result;

--6--
with RECURSIVE journey as 
    (select source_station_name, destination_station_name, distance, day_of_arrival, 0 as hops, array[source_station_name, destination_station_name] as stations 
        from train_info 
    union all
    select j.source_station_name, t.destination_station_name, t.distance+j.distance, t.day_of_arrival, j.hops+1, j.stations || t.destination_station_name
    from train_info t, journey j 
    where t.source_station_name=j.destination_station_name and 
        t.source_station_name<>t.destination_station_name and
        t.destination_station_name != all(j.stations) and
        j.hops < 5),
    minpath as (select source_station_name, destination_station_name, min(distance) as d from journey group by source_station_name, destination_station_name)
select destination_station_name, source_station_name, d as distance from minpath
order by destination_station_name, source_station_name;

--7--
with RECURSIVE journey as 
    (select source_station_name, destination_station_name, distance, day_of_arrival, 0 as hops, array[source_station_name, destination_station_name] as stations 
        from train_info 
    union all
    select j.source_station_name, t.destination_station_name, t.distance+j.distance, t.day_of_arrival, j.hops+1, j.stations || t.destination_station_name
    from train_info t, journey j 
    where t.source_station_name=j.destination_station_name and 
        t.source_station_name<>t.destination_station_name and
        t.destination_station_name != all(j.stations) and
        j.hops < 3)
select distinct source_station_name, destination_station_name from journey
order by source_station_name, destination_station_name;

--8--
with RECURSIVE journey as 
    (select source_station_name, destination_station_name, distance, day_of_arrival, 0 as hops, array[source_station_name, destination_station_name] as stations 
        from train_info 
        where source_station_name='SHIVAJINAGAR'
        and train_info.day_of_arrival=train_info.day_of_departure 
    union all
    select j.source_station_name, t.destination_station_name, t.distance+j.distance, t.day_of_arrival, j.hops+1, j.stations || t.destination_station_name
    from train_info t, journey j 
    where t.source_station_name=j.destination_station_name and 
        t.source_station_name<>t.destination_station_name and
        t.day_of_arrival=t.day_of_departure and 
        t.day_of_arrival=j.day_of_arrival and
        t.destination_station_name != all(j.stations) and
        j.hops < 3)
select distinct source_station_name, destination_station_name from journey
order by source_station_name, destination_station_name;

--9--
with RECURSIVE journey as 
    (select source_station_name, destination_station_name, distance, day_of_arrival, 0 as hops, array[source_station_name, destination_station_name] as stations 
        from train_info 
        where source_station_name='LONAVLA'
        and train_info.day_of_arrival=train_info.day_of_departure 
    union all
    select j.source_station_name, t.destination_station_name, t.distance+j.distance, t.day_of_arrival, j.hops+1, j.stations || t.destination_station_name
    from train_info t, journey j 
    where t.source_station_name=j.destination_station_name and 
        t.source_station_name<>t.destination_station_name and
        t.day_of_arrival=t.day_of_departure and 
        t.day_of_arrival=j.day_of_arrival and
        t.destination_station_name != all(j.stations)),
    minpath as (select destination_station_name, min(distance) as d from journey group by destination_station_name)
select distance, destination_station_name as destination, day_of_arrival as day from journey where 
    (destination_station_name, distance) in (select * from minpath)
order by distance, destination_station_name, day;

--10--


--11--
with recursive
    stations as (select distinct source_station_name from train_info union (select distinct destination_station_name from train_info)),
    journey as 
    (select source_station_name, destination_station_name, distance, day_of_arrival, 0 as hops, array[source_station_name, destination_station_name] as stations 
        from train_info 
    union all
    select j.source_station_name, t.destination_station_name, t.distance+j.distance, t.day_of_arrival, j.hops+1, j.stations || t.destination_station_name
    from train_info t, journey j 
    where t.source_station_name=j.destination_station_name and 
        t.source_station_name<>t.destination_station_name and
        t.destination_station_name != all(j.stations) and
        j.hops < 1),
    result as (select distinct source_station_name, destination_station_name from journey),
    temp as (select source_station_name, count(*) as count from result group by source_station_name),
    c as (select count(*) from (select distinct * from stations) as p)
select source_station_name from temp where count in (select * from c)
order by source_station_name;

--12--
with arsid as (select teamid from teams where name='Arsenal'),
    awayteamids as (select distinct(awayteamid) from games where hometeamid in (select * from arsid)),
    hometeamids as (select distinct(hometeamid) from games where awayteamid in (select * from awayteamids) except (select * from arsid))
select name as teamnames from teams where teamid in (select * from hometeamids) order by name;

--13--
with arsid as (select teamid from teams where name='Arsenal'),
    awayteamids as (select distinct(awayteamid) from games where hometeamid in (select * from arsid)),
    hometeamidsyear as (select hometeamid, year from games where awayteamid in (select * from awayteamids) and hometeamid not in (select * from arsid)),
    minyear as (select min(year) from hometeamidsyear),
    hometeamids as (select distinct hometeamid from hometeamidsyear where year in (select min(year) from hometeamidsyear)),
    hometeamgoals as (select hometeamid, sum(homegoals) from games where hometeamid in (select * from hometeamids) group by hometeamid),
    awayteamgoals as (select awayteamid, sum(awaygoals) from games where awayteamid in (select * from hometeamids) group by awayteamid),
    totalgoals as (select hometeamid, hometeamgoals.sum+awayteamgoals.sum as tgoals from hometeamgoals inner join awayteamgoals on hometeamid=awayteamid),
    result as (select * from totalgoals, minyear where tgoals in (select max(tgoals) from totalgoals))
select name as teamnames, tgoals as goals, min as year from result inner join teams on teams.teamid = result.hometeamid order by teamnames;

--14--
with Lid as (select teamid from teams where name='Leicester'),
    awayteamids as (select distinct(awayteamid) from games where hometeamid in (select * from Lid)),
    hometeamidsyear as (select hometeamid, year, homegoals-awaygoals as diff from games where awayteamid in (select * from awayteamids) and hometeamid not in (select * from Lid) and year=2015),
    result as (select hometeamid, diff as goals from hometeamidsyear where diff>3)
select name as teamnames, goals as goaldiff from result inner join teams on teams.teamid = result.hometeamid order by goaldiff, teamnames;

--15--
with Vid as (select teamid from teams where name='Valencia'),
    awayteamids as (select distinct(awayteamid) from games where hometeamid in (select * from Vid)),
    hometeamids as (select distinct(hometeamid) from games where awayteamid in (select * from awayteamids) and hometeamid not in (select * from Vid)),
    gameids as (select gameid from games where hometeamid in (select * from hometeamids)),
    sumgoals as (select playerid, sum(goals) as tgoals from gameids inner join appearances on appearances.gameid = gameids.gameid group by playerid)
select name as playernames, tgoals as goals from sumgoals inner join players on players.playerid = sumgoals.playerid where tgoals in (select max(tgoals) from sumgoals) order by playernames;

--16--
with Eid as (select teamid from teams where name='Everton'),
    awayteamids as (select distinct(awayteamid) from games where hometeamid in (select * from Eid)),
    hometeamids as (select distinct(hometeamid) from games where awayteamid in (select * from awayteamids) and hometeamid not in (select * from Eid)),
    gameids as (select gameid from games where hometeamid in (select * from hometeamids)),
    sumassists as (select playerid, sum(assists) as tassists from gameids inner join appearances on appearances.gameid = gameids.gameid group by playerid)
select name as playernames, tassists as assistscount from sumassists inner join players on players.playerid = sumassists.playerid where tassists in (select max(tassists) from sumassists) order by playernames;

--17--
with Aid as (select teamid from teams where name='AC Milan'),
    awayteamids as (select distinct(hometeamid) from games where awayteamid in (select * from Aid)),
    hometeamids as (select distinct(awayteamid) from games where hometeamid in (select * from awayteamids) and awayteamid not in (select * from Aid)),
    gameids as (select gameid from games where (awayteamid in (select * from hometeamids)) and year=2016),
    sumshots as (select playerid, sum(shots) as tshots from gameids inner join appearances on appearances.gameid = gameids.gameid group by playerid)
select name as playernames, tshots as shotscount from sumshots inner join players on players.playerid = sumshots.playerid where tshots in (select max(tshots) from sumshots) order by playernames;

--18--
with Aid as (select teamid from teams where name='AC Milan'),
    awayteamids as (select distinct(awayteamid) from games where hometeamid in (select * from Aid)),
    hometeamids as (select distinct(hometeamid) from games where awayteamid in (select * from awayteamids) and hometeamid not in (select * from Aid)),
    result as (select distinct awayteamid, year from games where (hometeamid in (select * from hometeamids)) and year=2020 and awaygoals=0)
select name as teamname, year from result inner join teams on teams.teamid = result.awayteamid order by teamname limit 5;

--19--
with game2019 as (select * from games where year=2019),
    hometeamgoals as (select leagueid, hometeamid, sum(homegoals) from game2019 group by leagueid, hometeamid),
    awayteamgoals as (select leagueid, awayteamid, sum(awaygoals) from game2019 group by leagueid, awayteamid),
    totalgoals as (select awayteamgoals.leagueid, hometeamid as teamid, hometeamgoals.sum+awayteamgoals.sum as tgoals
                     from hometeamgoals inner join awayteamgoals on 
                     hometeamgoals.leagueid = awayteamgoals.leagueid and hometeamid=awayteamid),
    ordered as (select *,ROW_NUMBER() OVER(partition by leagueid order by tgoals desc) as rn from totalgoals),
    topscorers as (select * from ordered where rn=1),
    awayteamids as (select distinct topscorers.leagueid, topscorers.teamid as teamid, tgoals as teamscore, game2019.awayteamid 
                     from game2019 inner join topscorers on topscorers.teamid = game2019.hometeamid),
    hometeamids as (select distinct awayteamids.leagueid, awayteamids.teamid, awayteamids.teamscore, game2019.hometeamid 
                     from game2019 inner join awayteamids on awayteamids.awayteamid = game2019.awayteamid
                     where game2019.hometeamid != awayteamids.teamid),
    gameids as (select distinct teamid, gameid from game2019, hometeamids where 
                (hometeamids.hometeamid = game2019.hometeamid 
                )),
    playerstemp as (select * from gameids inner join appearances on appearances.gameid = gameids.gameid),
    sumgoals as (select teamid, playerid, sum(goals) as tgoals from gameids inner join appearances on appearances.gameid = gameids.gameid group by teamid, playerid),
    temp as (select *, ROW_NUMBER() OVER(partition by teamid order by tgoals desc) AS rn from sumgoals),
    teamtopplayers as (select teamid, playerid, tgoals from temp where rn=1),
    output as (select leagueid, topscorers.teamid, topscorers.tgoals as teamscore, playerid, teamtopplayers.tgoals from teamtopplayers, topscorers where topscorers.teamid=teamtopplayers.teamid)
select leagues.name as leaguename, players.name as playernames, tgoals as playertopscore, teams.name as teamname, teamscore as teamtopscore from output inner join teams on output.teamid=teams.teamid 
inner join players on players.playerid = output.playerid
inner join leagues on leagues.leagueid = output.leagueid
order by playertopscore desc, teamtopscore desc, playernames;

--20--
with recursive Lid as (select teamid from teams where name='Manchester United'),
    Mid as (select teamid from teams where name='Manchester City'),
    journey(awayteamid, pathlength) as 
    (select distinct awayteamid, 1 as pathlength, array[hometeamid, awayteamid] as path 
        from games 
        where hometeamid in (select * from Lid)
    union all
    select g.awayteamid, j.pathlength+1, j.path || g.awayteamid
    from games g, journey j 
    where g.hometeamid=j.awayteamid and 
        g.awayteamid != all(j.path) 
    ),
    result as (select awayteamid, pathlength from journey where awayteamid in (select * from Mid))
select distinct max(pathlength) from result;

--21--
with recursive Lid as (select teamid from teams where name='Manchester United'),
    Mid as (select teamid from teams where name='Manchester City'),
    journey(awayteamid, pathlength) as 
    (select distinct awayteamid, 1 as pathlength, array[hometeamid, awayteamid] as path 
        from games 
        where hometeamid in (select * from Lid)
    union all
    select g.awayteamid, j.pathlength+1, j.path || g.awayteamid
    from games g, journey j 
    where g.hometeamid=j.awayteamid and 
        g.awayteamid != all(j.path) 
    ),
    result as (select awayteamid, pathlength from journey where awayteamid in (select * from Mid))
select count(*) from result;

--22--
with recursive
    journey as 
    (select distinct hometeamid, awayteamid, 1 as pathlength, leagueid, array[hometeamid, awayteamid] as path 
        from games 
    union all
    select distinct j.hometeamid, g.awayteamid, j.pathlength+1, g.leagueid, j.path || g.awayteamid
    from games g, journey j 
    where g.hometeamid=j.awayteamid and 
        g.awayteamid != all(j.path) and
        g.leagueid = j.leagueid
    ),
    leaguemaxpath as (select leagueid, max(pathlength) from journey group by leagueid),
    result as (select hometeamid, awayteamid, pathlength, leagueid from journey where (leagueid,pathlength) in (select * from leaguemaxpath))
select leagues.name as leaguename, t1.name as teamAname, t2.name as teamBname, pathlength as count from result, leagues, teams t1, teams t2 
    where leagues.leagueid = result.leagueid and
            t1.teamid = hometeamid and
            t2.teamid = awayteamid
order by count desc, teamAname, teamBname;