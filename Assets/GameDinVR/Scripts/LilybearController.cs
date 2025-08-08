// Lilybear orchestrates whispers and logs them for debugging.

using UnityEngine;

public class LilybearController : GuardianBase {
    [TextArea] public string LastMessage;

    void Start(){ GuardianName = "Lilybear"; Role = "Voice & Operations"; }

    public override void OnMessage(string from, string message){
        LastMessage = $"{from}: {message}";
        if (message.StartsWith("/route ")){
            // broadcast anything after /route
            var payload = message.Substring(7);
            Whisper("*", payload);
        }
    }

    [ContextMenu("Test Whisper")]
    void TestWhisper(){
        Whisper("*", "The council is assembled.");
    }
}
