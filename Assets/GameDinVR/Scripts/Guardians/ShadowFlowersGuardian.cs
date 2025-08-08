// ShadowFlowers manifests blessings onto a TextMesh when prompted.

using UnityEngine;

public class ShadowFlowersGuardian : GuardianBase {
    public TextMesh BlessingText;

    void Start(){ GuardianName = "ShadowFlowers"; Role = "Sentiment & Rituals"; }

    public override void OnMessage(string from, string message){
        if (message.Contains("blessing")){
            var line = "\uD83C\uDF38 May your path be protected and your heart be held.";
            if (BlessingText) BlessingText.text = line;
            Whisper("Lilybear", "Blessing delivered.");
        }
    }
}
