# Post Joint Hackathon 2024

Hackathon was a success!  A big shout to all participants, and from EERIE side, particularly postdocs who led breakout groups (Fraser Goldsworth, Matthias Aengenheyster, Aaron Wienkers), simulation data and examples preppers (Rohit Ghosh, Fabian Wachsmann, Matthias Aengenheyster, Jürgen Kröger, Nikolay Koldunov), tech support (Kamesh Modali, Florian Ziemen), and +++ . A big thanks also to NextGEMS team as well (Johann Jungclaus, Arjun Kumar, Karl-Hermann Wieners, Heike Konow, Thomas Rackow, +++)  Sorry, I'm bound to have missed out people who also deserve so much gratitude. 

Many things slow down post-hackathon, so before it fizzles out and with the hackathon still fresh in mind, we have **two requests** from the hackathon participants. Additionally, there's also a preliminary **collection of material** from the hackathon that might be of interest or useful for people. 

**Requests**
1)  To participants willing to share their scripts, notebooks, figures, to please upload them to [StormsOceanBOGplots folder](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/results_hamburg_hackathon_2024/StormsOceanBOGplots) for figures or slides, and [notebooks folder](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/results_hamburg_hackathon_2024/notebooks) for scripts and notebooks you may have created pre/during/post hackathon. Please don't forget to make a pull request when you've uploaded material. If you have issues, please contact Nikolay or Dian. 
2) Feedback (likes, dislikes, neutral) from the hackathon on technical, scientific, logistical, miscellaneous are extremely welcomed. Please provide them on [this google doc](https://docs.google.com/document/d/1Y9oTEQ4vZicsjnJ4buEOvGeavqp8BgTi-kiwmSzlBds/edit)


**Collection of material on [EERIE github repo](https://github.com/eerie-project/EERIE_hackathon_2023/tree/main/results_hamburg_hackathon_2024)**
- [Slides and figures in this repo](StormsOceanBOGplots) from the breakout groups of Storms & Ocean (nextGEMS) and EERIE
  - [Owncloud folder](https://owncloud.gwdg.de/index.php/s/z3pHKrPkqSvLeJc) hosting slides from S&O breakout groups
- Slides from opening plenary session hosted on [Owncloud](https://owncloud.gwdg.de/index.php/s/uTnNx02YuENDwYT?path=%2Fopening). File sizes too big to be placed on this repo.
- [Slides and figures in this repo](ClosingPlenary) from the closing plenary session (includes hackathon pictures!)
  - [Owncloud folder](https://owncloud.gwdg.de/index.php/s/uTnNx02YuENDwYT?path=%2F) hosting slides from hackathon plenary sessions

- IFS-AMIP: spatial scale dependency of air-sea coupling by Matthias Aengenheyster. Methodology, notebooks and scripts can be found [here](../pre-joint-hackathon-2024/mesoscale-air-sea-coupling/IFS-FESOM/README.md).
- Other example notebooks for scientific analysis created before the hackathon can be found [here](../pre-joint-hackathon-2024/README.md).

- Data viewers
  - Interactive variable browser by Fabian Wachsmann: [https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_view-and-access.html](https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_view-and-access.html)
  - Interactive animation viewer by Fabian Wachsmann: [https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_gr025_interactive-animation.html](https://swift.dkrz.de/v1/dkrz_7fa6baba-db43-4d12-a295-8e3ebb1a01ed/apps/eerie-cloud_gr025_interactive-animation.html)
  - Interactive climatology and model difference [explorer](notebooks/IFS_AMIP_explorer.ipynb) by Markel Garcia-Diez

- EERIE related details on [easygems](https://easy.gems.dkrz.de/simulations/EERIE/index.html#), particularly for accessing EERIE data on Levante. 
- [Python environment used in the hackathon](BuildPyEnv.md)
  
- [Starter pack pad](StarterPackPad.md) translated to markdown file in this repo. 
  - [Hackathon Starter Pack](StarterPackPad.md#hackathon-starter-pack)
    * [Links to relevant documents](StarterPackPad.md#links-to-relevant-documents)
    * [Using the Levante Supercomputer](StarterPackPad.md#using-the-levante-supercomputer)
      + [DKRZ User account for data access](StarterPackPad.md#dkrz-user-account-for-data-access)
      + [Jupyterhub](StarterPackPad.md#jupyterhub)
      + [Python environments](StarterPackPad.md#python-environments)
      + [Building python environment](StarterPackPad.md#building-python-environment)
        - [Easiest option (pre-made python env for hackathon)](StarterPackPad.md#easiest-option-pre-made-python-env-for-hackathon)
      + [CDO Versions](StarterPackPad.md#cdo-versions)
      + [General documentation](StarterPackPad.md#general-documentation)
  - [Simulation Overview](StarterPackPad.md#simulation-overview)
    * [NextGEMS](StarterPackPad.md#nextgems)
      + [ICON](StarterPackPad.md#icon)
        - [prefinal](StarterPackPad.md#prefinal)
        - [pre-prefinal experiments **(volatile data)**](StarterPackPad.md#pre-prefinal-experiments-zapvolatile-data)
        - [Terms and conditions](StarterPackPad.md#terms-and-conditions)
      + [Basic notes on HEALpix](StarterPackPad.md#basic-notes-on-healpix)
    * [EERIE](StarterPackPad.md#eerie)
  - [Working with the data](StarterPackPad.md#working-with-the-data)
    * [Reading in the data](StarterPackPad.md#reading-in-the-data)
      + [NextGEMS (data access via intake)](StarterPackPad.md#nextgems-data-access-via-intake)
      + [EERIE (data access via intake)](StarterPackPad.md#eerie-data-access-via-intake)
      + [EERIE (data access on shell environment for cdo operations)](StarterPackPad.md#eerie-data-access-on-shell-environment-for-cdo-operations)
    * [Example notebooks on some scientific analysis](StarterPackPad.md#example-notebooks-on-some-scientific-analysis)
  - [Hackathon breakout groups](StarterPackPad.md#hackathon-breakout-groups)
    * [Storms&Ocean](StarterPackPad.md#stormsocean)
    * [Storms&Radiation](StarterPackPad.md#stormsradiation)
    * [Storms&Land](StarterPackPad.md#stormsland)
 

