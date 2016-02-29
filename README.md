# Zeitgeist Borders

Research Paper : <https://hal.inria.fr/hal-00805048/document>

Review by New Scientist : <https://www.newscientist.com/blogs/onepercent/2013/04/zeitgeist-borders-google.html>

**Zeitgeist Borders enable you to map suggestions from all Google search domains over a world map.**

By passing your mouse over a country you get the list of all related suggestions:

![Map Interaction](https://raw.github.com/fabelier/Zeitgeist-Borders/master/documentation/map_zeitgeist.jpg)

By passing your mouse over a suggestion you see all the related countries being highlighted on the map:

![List Interaction](https://raw.github.com/fabelier/Zeitgeist-Borders/master/documentation/menu_zeitgeist.jpg)

Add a space after the last word of your query if you don't want Zeitgeist Borders to suggests you completion of the single last word instead of completion of your whole query.

# License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Installing Zeitgeist Borders

We couldn't make an online service because of the Google's limitation on the number of query on their servers, but still you can install it on your computer with a little bit of patience. Install [Python](http://www.python.org/) and follow the steps described above. It's worth it, it's a pretty funny and addictive tool ! :)

## Dependencies

In order to use Zeitgeist Borders you must have [Python](http://www.python.org/download/releases/2.7/) installed with the following dependencies: 

+ [Pyramid](http://docs.pylonsproject.org/projects/pyramid/en/latest/index.html)
+ [PyMongo](http://api.mongodb.org/python/current/)
+ [Paste](http://pythonpaste.org/)

All of them are available through [`easy_install`](http://pypi.python.org/pypi/setuptools):

	sudo pip install pyramid
	sudo pip install pyramid_mako
	sudo pip install pymongo
	sudo pip install paste

## Installation and usage

Open a terminal and download Zeitgeist Borders:

	git clone git://github.com/fabelier/Zeitgeist-Borders.git

Move to the application's folder:

	cd Zeitgeist-Borders/

Launch the server:

	python ./http.py

Browse the application's page by typing the following address into your Browser:

	http://127.0.0.1:8080/

# About

This software was developed at [Fabelier](http://fabelier.org), a parisian hackerspace, by:

+ [Antoine Mazières](https://github.com/mazieres), PhD Candidate at [INRA-Sens](http://www.inra-ifris.org/) and [LIAFA](http://www.liafa.jussieu.fr/).
+ [Samuel Huron](https://github.com/cybunk), PhD Candidate at [Aviz](http://www.aviz.fr/) and lead designer at [IRI](http://www.iri.centrepompidou.fr/).
+ [Julien Palard](https://github.com/JulienPalard), CTO of [Melty](http://www.meltynetwork.fr/).

Feel free to contact them at `zeitgeist at fabelier dot org` or to chat about this project on [Fabelier's mailing-list](https://groups.google.com/forum/?hl=en&fromgroups#!forum/fabelier).
