# EPL_Extract
Extract datasets for a football team of your choice, with various types of useful information, into Excel files.

<h2>Description</h2>
This script, in its current format takes your football team and year as input, and extracts all matches played by the team with relevant information, such as score, formations, lineups, and stats.
The project is in its most basic implementation sofar, but in the near future, I will be extracting events per match, including goals, assists, cards, and substitutions. Long-term, I hope to be able to extract more detailed statistics per match, as well as develop a user-friendly GUI.


<h2>Installation/Dependencies</h2>
<ul>
<li>Anaconda distribution of Python 3.7</li>
<li>Selenium library on Python and Chrome extension, to scrape websites (make sure you install the appropriate versions </li>
<li>xlsxwriter library on Python, to write information on Excel files</li>
 </ul>
  
 
<h2>Project Motivation</h2>
I wished to analyze the effect of frequent lineup changes made in Chelsea FC's early 2020-2021 season on their performance, but couldn't find online datasets that provided lineups for all matches all consolidated in one source. So, I sought out to create those datasets myself by web scraping and automation, and I kept expanding the scope from thereon to include this information for other teams and across different years.


<h2>Current Implementation/Future Steps</h2>
<ul>
The current implementation extracts, per match, the following information:
<li> Date </li>
<li> Competition</li>
<li> Scores, including xG or Penalties </li>
<li> Team Managers & Captains </li>
<li> Stats such as Passing, Shots, Possession </li>
<li> Formation & Lineups </li>
</ul>
