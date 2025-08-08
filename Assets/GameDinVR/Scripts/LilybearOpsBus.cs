// Architectural preamble:
// Acts as a lightweight event bus inside Unity so guardians can communicate
// without tight coupling. External systems (Discord, MCP) can inject messages
// by calling LilybearOpsBus.I.Say.

using UnityEngine;
using System;

public class LilybearOpsBus : MonoBehaviour {
    public static LilybearOpsBus I; // singleton instance

    public delegate void Whisper(string from, string to, string message);
    public event Whisper OnWhisper;

    void Awake(){ I = this; }

    public void Say(string from, string to, string message){
        OnWhisper?.Invoke(from, to, message);
        Debug.Log($"[LilybearBus] {from} → {to}: {message}");
    }
}
