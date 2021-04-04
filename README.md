# EPL_Extract
Extract datasets for a football team of your choice, with various types of useful information, into Excel files.

<h2>Description</h2>
This script, in its current format takes your football team and year as input, and extracts all matches played by the team with relevant information, such as score, formations, lineups, and stats.
The project has only been updated twice since its creation, but in the near future, I will be extracting more detailed events per match. Long-term, I hope to be able to extract more detailed statistics per match, as well as develop a user-friendly GUI.


<h2>Installation/Dependencies</h2>
<ul>
<li>Anaconda distribution of Python 3.7</li>
<li>Selenium library on Python and Chrome extension, to scrape websites (make sure you install the appropriate versions </li>
<li>xlsxwriter library on Python, to write information on Excel files</li>
<li>Pandas library on Python, for stats tables and future computations</li>
<li> fbref website, as a source for all stats </li>
 </ul>
  
 
<h2>Project Motivation</h2>
I wished to analyze the effect of frequent lineup changes made in Chelsea FC's early 2020-2021 season on their performance, but couldn't find online datasets that provided lineups for all matches consolidated in one source. So, I sought out to create those datasets myself by web scraping and automation, and I kept expanding the scope from thereon to include this information for other teams and across different years.


<h2>Current Implementation/Future Steps</h2>

The current implementation extracts, per match, the following information:
<ul>
<li> Date </li>
<li> Competition</li>
<li> Scores, including xG or Penalties </li>
<li> Team Managers & Captains </li>
<li> Stats such as Passing, Shots, Possession </li>
<li> Formation & Lineups </li>
<li> (new) Stats per player per team, on different sheets </li>
</ul>

In the near future, I hope to implement the following:
<ul>
 <li> Extract various match events </li>
 <li> Refactor the working basic code into a working object oriented programming code (done!) </li>
 <li> Adding more features for dataset generation, e.g. get all formations in one file, or generate stats per player in a team (partially done!) </li>
 <li> Creating a GUI for the project that takes few variables as input rather than have people edit code </li>
 </ul>
 
![image](https://user-images.githubusercontent.com/40544032/111081600-b81de200-850c-11eb-89cc-73f87489064f.png)
 

![image](https://user-images.githubusercontent.com/40544032/111081731-6d509a00-850d-11eb-81b5-974da193b469.png)

 ![image](https://user-images.githubusercontent.com/40544032/111081833-e51ec480-850d-11eb-80fa-993d95f1fe22.png)

