from activities.activity import Activity

class CreateMatchActivity(Activity):
    
    teamAPlayers = []
    teamBPlayers = []
    
    def onCreate(self,data):
        self.setLayout("match_setup")
        
    def processDisplayMessage(self,message):
        if(message["data"]=="start_match"):
            print("Start Match Button Pressed")
            data = dict()
            data["teamA"] = self.teamAPlayers
            data["teamB"] = self.teamBPlayers
            self.switchActivity("MatchActivity",data)   
    
    def start_match(self,teama,teamb):
        if self.is_active:
            print ("Unable to start match, already in progress!")
            #self.end_match()
            return
        team_a = self.session.query(Team).filter(Team.name == teama).one()
        team_b = self.session.query(Team).filter(Team.name == teamb).one()
        self.is_active = True
        self.match = Match( team_a = team_a, score_a = 0,\
                            team_b = team_b, score_b = 0)
        self.session.add(self.match)
        self.controller.switch_activity("MatchActivity", {"teamA":self.teamA,"teamB":self.teamB})
        print("Match: received a match, starting match between: "+team_a.name+" and "+team_b.name )
        
    def new_player(self, name):
        self.session.add(Player(name = name))
        self.session.commit()


    def new_team(self, name_a, name_b, team_name):
        team = Team(name = team_name)
        self.session.add(team)
        players = self.session.query(Player).filter(Player.name.in_([name_a,name_b]))
        if players.count() != 2:
            print("Something amiss! Found " + players.count() + " players when expecting 2")
            self.session.rollback()
            return
        for player in players:
            team.players.append(player)
        self.session.commit()
        
    def processRfidMessage(self,message):
        if(message["header"]=="player_rfid"):
            self.loadPlayer(message["data"])
            
            
    def loadPlayer(self,playerRfid):
        #if(self.session.query(Player).filter(Player.id == playerId).count() > 0):
        if(len(self.teamBPlayers) < len(self.teamAPlayers)):
            self.teamBPlayers.append(playerRfid)
            self.controller.sockets["display"].send_json({"header":"call_func","data":{"func":"updateTeamB","param":reduce(lambda x,y: x+"\n" +y,self.teamBPlayers)}})
        else:
            self.teamAPlayers.append(playerRfid)
            self.controller.sockets["display"].send_json({"header":"call_func","data":{"func":"updateTeamA","param":reduce(lambda x,y: x+"\n" +y,self.teamAPlayers)}})
        
        