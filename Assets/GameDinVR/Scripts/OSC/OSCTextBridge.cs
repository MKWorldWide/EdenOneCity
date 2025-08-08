// Placeholder for future OSC hook (MCP → VRChat via external OSC app)

using UnityEngine;

public class OSCTextBridge : MonoBehaviour {
    public TextMesh Target;
    public void SetText(string s){ if (Target) Target.text = s; }
}
