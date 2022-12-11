using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System;
using System.IO;
using UnityEngine.Networking;

[Serializable]
public class BotStatus
{
    public string lastRoundStatus;
    public float lastMessageTime;
    public string lastMessage;
    public string partialMessage;
    public string botLoopStep;
    public string subject;
    public string category;
}
public class ApiHandler : MonoBehaviour
{
    public string api_endpoint = "http://127.0.0.1:5000/api/status";

    public string generatedPagePath = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\html_result.html";
    public string generatedAudioPath = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\tts_response.wav";
    public string initialPagePath = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\SplashPage.html";
    public string initialAudioPath = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\splash_audio.wav";
    public AvatarAnimatorScript animatorScript;
    public DynamicPageLoader pageLoader;
    public PulseEmissionFromSound emissionController;
    public LoadDynamicAudio audioLoader;

    protected bool recievedFirstApiCall = false;

    public string localLastRoundStatus = "NOT_RUN";
    public float localLastMessageTime = 0;
    public string localLastMessage = "";
    public string localPartialMessage = "";
    public string localLastBotLoopStep = "SETUP";
    public string localSubject = "";
    public string localCategory = "";

    IEnumerator GetBotStatus()
    {
        using (UnityWebRequest req = UnityWebRequest.Get(api_endpoint))
        {
            yield return req.Send();
            while (!req.isDone)
                yield return null;
            byte[] result = req.downloadHandler.data;
            string weatherJSON = System.Text.Encoding.Default.GetString(result);
            BotStatus info = JsonUtility.FromJson<BotStatus>(weatherJSON);
            Debug.Log(info);
            processApiResponseValues(
                    info.lastRoundStatus,
                        info.lastMessageTime,
                        info.lastMessage,
                        info.partialMessage,
                        info.botLoopStep,
                        info.subject,
                        info.category);
            StartCoroutine(GetBotStatus());
        }
    }
    IEnumerator WaitForSplash()
    {
        yield return new WaitForSeconds(2);
        while (audioLoader.audioSource.isPlaying)
            yield return null;
        StartCoroutine(GetBotStatus());
    }

    // Start is called before the first frame update
    void Start()
    {
        animatorScript = GetComponent<AvatarAnimatorScript>();
        pageLoader = GetComponent<DynamicPageLoader>();
        emissionController = GetComponent<PulseEmissionFromSound>();
        audioLoader = GetComponent<LoadDynamicAudio>();
        StartCoroutine(WaitForSplash());

    }

    // Update is called once per frame
    void Update()
    {
    }

    public void processApiResponseValues(
            string lastRoundStatus,
            float lastMessageTime,
            string lastMessage,
            string partialMessage,
            string botLoopStep,
            string subject,
            string category
        )
    {
        localCategory = category;
        localLastBotLoopStep = botLoopStep;
        localLastMessage = lastMessage;
        localLastRoundStatus = lastRoundStatus;
        localPartialMessage = partialMessage;
        localCategory = category;
        localSubject = subject;


        if (!recievedFirstApiCall && botLoopStep == "STANDBY")
        {
            animatorScript.updateState(localLastBotLoopStep);
            recievedFirstApiCall = true;
            pageLoader.loadPage(initialPagePath);
            audioLoader.loadAudioClip(initialAudioPath);
        }
        else
        {
            animatorScript.updateState(localLastBotLoopStep);

            if (localLastMessageTime != lastMessageTime)
            {
                pageLoader.loadPage(generatedPagePath);
                audioLoader.loadAudioClip(generatedAudioPath);
            }
        }
        localLastMessageTime = lastMessageTime;

    }
}
