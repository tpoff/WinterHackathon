using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApiHandler : MonoBehaviour
{
    public string generatedPagePath = "";
    public string generatedAudioPath = "";
    public string initialPagePath = "";
    public string initialAudioPath = "";
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



    // Start is called before the first frame update
    void Start()
    {
        animatorScript = GetComponent<AvatarAnimatorScript>();
        pageLoader = GetComponent<DynamicPageLoader>();
        emissionController = GetComponent<PulseEmissionFromSound>();
        audioLoader = GetComponent<LoadDynamicAudio>();

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
