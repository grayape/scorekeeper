#test_models.py
import unittest
from red.config import config
config.read('config/test_conf.conf') # must be called before importing models to ensure memory based db
from models.model import Player, Match, Team, initSchema, dropSchema, sessionmaker, engine

Session = sessionmaker(bind=engine)


class Test_ModelTest(unittest.TestCase):

    def setUp(self):
        initSchema()
        self.session = Session()

    def tearDown(self):
        self.session.close()
        dropSchema()

    def testPlayerCreateOrLoadSame(self):
        playerA = Player.createOrLoad('1',self.session)
        self.session.commit()
        playerB = Player.createOrLoad('1',self.session)
        self.assertEqual(playerA,playerB)

    def testPlayerCreateOrLoadDifferent(self):
        playerA = Player.createOrLoad('1',self.session)
        self.session.commit()
        playerB = Player.createOrLoad('2',self.session)
        self.assertNotEqual(playerA,playerB)

    def testTeamCreateOrLoadExistingPlayerSame(self):
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

    def testTeamCreateOrLoadExistingPlayersSame(self):
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

    def testTeamCreateOrLoadExistingPlayerDifferent(self):
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

    def testTeamCreateOrLoadExistingPlayersDifferent(self):
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

    def testTeamCreateOrLoadNewPlayerSame(self):
        #setup
        player = Player(rfid='1',name='1')
        #run
        teamA = Team.createOrLoad([player],self.session)
        self.session.add(teamA)
        self.session.commit()
        self.assertEqual(self.session.query(Player).filter(Player.rfid == '1').one(),player)
        teamB = Team.createOrLoad([player],self.session)
        self.assertEqual(teamA,teamB)

    def testTeamCreateOrLoadNewPlayersSame(self):
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

    def testTeamCreateOrLoadNewPlayerDifferent(self):
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

    def testTeamCreateOrLoadNewPlayersDifferent(self):
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


    def testTeamCreateOrLoadPlayersEmpty(self):
        #run
        self.assertRaises(Exception, Team.createOrLoad,([],self.session))
        
    def testTeamCreateOrLoadPlayersEmpty(self):
        #run
        self.assertRaises(Exception, Team.createOrLoad,(None,self.session))
     
    def testMatchAsDict(self):
        #run 

        match = self.session.query(Team).filter_by(rfid='1').first()
        
        self.assertEqual(match.asDict(), {
            "scorea":10,
            "scoreb":0,
            "teama":['1'],
            "teamb":['1']
         

            })



if __name__ == '__main__':
    unittest.main()