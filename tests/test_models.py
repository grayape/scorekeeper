
import unittest


from red.config import config
print config.sections()
config.read('config/test_conf.conf') # must be called before importing models to ensure memory based db
print config.sections()
from models.model import Player, Match, Team, initData, initSchema, dropSchema, sessionmaker, engine
print config.sections()

Session = sessionmaker(bind=engine)


class Test_ModelsTest(unittest.TestCase):

    def setUp(self):
        initSchema()

        self.session = Session()

    def tearDown(self):
        self.session.close()
        dropSchema()

    def testPass(self):
        """Test case A. note that all test method names must begin with 'test.'"""
        assert True 

    

    def testPlayercreateOrLoadSame(self):
        playerA = Player.createOrLoad('1',self.session)
        self.session.commit()
        playerB = Player.createOrLoad('1',self.session)
        self.assertEqual(playerA,playerB)

    def testPlayer_createOrLoad_different(self):
        playerA = Player.createOrLoad('1',self.session)
        self.session.commit()
        playerB = Player.createOrLoad('2',self.session)
        self.assertNotEqual(playerA,playerB)

    def testTeam_createOrLoad_existingPlayer_same(self):
        #setup
        player = Player(rfid='1',name='1')
        self.session.add(player)
        self.session.commit()
        #run
        teamA = Team.createOrLoad([player],self.session)
        self.session.add(teamA)
        self.session.commit()
        teamB = Team.createOrLoad([player],self.session)
        self.assertEqual(teamA,teamB)

    def test_team_createOrLoad_existingPlayers_same(self):
        #setup
        player1 = Player(rfid='1',name='1')
        player2 = Player(rfid='2',name='2')
        self.session.add(player1)
        self.session.add(player2)
        self.session.commit()
        #run
        teamA = Team.createOrLoad([player1,player2],self.session)
        self.session.add(teamA)
        self.session.commit()
        teamB = Team.createOrLoad([player1,player2],self.session)
        self.assertEqual(teamA,teamB)

    def test_team_createOrLoad_existingPlayer_different(self):
        #setup
        player1 = Player(rfid='1',name='1')
        player2 = Player(rfid='2',name='2')
        self.session.add(player1)
        self.session.add(player2)
        self.session.commit()
        #run
        teamA = Team.createOrLoad([player1],self.session)
        self.session.add(teamA)
        self.session.commit()
        teamB = Team.createOrLoad([player2],self.session)
        self.assertNotEqual(teamA,teamB)

    def test_team_createOrLoad_existingPlayers_different(self):
        #setup
        player1 = Player(rfid='1',name='1')
        player2 = Player(rfid='2',name='2')
        player3 = Player(rfid='3',name='3')
        player4 = Player(rfid='4',name='4')
        self.session.add(player1)
        self.session.add(player2)
        self.session.add(player3)
        self.session.add(player4)
        self.session.commit()
        #run
        teamA = Team.createOrLoad([player1,player2],self.session)
        self.session.add(teamA)
        self.session.commit()
        teamB = Team.createOrLoad([player3,player4],self.session)
        self.assertNotEqual(teamA,teamB)

    def test_team_createOrLoad_newPlayer_same(self):
        #setup
        player = Player(rfid='1',name='1')
        #run
        teamA = Team.createOrLoad([player],self.session)
        self.session.add(teamA)
        self.session.commit()
        self.assertEqual(self.session.query(Player).filter(Player.rfid == '1').one(),player)
        teamB = Team.createOrLoad([player],self.session)
        self.assertEqual(teamA,teamB)

    def test_team_createOrLoad_newPlayers_same(self):
        #setup
        player1 = Player(rfid='1',name='1')
        player2 = Player(rfid='2',name='2')
        #run
        teamA = Team.createOrLoad([player1,player2],self.session)
        self.session.add(teamA)
        self.session.commit()
        self.assertEqual(self.session.query(Player).filter(Player.rfid == '1').one(),player1)
        teamB = Team.createOrLoad([player1,player2],self.session)
        self.assertEqual(teamA,teamB)

    def test_team_createOrLoad_newPlayer_different(self):
        #setup
        player1 = Player(rfid='1',name='1')
        player2 = Player(rfid='2',name='2')
        #run
        teamA = Team.createOrLoad([player1],self.session)
        self.session.add(teamA)
        self.session.commit()
        self.assertEqual(self.session.query(Player).filter(Player.rfid == '1').one(),player1)
        teamB = Team.createOrLoad([player2],self.session)
        self.assertNotEqual(teamA,teamB)

    def test_team_createOrLoad_newPlayers_different(self):
        #setup
        player1 = Player(rfid='1',name='1')
        player2 = Player(rfid='2',name='2')
        player3 = Player(rfid='3',name='3')
        player4 = Player(rfid='4',name='4')
        #run
        teamA = Team.createOrLoad([player1,player2],self.session)
        self.session.add(teamA)
        self.session.commit()
        self.assertEqual(self.session.query(Player).filter(Player.rfid == '1').one(),player1)
        teamB = Team.createOrLoad([player3,player4],self.session)
        self.assertNotEqual(teamA,teamB)


    def test_team_createOrLoad_players_empty(self):
        #run
        self.assertRaises(Exception, Team.createOrLoad,([],self.session))
        
    def test_team_createOrLoad_players_empty(self):
        #run
        self.assertRaises(Exception, Team.createOrLoad,(None,self.session))
     
    def testMatchasDict(self):
        #run 
        initData()
        match = self.session.query(Match).first()
        
        self.assertEqual(match.asDict(), {
            "scorea":10,
            "scoreb":0,
            "teama":['1'],
            "teamb":['2']
         

            })
 


          
if __name__ == "__main__":
    unittest.main() # run all tests