# EverBitica

This is an alternative interface for Habitica based on the GUI from the classic EverQuest client circa ~1999. I'm working on this project because I really enjoy Habitica and use it daily but also have a lot of nostalgia for Everquest. The richness of spells/skills/items/tradeskills available in the EverQuest universe will provide a lot more incentive/reward/progress than base Habitica by itself, which runs out of most content after around three months. 

This project's use of EverQuest images and text falls under [Fair Use](https://en.wikipedia.org/wiki/Fair_use) because this project is both commentary and parody by contrasting the completely useless time-suck of EverQuest with the productive and life-enriching habits tracked and encouraged by Habitica. It will also never generate income of any sort and generally has zero impact on the value and operation of the EverQuest franchise by its current owners. 

### Dev

Run `docker "everbitica"` - there's a container for serving web app and one for postgres. 

Running `docker ps` in terminal can verify these are running. 


#### Setup, Migrating, and Seeding

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py seed_playerclass


#### Requirements Updates

Changes to requirements.txt to add libraries requires:

1. docker-compose build
2. docker-compose up


#### Importing Spells

The spells text file comes from Project1999 downloads. The headings for this CSV come from `Server/common/repositories/base/base_spells_new_repository.h` in https://github.com/EQEmu/Server/ ([direct link to code](https://github.com/EQEmu/Server/blob/82aa6a1587477e642e7ac44e7902f4568bb8563e/common/repositories/base/base_spells_new_repository.h#L19))

### To-Do

* Get "Current Target" UI element to show current boss or collection quest name
* Allow sending chat messages
* Show party members (scrolling or top 5?)
* Install React and transition HTML/CSS/JS to that
* Lots more
