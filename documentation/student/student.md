<div class="row center">
    <div class="container center display-container col-md-offset-1 col-md-10">
        <h1 class="headings row left">Student Documentation</h1>
        <h2 class="headings row left">Terminology</h2>		
		<div class="row left">
			<ul>
				<li><strong>Player</strong>: A file of code submitted by a user to play in a specific contest (which can contain many tournaments)</li>
				<li><strong>Tournament</strong>: A competition between two or more players. The competition consists of a series of matches between various players</li>	
				<li><strong>Match</strong>: The overarching result of rounds played between two or more players. Matches contain at least one round, but can contain more depending on what the instructor or challenger decides</li>
				<li><strong>Round</strong>: One specific instance within a match. For example, a single game of checkers, or a single game of risk. However many rounds are set by either the instructor or the challenger determines how many rounds there are in a match. Whoever has the majority of rounds won determines who wins the overall match</li>
				<li><strong>Referee</strong>: A program submitted by an instructor that defines the rules of matches played within contests and enforces those rules</li>
				<li><strong>Contest</strong>: This is what ties the Game Contest Server together. A contest is a container of tournaments and players. For example, an instructor may set up a contest for a specific semester class. Within this contest, students will upload their player files to it, which allows the instructor to then set up tournaments to be played with the various players submitted. Also, players can challenge other players from the same contest if they want to see how they compare to another player specifically</li>	
				<li><strong>Challenge Match</strong>: A match between two or more players from the same contest that a student can set up independently from an instructor to compare their players with other players</li>	
			</ul>
		</div>
		<h2 class="headings row left">Terminology Dependencies</h2>		
		<h4>Round -> Match/Challenge Match -> Tournament and Players -> Contest -> Referee</h4>
		<div class="row left">
			<ul>
				<li><strong>Referee</strong>: Does not need anything!</li>
				<li><strong>Contest</strong>: Needs a Referee</li>	
				<li><strong>Tournament</strong>: Needs a Contest</li>	
				<li><strong>Player</strong>: Needs a Contest</li>
				<li><strong>Match</strong>: Needs a Tournament and multiple Players</li>
				<li><strong>Challenge Match</strong>: Needs multiple Players</li>	
				<li><strong>Round</strong>: Needs a Match or a Challenge Match</li>
			</ul>
		</div>
		<h2 class="headings row left">Student Capabilities</h2>		
		<div class="row left">
			<ul>
				<li>Uploading Players to a specific Contest</li>
				<li>Challenging Players to a specific Contest</li>
				<li>Viewing all results from Tournaments and Challenge Matches</li>				
			</ul>
		</div>
	</div>
</div>