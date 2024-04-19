# EverBitica

This is an alternative interface for Habitica based on the GUI from the classic EverQuest client circa ~1999. I'm working on this project because I really enjoy Habitica and use it daily but also have a lot of nostalgia for Everquest. The richness of spells/skills/items/tradeskills available in the EverQuest universe will provide a lot more incentive/reward/progress than base Habitica by itself, which runs out of most content after around three months. 

This project's use of EverQuest images and text falls under [Fair Use](https://en.wikipedia.org/wiki/Fair_use) because this project is both commentary and parody by contrasting the completely useless time-suck of EverQuest with the productive and life-enriching habits tracked and encouraged by Habitica. It will also never generate income of any sort and generally has zero impact on the value and operation of the EverQuest franchise by its current owners. 

This alternative interface is a stand-alone Django web application and doesn't integrate directly with Habitica aside from API calls. 

### Dev

Run `docker "everbitica"` - there's a container for serving web app and one for postgres. 

Running `docker ps` in terminal can verify these are running. 


#### Setup, Migrating, and Seeding

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py seed_playerclass


#### Tests

 docker-compose exec web python manage.py test everbitica.tests.GetPartyMembersTest

#### Requirements Updates

Changes to requirements.txt to add libraries requires:

1. docker-compose build
2. docker-compose up


#### Importing Spells

The spells text file comes from Project1999 downloads. The headings for this CSV come from `Server/common/repositories/base/base_spells_new_repository.h` in https://github.com/EQEmu/Server/ ([direct link to code](https://github.com/EQEmu/Server/blob/82aa6a1587477e642e7ac44e7902f4568bb8563e/common/repositories/base/base_spells_new_repository.h#L19))

### To-Do

* Make current user name not show in party members
* Test current target for non-boss times and for collection question times
* Fix styling issues with scaling/resizing window
* Have it pull in habits and to-do items, be able to press them in UI
* Add options window
* Add webhooks to auto update (probably wait for React implementation for this)
* Create list of Youtube videos to embed along with timestamps to randomly start between
* Allow sending chat messages
* Show party members (scrolling or top 5?)
* Install React and transition HTML/CSS/JS to that
* Fix CSS/HTML for longer usernames
* Fix targeting for stuff like aprils fools events (since it's an event and not a quest, it was confusing how this is accessed in content.json since it's seemingly not there at all)
* Add auto-action options
    * Auto-heal 
    * Auto-buy healing potion
    * Auto-nuke
    * Auto quest accept
    * Auto chat pending boss damage
* Multi-nuke option
* Test for bugs when not in a party
* Lots more
