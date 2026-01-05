WHAT I DID IN THIS AGENT - 

1.	i build scanners/ which have basically 3 steps of scanning, sast scanning, dependency scanning and secret scanning. sast/ dependency/ and secret-scanning/ for sast i have used bandit, for dependency scanning i have used OSV and for secret scanning i have used trufflehog. 
2.	i have core/models.py which gives the schema for the input and output data. 
3.	the code for now, when you give the repository link in the main.py file, it clones the repo in tmp/ folder [you would have to create the tmp/ folder manually if you clone it], performs the necessary scan and then cleans the clone of the repo from tmp/ folder creating a separate blackbox for scanning. The process of repository cloning and cleanup is stored in core/repo_manager.py
4.	we then define a UnifiedFinding basemodel which basically uniforms the response of these scanners into one output and cleans any noise created by any of the scanners. 
5.	Noise suppression - the folder normalizers/ basically removes noise from each scanners and makes a uniform output. 
6.	I now have risk engine which takes all the risk findings and based on that it gives you the score of the repository. you can add the rules of that risk rating score and if the rating is greater than 500 it gives the status as FAIL and FAILS the repository as a safe one. it is mentioned in engine/risk_rating.py
