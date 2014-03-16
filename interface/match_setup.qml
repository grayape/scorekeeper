import QtQuick 1.0

import "core" as Core 

Core.Interface {
    id: match_setup
 
    function updateTeamA(playerIds){
        teamaplayers.text = playerIds
    }
    
    function updateTeamB(playerIds){
        teambplayers.text = playerIds
    }

    Text {
        id: headline
        x: 9
        y: 8
        width: 463
        height: 80
        color: "#ffffff"
        text: qsTr("Scan Your Tag")
        horizontalAlignment: Text.AlignHCenter
        font.pixelSize: 67
    }

    Core.Button {
        id: start_match
        callId: "start_match"
        btnText: "Start match"
        x: 145
        y: 214
    }

    Core.TeamText {
        id: teamatext
        x: 10
        y: 100   
        text: qsTr("Team A")
    }

    Core.TeamText {
        id: teambtext
        x: 250
        y: 100      
        text: qsTr("Team B")
    }

    Core.PlayerText {
        id: teamaplayers
        x: 10
        y: 127
         text: qsTr("(no player scanned)")
       
    }

    Core.PlayerText {
        id: teambplayers
        x: 256
        y: 127
       
        text: qsTr("(no player scanned)")
   
    }
}