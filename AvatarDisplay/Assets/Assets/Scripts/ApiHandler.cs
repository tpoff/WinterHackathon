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
    public string BotLoopStep;
    public string Category;
    public string LastRoundStatus;
    public float LastMessageTime;
    public string LastMessage;
    public string PartialMessage;
    public string Subject;
}
public class ApiHandler : MonoBehaviour
{
    public string api_endpoint = "http://127.0.0.1:5000/api/status";

    public string generatedPagePath = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\html_result.html";
    public string generatedAudioPath = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\tts_response.wav";
    public string initialPagePath = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\SplashPage.html";
    public string initialAudioPath = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\splash_audio.wav";
    public string lookupAudio = "C:\\Users\\Tyler\\Desktop\\Hackathon\\WinterHackathon\\BotContent\\lookup.wav";

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

    public bool playSplash = true;

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
            processApiResponseValues(
                    info.LastRoundStatus,
                        info.LastMessageTime,
                        info.LastMessage,
                        info.PartialMessage,
                        info.BotLoopStep,
                        info.Subject,
                        info.Category);
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
        if (playSplash)
            StartCoroutine(WaitForSplash());
        else
            StartCoroutine(GetBotStatus());

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

        if (!recievedFirstApiCall)
        {
            if (botLoopStep == "STANDBY")
            {
                Debug.Log("recording first api call...");
                animatorScript.updateState(botLoopStep);
                recievedFirstApiCall = true;
                localLastMessageTime = lastMessageTime;
            }
        }
        else
        {
            Debug.Log(botLoopStep);
            animatorScript.updateState(botLoopStep);

            if (localLastMessage != lastMessage && botLoopStep=="STANDBY")
            {
                Debug.Log("api records a need to update audio and page content...");
                pageLoader.loadPage(generatedPagePath);
                audioLoader.loadAudioClip(generatedAudioPath);
                localLastMessageTime = lastMessageTime;
                localLastMessage = lastMessage;
            }
            else if (botLoopStep== "DATA_LOOKUP" && localLastBotLoopStep != "DATA_LOOKUP")
            {
                audioLoader.loadAudioClip(lookupAudio);

            }
        }

        localCategory = category;
        localLastBotLoopStep = botLoopStep;
        localLastRoundStatus = lastRoundStatus;
        localPartialMessage = partialMessage;
        localCategory = category;
        localSubject = subject;

    }
}
