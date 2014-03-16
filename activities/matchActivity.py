from activities.activity import Activity
from models import Match, Session, Player, Team, Base, initSchema

class MatchActivity(Activity):
   
    def onCreate(self,data=None):
        self.setLayout("match")
        self.match = data
        self.updateLayout()
     

    def processDisplayMessage(self,message):
        if message["header"] == "button_clicked":          
            if message["data"] == "a_scored":
                self.team_scored("a");
            elif message["data"] == "b_scored":
                self.team_scored("b");
            elif message["data"] == "end_match":
                self.end_match();
          
        
        else:
            print("We (match) received something (message), but we are unsure what it is")
      
    

    def end_match(self):
               
        #print ("Ending match and saving the results at time: "+self.match.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        self.switchActivity("ConfirmResultActivity", self.match)
        
    def team_scored(self, team):
       
        if team == 'a':
            scoring_team = self.match.team_a;
            self.match.score_a = self.match.score_a + 1
        elif team == 'b':
            scoring_team = self.match.team_b;
            self.match.score_b = self.match.score_b + 1
        else:
            print ("Who the hell scored")
        
        print("Some scored it was team: " + scoring_team.name)
        print("Score is now: %s - %s" % (self.match.score_a  ,self.match.score_b))
        # Broadcast to display

        self.updateLayout()


    def updateLayout(self):

        message =  {"header":"call_func", 
                    "data":{"func":"updateScoreA",
                            "param":self.match.score_a}}

        self.controller.sockets["display"].send_json(message)

        message =  {"header":"call_func", 
                    "data":{"func":"updateScoreB",
                            "param":self.match.score_b}}

        self.controller.sockets["display"].send_json(message)
    

        