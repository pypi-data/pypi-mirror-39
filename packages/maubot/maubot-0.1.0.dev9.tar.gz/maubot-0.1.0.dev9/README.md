# maubot
A plugin-based [Matrix](https://matrix.org) bot system written in Python.

Management API spec: [maubot.xyz/spec](https://maubot.xyz/spec)

### [Wiki](https://github.com/maubot/maubot/wiki)

## Discussion
Matrix room: [#maubot:maunium.net](https://matrix.to/#/#maubot:maunium.net)

### Development setup
0. Clone the repo (`git clone https://github.com/maubot/maubot.git`)
1. (Optional) Create a virtualenv (`virtualenv -p python3.6 .venv` and `source .venv/bin/activate`)
2. Install dependencies (`pip install -r requirements.txt`)
3. Compile the frontend
   0. Install [Node.js](https://nodejs.org/en/) and Yarn (`npm install --global yarn`)
   1. `cd maubot/management/frontend`
   2. `yarn`
   3. `yarn build`
4. Copy `example-config.yaml` to `config.yaml` and fill it in
5. Start with `python -m maubot`
6. Browse to the management interface

## Plugins
* [jesaribot](https://github.com/maubot/jesaribot) - A simple bot that replies with an image when you say "jesari".
* [sed](https://github.com/maubot/sed) - A bot to do sed-like replacements.
* [factorial](https://github.com/maubot/factorial) - A bot to calculate unexpected factorials.
* [media](https://github.com/maubot/media) - A bot that replies with the MXC URI of images you send it.
* [dice](https://github.com/maubot/dice) - A combined dice rolling and calculator bot.
* [karma](https://github.com/maubot/karma) - A user karma tracker bot.
* [xkcd](https://github.com/maubot/xkcd) - A bot to view xkcd comics.
* [echo](https://github.com/maubot/echo) - A bot that echoes pings and other stuff.
* [rss](https://github.com/maubot/rss) - A bot that posts RSS feed updates to Matrix.

### Upcoming
* dictionary - A bot to get the dictionary definitions of words.
* poll - A simple poll bot.
* reminder - A bot to ping you about something after a certain amount of time.
* github - A GitHub client and webhook receiver bot.
* wolfram - A Wolfram Alpha bot
* gitlab - A GitLab client and webhook receiver bot.
