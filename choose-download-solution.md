# Decision record for downloading data once per day problem

**Issue**: Now the App unnecessarily calls TMDb API very often, it’s needed to change structure of some modules in order to limit API calls to 1 call per day

**Decision**: Implementation of Cron Tab
Status: Waiting from Noemi’s blessing

**Assumptions**: the implementation of Cron Tab will allow us to schedule 1 call to TMDb API and get all data from it. Next, this data will be stored locally (using SQLAlchemy or other tool) and served directly to the client. This will increase performance of the application. Moreover, it makes the app more independent from API and in consequence - less prone to bugs caused by external tool.

**Constraints**: the main developer (Magda) has never used Cron Tab before so some unforeseen issues might come up. Moreover, Magda has no experience working with big data set and isn’t sure is SQLite and SQLAlchemy will be enough to handle data traffic. Thus, additional changes may come up later.

**Positions**: The main opponent of Cron Tab in the research was Advanced Python Scheduler (APS).

**Argument**: Cron Tab is easier to set up and use, than APS. Moreover, it has a special version for the Flask application, which is a framework used in this project. However, the most important thing to consider is the fact that Cron Tab has a big community, which will be crucial when handling bugs and errors, especially considering the lack of Magda’s experience.

**Conclusion**: Cron Tab is the best solution for now but some additional challenges regarding data handling might come back later.
