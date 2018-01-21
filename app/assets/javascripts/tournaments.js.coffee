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
bNumPlayersPerGameExponent = .077255
RMSEPhraseList = ["Very sure", "Pretty sure", "Sure", "Unsure", "Pretty unsure", "Very unsure"]


window.onload = () -> (   
   setupForMultiplayerElements() 
   attachListeners()
)

setupForMultiplayerElements = () -> (
   matchTypeSelector = getMatchTypeSelector()
   multiplayerDiv = document.getElementById("multiplayerAssets")
   if matchTypeSelector.value == "multiplayer game"
     multiplayerDiv.removeAttribute("hidden")
   else
     multiplayerDiv.setAttribute("hidden", true)
)

getDisparityDiv = () -> (
   disparityInput = getDisparityInput()
   if disparityInput != null
    disparityInputFather = disparityInput.parentNode
)

getDisparityInput = () -> (
   disparityInput = document.getElementById("tournament_expected_disparity")
)

getTotalMatchesDiv = () -> (
   totalMatchesInput = getTotalMatchesInput()
   if totalMatchesInput != null
    totalMatchesFather = totalMatchesInput.parentNode
)

getTotalMatchesInput = () -> (
   totalMatchesInput = document.getElementById("tournament_total_matches")
)

getMatchTypeSelector = () -> (
   document.getElementById('tournament_tournament_type')
)

getNumberOfPlayers = () -> (
   playerNumberHolder =  document.getElementById('rightValues')
   playerNumberHolder.length 
)

getTotalTimeInput = () -> (
  document.getElementById("tournament_total_time") 
)

getUncertaintyInput = () -> (
  document.getElementById("tournament_RMSE")
)

RMSEConditionChange = () -> (
  getDisparity()
  getNumberOfPlayers()
  totalMatchesChange() 
)

totalMatchesChange = () -> (
  totalMatchesInput = getTotalMatchesInput()
  totalMatches = totalMatchesInput.value
  totalTimeInput = getTotalTimeInput()
  totalUncertaintyInput = getUncertaintyInput()
  totalTime = calculateMaxTimeFromNumMatches(totalMatches)
  RMSE = calculateRMSE(totalMatches)
  totalTime = vetOutput(totalTime)
  totalTime = convertSecondsToHours(totalTime)
  RMSE = vetOutput(RMSE)
  phrase = convertRMSEToPhrase(RMSE)
  totalTimeInput.value = totalTime
  totalUncertaintyInput.value = phrase
)

totalTimeChange = () -> (
  totalMatchesInput = getTotalMatchesInput()
  totalTimeInput = getTotalTimeInput()
  totalUncertaintyInput = getUncertaintyInput()
  totalTime = convertHoursToSeconds(totalTimeInput.value)
  totalMatches = calculateTotalMatchesFromTime(totalTime)
  RMSE = calculateRMSE(totalMatches)
  totalMatches = vetOutput(totalMatches)
  RMSE = vetOutput(RMSE)
  totalMatchesInput.value = totalMatches
  phrase = convertRMSEToPhrase(RMSE)
  totalUncertaintyInput.value = phrase
)

totalUncertaintyChange = () -> (
  totalMatchesInput = getTotalMatchesInput()
  totalTimeInput = getTotalTimeInput()
  totalUncertaintyInput = getUncertaintyInput()
  RMSE = convertPhraseToRMSE(totalUncertaintyInput.value)
  totalMatches = calculateNumberOfMatchesToPlay(RMSE)
  totalTime = calculateMaxTimeFromNumMatches(totalMatches)
  totalMatches = vetOutput(totalMatches)
  totalTime = vetOutput(totalTime)
  totalTime = convertSecondsToHours(totalTime)
  totalMatchesInput.value = totalMatches
  totalTimeInput.value = totalTime
)

vetOutput = (output) ->(
  vettedOutput = Math.floor(output)
  return vettedOutput
)

convertSecondsToHours = (seconds) ->(
  hours = seconds/3600
  return hours
)

convertHoursToSeconds = (hours) ->(
  seconds = hours*3600
  return seconds
)

convertRMSEToPhrase = (RMSE) ->(
  phrase = "???"
  if RMSE <=1 
    phrase = RMSEPhraseList[0]
  else if RMSE <=2
    phrase = RMSEPhraseList[1]
  else if RMSE <= 4
    phrase = RMSEPhraseList[2]
  else if RMSE <= 8
    phrase = RMSEPhraseList[3]
  else if RMSE <= 16
    phrase = RMSEPhraseList[4]
  else
    phrase = RMSEPhraseList[5]
  return phrase
)

convertPhraseToRMSE = (phrase) -> (
  RMSE = 0
  if phrase == RMSEPhraseList[0]
    RMSE = 1
  else if phrase == RMSEPhraseList[1]
    RMSE = 2
  else if phrase == RMSEPhraseList[2]
    RMSE = 4
  else if phrase == RMSEPhraseList[3]
    RMSE = 8
  else if phrase == RMSEPhraseList[4]
    RMSE = 16
  else if phrase == RMSEPhraseList[5]
    RMSE = 100
  else
    RMSE = 1000
  return RMSE
)

calculateTotalMatchesFromTime = (time) -> (
  timePerMatch = getMaxTimePerMatch()
  totalMatches = time/timePerMatch
  totalMatches = Math.floor(totalMatches)
)

getNumberOfPlayersPerGame = () -> (
  numPlayersPerGame = playersPerGame ##retreived from the associated HTML file
  numPlayers = getNumberOfPlayers()
  if numPlayersPerGame >= numPlayers
    numPlayersPerGame = numPlayers
  return numPlayersPerGame
)

getDisparity = () -> ( 
  #WARNING: disparity is currently being calculated as if players were evenly distributed amongst a range of skills, while the formula to calculate RMSE assumes normal distribution
  #values generated using an ELO calculator                  
  numPlayers = getNumberOfPlayers()
  disparityInput = getDisparityInput()
  disparityString = disparityInput.value
  if disparityString == "Very small"
    eloDifferenceBetweenConsecutivePlayers = 14
  else if disparityString == "Small"
    eloDifferenceBetweenConsecutivePlayers = 35
  else if disparityString == "Medium small"
    eloDifferenceBetweenConsecutivePlayers = 108
  else if disparityString == "Medium"
    eloDifferenceBetweenConsecutivePlayers = 191 
  else if disparityString == "Medium large"
    eloDifferenceBetweenConsecutivePlayers = 301
  else if disparityString == "Large"
    eloDifferenceBetweenConsecutivePlayers = 512
  else if disparityString == "Very large"
    eloDifferenceBetweenConsecutivePlayers = 798
  else
    eloDifferenceBetweenConsecutivePlayers = 0
  disparityRange = eloDifferenceBetweenConsecutivePlayers*(numPlayers-1)
  if disparityRange <= 0
    disparityRange = 0
  return disparityRange
)

calculateNumberOfMatchesToPlay = (RMSE) -> ( 
  #PredictedRMSE = (-1.18808+ 0.322101*T^1.2964)NumberOfGames^(0.186474*D^0.086981*(1-3.3364/(T^0.778216*G^0.077255)))  #formula from research conducted by Jacob Bernard, Kyle Shelton, Daniel Grube
  disparity = getDisparity()
  numberOfPlayers = getNumberOfPlayers()
  numberOfPlayersPerGame = getNumberOfPlayersPerGame()
  firstPartOfTheTerm = bDisparityCoefficient*Math.pow(disparity, bDisparityExponent)
  secondPartOfTheTerm = bNumerator/(Math.pow(numberOfPlayers, bNumPlayersExponent)*Math.pow(numberOfPlayersPerGame, bNumPlayersPerGameExponent))
  b = -(firstPartOfTheTerm*(1-secondPartOfTheTerm))
  c = cConstant + cNumPlayersCoefficient*(Math.pow(numberOfPlayers, cNumPlayersExponent))
  numMatchesToPlay = Math.pow((RMSE/c),1/b)
  if numMatchesToPlay <= 0 or isNaN(numMatchesToPlay)
    return 0
  return numMatchesToPlay
)

calculateMaxTimeFromNumMatches = (numMatches) -> (
  predictedTimePerMatch = getMaxTimePerMatch()
  return numMatches*predictedTimePerMatch
)

getMaxTimePerMatch = () -> (
  timePerMatch = maxTimePerMatch #retreived from HTML
  return timePerMatch 
)

calculateRMSE = (numMatchesToPlay) -> (
  disparity = getDisparity()
  if disparity == 0 
    return 0  
  numberOfPlayers = getNumberOfPlayers()
  numberOfPlayersPerGame = getNumberOfPlayersPerGame()
  firstPartOfTheTerm = bDisparityCoefficient*Math.pow(disparity, bDisparityExponent)
  secondPartOfTheTerm = bNumerator/(Math.pow(numberOfPlayers, bNumPlayersExponent)*Math.pow(numberOfPlayersPerGame, bNumPlayersPerGameExponent))
  b = -1*(firstPartOfTheTerm*(1-secondPartOfTheTerm))
  c = cConstant + cNumPlayersCoefficient*(Math.pow(numberOfPlayers, cNumPlayersExponent))
  RMSE = c*Math.pow(numMatchesToPlay, b)
  if RMSE <= 0
    return 0
  return RMSE
)

attachListeners = () -> (
   matchType = getMatchTypeSelector()
   matchType.addEventListener('click', setupForMultiplayerElements)
   totalMatchesInput = getTotalMatchesInput()
   totalMatchesInput.addEventListener('keyup', totalMatchesChange)
   totalTimeInput = getTotalTimeInput()
   totalTimeInput.addEventListener('keyup', totalTimeChange)
   totalUncertaintyInput = getUncertaintyInput()
   totalUncertaintyInput.addEventListener('click', totalUncertaintyChange)
   disparityInput = getDisparityInput()
   disparityInput.addEventListener('click', RMSEConditionChange)
   rightButton = document.getElementById('btnRight')
   leftButton  = document.getElementById('btnLeft')
   rightButton.addEventListener('click', RMSEConditionChange)
   leftButton.addEventListener('click', RMSEConditionChange)
)
