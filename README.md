# Stratagem Picker

A simple tool for randomizing your Helldivers 2 game.

This tool allows you to randomly select your loadout for Helldivers 2, including primary and secondary weapons, grenades, stratagems, and a booster. You can re-roll each item individually or all at once, and lock specific items to keep them fixed during re-rolls.

Note that I have a quite poor overview of the total item pool, so if I have forgotten anything, mixed up the warbonds in any way, or made any other mistakes, please let me know!

The tool consists of this SvelteKit project, which contains the web page, including item thumbnails and a json file describing the items. In addition, there is a Python script ([weapon-extractor](weapon-extractor)) that fetches item information from [helldivers.wiki.gg](https://helldivers.wiki.gg), which is meant to be run once in a while to download information about new items.

An up-to-date instance of the tool is hosted at [stratagems.erlenddahl.no](https://stratagems.erlenddahl.no).

## Disclaimer
This project is not affiliated with Arrowhead Game Studios or Sony Interactive Entertainment. All weapon and stratagem images, names, and related media are the property of their respective owners.

## Development

To run and develop this project locally:

1. Clone the repository.
2. Open the project folder in [Visual Studio Code](https://code.visualstudio.com/).
3. Run `npm install` to install dependencies.
4. Start the development server with `npm run dev`.
5. Build (and optionally preview) with `npm run build` and `npm run preview`

**Pull requests are very welcome! If you have suggestions or improvements, feel free to fork the repo and open a PR.**