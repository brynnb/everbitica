# EverBitica

![image](https://github.com/brynnb/everbitica/assets/1271817/d39130dc-a92e-4475-9db6-86e8d2e67aae)

This is an alternative interface for Habitica based on the GUI from the classic EverQuest client circa ~1999. I'm working on this project because I really enjoy Habitica and use it daily but also have a lot of nostalgia for Everquest. The richness of spells/skills/items/tradeskills available in the EverQuest universe will provide a lot more incentive/reward/progress than base Habitica by itself, which runs out of most content after around three months.

This project's use of EverQuest images and text falls under [Fair Use](https://en.wikipedia.org/wiki/Fair_use) because this project is both commentary and parody by contrasting the completely useless time-suck of EverQuest with the productive and life-enriching habits tracked and encouraged by Habitica. It will also never generate income of any sort and generally has zero impact on the value and operation of the EverQuest franchise by its current owners.

This alternative interface is a stand-alone Django web application and doesn't integrate directly with Habitica aside from API calls.

### Dev

Run `docker "everbitica"` - there's a container for serving web app and one for postgres.

Running `docker ps` in terminal can verify these are running.

docker-compose exec web python manage.py shell

#### Setup, Migrating, and Seeding

EQ seeding needs to happen first so that it doesn't wipe out eq_ prefixed tables from Django migrations:

docker-compose exec web python manage.py seed_eq_data_tables 

docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py seed_additional_eq_data

#### Tests

docker-compose exec web python manage.py test

#### Requirements Updates

Changes to requirements.txt to add libraries requires:

1. docker-compose build
2. docker-compose up


### To-Do

- Write a utility to go through all imported EQ data and try to create an object instance with it see if it causes an error - this would catch any issues that would have come up converting the EQ database information into Django models
- Make current user name not show in party members
- Have pending bosses have "Pending:" in front of target name, or maybe not display at all
- Add options window
- Add webhooks to auto update (probably wait for React implementation for this)
- Allow sending chat messages
- Install React and transition HTML/CSS/JS to that
- Fix targeting for stuff like aprils fools events (since it's an event and not a quest, it was confusing how this is accessed in content.json since it's seemingly not there at all)
- Add auto-action options
  - Auto-heal
  - Auto-buy healing potion
  - Auto-nuke
  - Auto quest accept
  - Auto chat pending boss damage
- Multi-nuke option
- Test for bugs when not in a party
- Lots more

### Probably Not Doing Any Time Soon
- Pull in habits and to-do items, be able to press them in UI - recreating this is a lot of work for not much return, easy enough to mark off on actual Habitica website 

### Resources

- [EQEmu post on "Default EverQuest Melee Combat Routines Analyzed and Modeled"](https://www.eqemulator.org/forums/showthread.php?t=40543) - this is probably useful for programming combat logic in the future
- Similar one on NPC attack rates: https://www.eqemulator.org/forums/showthread.php?t=38734
  EQMechanics repo on github: https://github.com/mackal/EQMechanics/wiki/Some-Vanilla

### Notes

- NPC attack rate should be 3 seconds for everything under level 25. This is good enough for me for this project. It's maybe only Kunark where it even changes after level 25.
