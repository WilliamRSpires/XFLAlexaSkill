# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import json
import requests
import datetime
from datetime import timedelta
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Extreme Football Info. If you'd like to know when the next set of games are say Schedule. For Standings say Standings or Table. For scores say Scoreboard."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class ScheduleHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ScheduleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        ESPN = "https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=xfl&region=us&lang=en&contentorigin=espn&buyWindow=1m&showAirings=buy%2Clive%2Creplay&showZipLookup=true&tz=America/New_York"
        Schedule = requests.get(ESPN)
        NewSchedule=Schedule.json()
        XFLSchedule=NewSchedule['sports'][0]['leagues'][0]['events']
        game={}
        gametime={}
        channel={}
        output=[]
        speak_output=" "
        for i in range(len(XFLSchedule)): 
            game["game{0}".format(i)]=XFLSchedule[i]['competitors'][0]['displayName']+" versus "+XFLSchedule[i]['competitors'][1]['displayName']
            gametime["time{0}".format(i)]=XFLSchedule[i]['fullStatus']['type']['detail']
            channel["channel{0}".format(i)]=XFLSchedule[i]['broadcast']
        for key, value in gametime.items():
            gametime[key]=value.replace("Sat","Saturday")
            gametime[key]=value.replace("Sun","Sunday")
            gametime[key]=value.replace("EST","Eastern Time")
        for i in range(len(XFLSchedule)): 
            output.append("On " + gametime['time%s'%i] + " the " + game["game%s"%i] + " will air on " + channel["channel%s"%i]+".")
            output.append(" ,,,, ")
        for ele in output:
            speak_output+=ele
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class StandingsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StandingsIntent")(handler_input)
    def handle(self, handler_input):
        ESPN = "https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=xfl&region=us&lang=en&contentorigin=espn&buyWindow=1m&showAirings=buy%2Clive%2Creplay&showZipLookup=true&tz=America/New_York"
        Standings = requests.get(ESPN)
        NewStandings = Standings.json()
        EasternConference=["New York Guardians", "DC Defenders","St. Louis BattleHawks","Tampa Bay Vipers"]
        WesternConference=["Houston Roughnecks","Dallas Renegades","Los Angeles Wildcats","Seattle Dragons"]
        EasternStandings=[]
        WesternStandings=[]
        Events=NewStandings['sports'][0]['leagues'][0]['events']
        test=[]
        SortedEasternStandings=[]
        SortedWesternStandings=[]
        for i in range(4):
            CurrentGame=Events[i]
            test.append(i)
            for i in range(2):
                Competitors=CurrentGame['competitors'][i]
                if Competitors['displayName'] in EasternConference:
                    RecordSplit=Competitors['record'].split("-")
                    w=RecordSplit[0]
                    win=int(w)
                    l=RecordSplit[1]
                    loss=int(l)
                    EasternStandings.append([Competitors['displayName'],win,loss])
                    SortedEasternStandings = sorted(EasternStandings, key = lambda x: x[2])
                else:
                    RecordSplit=Competitors['record'].split("-")
                    w=RecordSplit[0]
                    win=int(w)
                    l=RecordSplit[1]
                    loss=int(l)
                    WesternStandings.append([Competitors['displayName'],win,loss])
                    SortedWesternStandings = sorted(WesternStandings, key = lambda x: x[2])
        FirstPlaceOutput=" "
        SecondPlaceOutput=" "
        ThirdPlaceOutput=" "
        FourthPlaceOuput=" "
        Team1=SortedEasternStandings[0][0]
        Team2=SortedEasternStandings[1][0]
        Team3=SortedEasternStandings[2][0]
        Team4=SortedEasternStandings[3][0]
        Wins1=SortedEasternStandings[0][1]
        Wins2=SortedEasternStandings[1][1]
        Wins3=SortedEasternStandings[2][1]
        Wins4=SortedEasternStandings[3][1]
        Losses1=SortedEasternStandings[0][2]
        Losses2=SortedEasternStandings[1][2]
        Losses3=SortedEasternStandings[2][2]
        Losses4=SortedEasternStandings[3][2]
        EastCoastOutput=""
        if Losses1 == Losses2 and Losses2 == Losses3 and Losses3 == Losses4:
            FirstPlaceOutput="All four teams are tied for first place with a record of %d"%Wins1 + " and %d"%Losses1
        elif Losses1 == Losses2 and Losses2 == Losses3:
            FirstPlaceOutput= Team1 + " and " + Team2 + "and" + Team3 + "are tied for First Place with a record of %d"%Wins1 + " and %d"%Losses1
            FourthPlaceOutput= Team4 + " are in last place with a record of %d"%Wins4 + " and %d"%Losses4
        elif Losses1 == Losses2:
            if Losses3 == Losses4:
                FirstPlaceOutput = Team1 + " and " + Team2 + " are tied for first place with a record of %d"%Wins1 + " and %d"%Losses1
                ThirdPlaceOutput = Team3 + " and " + Team4 + " are tied for third place with a record of %d"%Wins3 + " and %d"%Losses3
            else:
                FirstPlaceOutput = Team1 + " and " + Team2 + " are tied for first place with a record of %d"%Wins1 + "and %d"%Losses1
                ThirdPlaceOutput = Team3 + " are in third place with a record of %d"%Wins3 + " and %d"%Wins3
                FourthPlaceOutput = Team4 + " are in last place with a record of %d"%Wins4 + " and %d"%Losses4
        else:
            FirstPlaceOutput = Team1 + " are in first place with a record of %d"%Wins1 + " and %d"%Losses1
            if Losses2==Losses3 and Losses3==Losses4:
                SecondPlaceOutput=Team2 + " and " + Team3 + "and" + Team4 + " are tied for second place with a record of %d"%Wins2 + " and %d"%Losses2
            elif Losses2==Losses3:
                SecondPlaceOutput=Team2 + " and " + Team3 + " are tied for second place with a record of %d"%Wins2 + " and %d"%Losses2
                FourthPlaceOuput=Team4 + " are in last place with a record of %d"%Wins4 + " and %d"%Losses4
            else:
                SecondPlaceOutput = Team2 + " are in second place with a record of %d"%Wins2 + " and %d"%Losses
                if Losses3==Losses4:
                    ThirdPlaceOutput = Team3 + " and " + Team4 + " are tied for third place with a record of %d"%Wins3 + " and %d"%Losses3
                else:
                    ThirdPlaceOutput = Team3 + " are in third place with a record of %d"%Wins3 + " and %d"%Losses3 
                    FourthPlaceOutput = Team4 + " are in last place with a record of %d"%Wins4 + " and %d"%Losses4
        EastCoastOutput="In the Eastern Conference the standings are as follows," + FirstPlaceOutput + "." + SecondPlaceOutput + "." + ThirdPlaceOutput + "." + FourthPlaceOutput
        WestFirstPlaceOutput=" "
        WestSecondPlaceOutput=" "
        WestThirdPlaceOutput=" "
        WestFourthPlaceOuput=" "
        WestTeam1=SortedWesternStandings[0][0]
        WestTeam2=SortedWesternStandings[1][0]
        WestTeam3=SortedWesternStandings[2][0]
        WestTeam4=SortedWesternStandings[3][0]
        WestWins1=SortedWesternStandings[0][1]
        WestWins2=SortedWesternStandings[1][1]
        WestWins3=SortedWesternStandings[2][1]
        WestWins4=SortedWesternStandings[3][1]
        WestLosses1=SortedWesternStandings[0][2]
        WestLosses2=SortedWesternStandings[1][2]
        WestLosses3=SortedWesternStandings[2][2]
        WestLosses4=SortedWesternStandings[3][2]
        WestCoastOutput=""
        if WestLosses1 == WestLosses2 and WestLosses2 == WestLosses3 and WestLosses3 == WestLosses4:
            WestFirstPlaceOutput="All four teams are tied for first place with a record of %d"%WestWins1 + " and %d"%WestLosses1
        elif WestLosses1 == WestLosses2 and WestLosses2 == WestLosses3:
            WestFirstPlaceOutput= WestTeam1 + " and " + WestTeam2 + "and" + WestTeam3 + "are tied for First Place with a record of %d"%WestWins1 + " and %d"%WestLosses1
            WestFourthPlaceOutput= WestTeam4 + " are in last place with a record of %d"%WestWins4 + " and %d"%WestLosses4
        elif WestLosses1 == WestLosses2:
            if WestLosses3 == WestLosses4:
                WestFirstPlaceOutput = WestTeam1 + " and " + WestTeam2 + " are tied for first place with a record of %d"%WestWins1 + " and %d"%WestLosses1
                WestThirdPlaceOutput = WestTeam3 + " and " + WestTeam4 + " are tied for third place with a record of %d"%WestWins3 + " and %d"%WestLosses3
            else:
                WestFirstPlaceOutput = WestTeam1 + " and " + WestTeam2 + " are tied for first place with a record of %d"%WestWins1 + "and %d"%WestLosses1
                WestThirdPlaceOutput = WestTeam3 + " are in third place with a record of %d"%WestWins3 + " and %d"%WestWins3
                WestFourthPlaceOutput = WestTeam4 + " are in last place with a record of %d"%WestWins4 + " and %d"%WestLosses4
        else:
            WestFirstPlaceOutput = WestTeam1 + " are in first place with a record of %d"%WestWins1 + " and %d"%WestLosses1
            if WestLosses2==WestLosses3 and WestLosses3==WestLosses4:
                WestSecondPlaceOutput=WestTeam2 + " and " + WestTeam3 + "and" + WestTeam4 + " are tied for second place with a record of %d"%WestWins2 + " and %d"%WestLosses2
            elif Losses2==Losses3:
                WestSecondPlaceOutput=WestTeam2 + " and " + WestTeam3 + " are tied for second place with a record of %d"%WestWins2 + " and %d"%WestLosses2
                WestFourthPlaceOuput=WestTeam4 + " are in last place with a record of %d"%WestWins4 + " and %d"%WestLosses4
            else:
                WestSecondPlaceOutput = WestTeam2 + " are in second place with a record of %d"%WestWins2 + " and %d"%WestLosses2
                if WestLosses3==WestLosses4:
                    WestThirdPlaceOutput = WestTeam3 + " and " + WestTeam4 + " are tied for third place with a record of %d"%WestWins3 + " and %d"%WestLosses3
                else:
                    WestThirdPlaceOutput = WestTeam3 + " are in third place with a record of %d"%WestWins3 + " and %d"%WestLosses3 
                    WestFourthPlaceOutput = WestTeam4 + " are in last place with a record of %d"%WestWins4 + " and %d"%WestLosses4
        WestCoastOutput="In the Western Conference the standings are as follows," + WestFirstPlaceOutput + "." + WestSecondPlaceOutput + "." + WestThirdPlaceOutput + "." + WestFourthPlaceOuput
        speak_output = EastCoastOutput + WestCoastOutput
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class ScoreboardIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ScoreboardIntent")(handler_input)
    def handle(self, handler_input):
        ESPNScores=None
        ESPNScores2=None
        Scoreboard = None
        Scoreboard2 = None
        NewScoreboard = None
        NewScoreboard2 = None
        XFLScoreboard = None
        XFLScoreboard2 = None
        count=0
        output=[]
        speak_output=" "
        game={}
        winners={}
        losers={}
        winningscores={}
        losingscores={}
        d=datetime.datetime.today() - timedelta(hours=5, minutes=0)
        hour=d.hour
        delta=(d.weekday()+1)%7
        weekday=d.weekday()
        sun = d - datetime.timedelta(delta)
        sat = d - datetime.timedelta(delta+1)
        saturdaystring=sat.strftime("%Y%m%d")
        sundaystring=sun.strftime("%Y%m%d")
        if hour > 13 and weekday >= 5:
            ESPNScores="https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=xfl&region=us&lang=en&contentorigin=espn&buyWindow=1m&showAirings=buy%2Clive%2Creplay&showZipLookup=true&tz=America/New_York"
            Scoreboard = requests.get(ESPNScores)
            NewScoreboard=Scoreboard.json()
            XFLScoreboard=NewScoreboard['sports'][0]['leagues'][0]['events']
            for i in range(len(XFLScoreboard)):
                game["game{0}".format(i)]=XFLScoreboard[i]['name']
                if XFLScoreboard[i]['competitors'][0]['winner']==True:
                    winners["winner{0}".format(i)]=XFLScoreboard[i]['competitors'][0]['displayName']
                    winningscores["winningscores{0}".format(i)]=XFLScoreboard[i]['competitors'][0]['score']
                    losers["loser{0}".format(i)]=XFLScoreboard[i]['competitors'][1]['displayName']
                    losingscores["losingscores{0}".format(i)]=XFLScoreboard[i]['competitors'][1]['score']
                else:
                    winners["winner{0}".format(i)]=XFLScoreboard[i]['competitors'][1]['displayName']
                    winningscores["winningscores{0}".format(i)]=XFLScoreboard[i]['competitors'][1]['score']
                    losers["loser{0}".format(i)]=XFLScoreboard[i]['competitors'][0]['displayName']
                    losingscores["losingscores{0}".format(i)]=XFLScoreboard[i]['competitors'][0]['score']
            for i in range(len(XFLScoreboard)):
                output.append(game['game%s'%i] + ", " + winners["winner%s"%i] + " won with a score of " + winningscores["winningscores%s"%i] + " , " + losers["loser%s"%i] +" lost, scoring only " + losingscores["losingscores%s"%i])
        else:
            ESPNScores="https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=xfl&region=us&lang=en&dates={}&contentorigin=espn&buyWindow=1m&showAirings=buy%2Clive%2Creplay&showZipLookup=true&tz=America/New_York".format(saturdaystring)
            ESPNScores2="https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=xfl&region=us&lang=en&dates={}&contentorigin=espn&buyWindow=1m&showAirings=buy%2Clive%2Creplay&showZipLookup=true&tz=America/New_York".format(sundaystring)
            Scoreboard = requests.get(ESPNScores)
            NewScoreboard=Scoreboard.json()
            XFLScoreboard=NewScoreboard['sports'][0]['leagues'][0]['events']
            Scoreboard2 = requests.get(ESPNScores)
            NewScoreboard2=Scoreboard2.json()
            XFLScoreboard2=NewScoreboard2['sports'][0]['leagues'][0]['events']
            winners2={}
            losers2={}
            winningscores2={}
            losingscores2={}
            count=0
            for i in range(len(XFLScoreboard)):
                game["game{0}".format(i)]=XFLScoreboard[i]['name']
                count+=1
                if XFLScoreboard[i]['competitors'][0]['winner']==True:
                    winners["winner{0}".format(i+count)]=XFLScoreboard2[i]['competitors'][0]['displayName']
                    winningscores["winningscores{0}".format(i+count)]=XFLScoreboard2[i]['competitors'][0]['score']
                    losers["loser{0}".format(i+count)]=XFLScoreboard2[i]['competitors'][1]['displayName']
                    losingscores["losingscores{0}".format(i+count)]=XFLScoreboard2[i]['competitors'][1]['score']
                else:
                    winners["winner{0}".format(i)]=XFLScoreboard2[i]['competitors'][1]['displayName']
                    winningscores["winningscores{0}".format(i)]=XFLScoreboard2[i]['competitors'][1]['score']
                    losers["loser{0}".format(i)]=XFLScoreboard2[i]['competitors'][0]['displayName']
                    losingscores["losingscores{0}".format(i)]=XFLScoreboard2[i]['competitors'][0]['score']
            for i in range(len(XFLScoreboard2)):
                game["game{0}".format(i+count)]=XFLScoreboard2[i]['name']
                if XFLScoreboard2[i]['competitors'][0]['winner']==True:
                    winners2["winner{0}".format(i+count)]=XFLScoreboard2[i]['competitors'][0]['displayName']
                    winningscores2["winningscores{0}".format(i+count)]=XFLScoreboard2[i]['competitors'][0]['score']
                    losers2["loser{0}".format(i+count)]=XFLScoreboard2[i]['competitors'][1]['displayName']
                    losingscores2["losingscores{0}".format(i+count)]=XFLScoreboard2[i]['competitors'][1]['score'] 
                else:
                    winners2["winner{0}".format(i)]=XFLScoreboard2[i]['competitors'][1]['displayName']
                    winningscores2["winningscores{0}".format(i)]=XFLScoreboard2[i]['competitors'][1]['score']
                    losers2["loser{0}".format(i)]=XFLScoreboard2[i]['competitors'][0]['displayName']
                    losingscores2["losingscores{0}".format(i)]=XFLScoreboard2[i]['competitors'][0]['score']
            for i in range(len(XFLScoreboard)):
                output.append(game['game%s'%i] + ", " + winners["winner%s"%i] + " won with a score of " + winningscores["winningscores%s"%i] + ", " + losers["loser%s"%i] +" lost, scoring only " + losingscores["losingscores%s"%i])
            for i in range(len(XFLScoreboard2)):
                x=i+count
                output.append(game['game%s'%x] + ", " + winners2["winner%s"%i] + " won with a score of " + winningscores2["winningscores%s"%i] + " , " + losers2["loser%s"%i] +" lost, scoring only " + losingscores2["losingscores%s"%i])
                output.append(" . ")
        for ele in output:
            speak_output+=ele
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask me for the Standings, the Schedule, or the Scoreboard"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ScheduleHandler())
sb.add_request_handler(ScoreboardIntentHandler())
sb.add_request_handler(StandingsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()