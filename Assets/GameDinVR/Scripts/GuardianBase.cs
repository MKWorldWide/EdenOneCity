// Base class for all guardians. Provides subscription to LilybearOpsBus and
// simple whisper helper to keep derived guardians focused on their roles.

using UnityEngine;

public class GuardianBase : MonoBehaviour {
    [Header("Identity")]
    public string GuardianName = "Guardian";
    public string Role = "Undefined";

    protected virtual void OnEnable(){
        if (LilybearOpsBus.I != null)
            LilybearOpsBus.I.OnWhisper += HandleWhisper;
    }

    protected virtual void OnDisable(){
        if (LilybearOpsBus.I != null)
            LilybearOpsBus.I.OnWhisper -= HandleWhisper;
    }

    protected virtual void HandleWhisper(string from, string to, string message){
        if (to == GuardianName || to == "*"){
            Debug.Log($"[{GuardianName}] received from {from}: {message}");
            OnMessage(from, message);
        }
    }

    public virtual void OnMessage(string from, string message) {}

    protected void Whisper(string to, string message){
        LilybearOpsBus.I?.Say(GuardianName, to, message);
    }
}
