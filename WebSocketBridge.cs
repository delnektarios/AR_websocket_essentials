using System;
using System.Collections;
using System.Collections.Concurrent;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Net.WebSockets;



using UnityEngine;
using System.Net;
using UnityEngine.UI;

class WebSocketBridge : MonoBehaviour
{
    public Text text;

    public delegate void ReceiveAction(string message);
    public event ReceiveAction OnReceived;

    private ClientWebSocket webSocket = null;
    private ConcurrentQueue<string> messageQueue = new ConcurrentQueue<string>();

    [SerializeField]
    private string url = "wss://localhost:3000";

    void Start()
    {
        Task connect = Connect(url);
    }

    void OnDestroy()
    {
        if (webSocket != null)
        {
            webSocket.Dispose();
        }
        Debug.Log("the socket is closed");

    }

    public async Task Connect(string url)
    {
        //ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

        try
        {
            webSocket = new ClientWebSocket();
            await webSocket.ConnectAsync(new Uri(url), CancellationToken.None);

        }
        catch (Exception e)
        {
            Debug.LogError(e);
        }

        await Send("Welcome UNITY App!");

        await Receive(1000);

        
    }

    private async Task Send(string message)
    {
        var encoded = Encoding.UTF8.GetBytes(message);
        var buffer = new ArraySegment<Byte>(encoded, 0, encoded.Length);

        await webSocket.SendAsync(buffer, WebSocketMessageType.Text, true, CancellationToken.None);

    }

    private async Task Receive(int length = 8192)
    {
        ArraySegment<Byte> buffer = new ArraySegment<byte>(new byte[length]);

        while (webSocket.State == WebSocketState.Open)
        {
            WebSocketReceiveResult result = null;

            using (var ms = new MemoryStream())
            {
                do
                {
                    result = await webSocket.ReceiveAsync(buffer, CancellationToken.None);
                    ms.Write(buffer.Array, buffer.Offset, result.Count);

                } while (!result.EndOfMessage);

                ms.Seek(0, SeekOrigin.Begin);

                if (result.MessageType == WebSocketMessageType.Text)
                {
                    using (var reader = new StreamReader(ms, Encoding.UTF8))
                    {
                        string message = reader.ReadToEnd();
                        Debug.Log(message);

                        text.text = message;

                        //must be delete in case of threads 
                        //the call may happen elseware
                        if (OnReceived != null) OnReceived(message);
                    }
                }
                else if (result.MessageType != WebSocketMessageType.Text)
                {
                    using (var reader = new StreamReader(ms, Encoding.UTF8))
                    {
                        Debug.LogWarning("unknown message type to receive.");
                        string message = reader.ReadToEnd();
                        Debug.Log(message);

                        //must be delete in case of threads 
                        //the call may happen elseware
                        if (OnReceived != null) OnReceived(message);
                    }

                }else if(result.MessageType == WebSocketMessageType.Close)
                {
                    await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None);

                }
            }
        }
    }

    private async Task Process()
    {
        while (webSocket.State == WebSocketState.Open)
        {
            if(messageQueue.Count > 0)
            {
                string message;
                bool success = messageQueue.TryDequeue(out message);

                if (success)
                {
                    Debug.Log(message);
                    if (OnReceived != null) OnReceived(message);
                }
            }
        }
    }
}