# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/
#PredictedRMSE = (-1.18808+ 0.322101*T^1.2964)NumberOfGames^(0.186474*D^0.086981*(1-3.3364/(T^0.778216*G^0.077255)))  #formula from research conducted by Jacob Bernard, Kyle Shelton, Daniel Grube
 
cConstant = -1.18808
cNumPlayersCoefficient = 0.322101
cNumPlayersExponent = 1.2964
bDisparityCoefficient = .186474
bDisparityExponent = .086981
bNumerator = 3.3364
bNumPlayersExponent = .778261
bNumPlayersPerGame = .077255



window.onload = () -> (   
   setupForMultiplayerElements() 
   attachListeners()
)

setupForMultiplayerElements = () -> (
   matchTypeSelector = getMatchTypeSelector()
   totalMatchesDiv = getTotalMatchesDiv()
   disparityDiv = getDisparityDiv()
   if matchTypeSelector.value == "round robin"
    disparityDiv.removeAttribute("hidden")
    totalMatchesDiv.removeAttribute("hidden")
   else
    disparityDiv.setAttribute("hidden", true) 
    totalMatchesDiv.setAttribute("hidden", true)
)

getDisparityDiv = () -> (
   disparityInput = document.getElementById("tournament_expected_disparity")
   disparityInputFather = disparityInput.parentNode
)

getTotalMatchesDiv = () -> (
   totalMatchesInput = document.getElementById("tournament_total_matches")
   totalMatchesFather = totalMatchesInput.parentNode
)

getMatchTypeSelector = () -> (
   document.getElementById('tournament_tournament_type')
)

getNumberOfPlayers = () -> (
   playerNumberHolder =  document.getElementById('rightValues')
   playerNumberHolder.length
)

numberOfPlayersChange = () -> (
  console.log(calculateNumberOfMatchesToPlay())
)

getNumberOfPlayersPerGame = () -> (
  4
)

getDisparity = () -> (
  1000
)

calculateNumberOfMatchesToPlay = (RMSE) -> ( 
  #PredictedRMSE = (-1.18808+ 0.322101*T^1.2964)NumberOfGames^(0.186474*D^0.086981*(1-3.3364/(T^0.778216*G^0.077255)))  #formula from research conducted by Jacob Bernard, Kyle Shelton, Daniel Grube
  disparity = getDisparity()
  numberOfPlayers = getNumberOfPlayers()
  numberOfPlayersPerGame = getNumberOfPlayersPerGame()
  firstPartOfTheTerm = bDisparityCoefficient*Math.pow(disparity, bDisparityExponent)

  secondPartOfTheTerm = bNumerator/(Math.pow(numberOfPlayers, bNumPlayersExponent)*Math.pow(numberOfPlayersPerGame, bNumPlayersPerGame))
  b = 1/(firstPartOfTheTerm*(1-secondPartOfTheTerm))
  b
)

attachListeners = () -> (
   matchType = getMatchTypeSelector()
   matchType.addEventListener("click", setupForMultiplayerElements)
   rightButton = document.getElementById('btnRight')
   leftButton  = document.getElementById('btnLeft')
   rightButton.addEventListener('click', numberOfPlayersChange)
   leftButton.addEventListener('click', numberOfPlayersChange)
)
