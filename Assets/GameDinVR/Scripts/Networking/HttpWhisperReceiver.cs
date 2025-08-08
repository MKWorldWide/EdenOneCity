// Listens for HTTP POST /whisper and forwards payload to LilybearOpsBus.
// Now supports a shared bearer token for basic auth; still requires TLS for
// production deployments and more robust auth for hostile networks.

using UnityEngine;
using System;
using System.Net;
using System.IO;
using System.Text;
using System.Threading.Tasks;

public class HttpWhisperReceiver : MonoBehaviour {
    public int Port = 8080;
    public string TokenEnvVar = "WHISPER_TOKEN"; // env var name for shared token
    HttpListener listener;
    string token;

    async void Start(){
        token = Environment.GetEnvironmentVariable(TokenEnvVar);
        listener = new HttpListener();
        listener.Prefixes.Add($"http://*:{Port}/");
        listener.Start();
        Debug.Log($"HttpWhisperReceiver listening on {Port}");
        while (listener.IsListening){
            var ctx = await listener.GetContextAsync();
            _ = Process(ctx); // fire and forget
        }
    }

    async Task Process(HttpListenerContext ctx){
        try {
            if (ctx.Request.HttpMethod == "POST" && ctx.Request.Url.AbsolutePath == "/whisper"){
                // rudimentary bearer token check to prevent random posts
                var auth = ctx.Request.Headers["Authorization"];
                if(!string.IsNullOrEmpty(token) && auth != $"Bearer {token}"){
                    ctx.Response.StatusCode = 401;
                    return;
                }
                using var reader = new StreamReader(ctx.Request.InputStream, ctx.Request.ContentEncoding);
                var body = await reader.ReadToEndAsync();
                var payload = JsonUtility.FromJson<WhisperPayload>(body);
                LilybearOpsBus.I?.Say(payload.from, payload.to, payload.message);
                ctx.Response.StatusCode = 200;
            } else {
                ctx.Response.StatusCode = 404;
            }
        } catch(Exception e){
            Debug.LogError($"HttpWhisperReceiver error: {e.Message}");
            ctx.Response.StatusCode = 500;
        } finally {
            ctx.Response.Close();
        }
    }

    void OnDestroy(){
        listener?.Stop();
    }

    [Serializable]
    public class WhisperPayload{
        public string from;
        public string to;
        public string message;
    }
}
