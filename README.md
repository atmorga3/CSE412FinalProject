# CSE412 Final Project 

## Competitive League of Legends Match Application
 
Created by - Group 17: 
Aidan Morgan | 
Liam Donnelly | 
Novilia Lioe | 
Junghwan Park

### Application Description
This application will visualize Competitive League of Legends win-rate, KDA, ban-rate, total CS, and role by champion or player. Data regarding the match, player, and champion will be able to be searched. 

Match data will store unique instances of matches in the system by an identifying match_id. Player data will store player names and identifying player ID’s. Similarly, Champion data will store champion names and champion ID’s.

A ternary relationship among Match, Player, and Champion will store relevant match data specific to the player and champion played such as win, team, total CS, kills, deaths, assists, and role. Because this is a ternary relationship, all three entity sets must be present to form a row for the Plays table, meaning a match cannot be played without both players and champions.

A Ban relationship connects a Match and 10 Champions with key and participation constraints that specify a match can ban several champions.

### Important Definitions
Ban: Before the match, each team takes turns banning champions preventing them from being played in the match. There are 10 ban's per match and a champion can only be banned once per match so a total of 10 bans happen every match.

average_cs: average creep score -- average amount of minions (creeps) killed

kda: kills deaths assists -- calculated by (kills + assists)/deaths

average_win_rate: % of wins vs losses

average_ban_rate: % of games it was banned
