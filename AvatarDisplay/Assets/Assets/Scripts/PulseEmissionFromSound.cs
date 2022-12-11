using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PulseEmissionFromSound : MonoBehaviour
{
    protected ControlEmission[] emissionControllers;
    public AudioSource audioSource;
    public int sampleDataLength = 2048;
    public float updateStep = 0.1f;
    private float currentUpdateTime = 0f;
    private float clipLoudness;
    private float[] clipSampleData;

    public float maxLoudness = .15f;
    public float smoothLoudnessDelta = .35f;


    protected float lastValue = 1;
    // Start is called before the first frame update
    void Start()
    {
        emissionControllers = GetComponents<ControlEmission>();
        audioSource = GetComponent<AudioSource>();
        Debug.Log(emissionControllers.Length);
        clipSampleData = new float[sampleDataLength];
    }

    

    // Update is called once per frame
    void Update()
    {
        currentUpdateTime += Time.deltaTime;
        if (currentUpdateTime >= updateStep)
        {
            currentUpdateTime = 0f;
            audioSource.clip.GetData(clipSampleData, audioSource.timeSamples); //I read 1024 samples, which is about 80 ms on a 44khz stereo clip, beginning at the current sample position of the clip.
            clipLoudness = 0f;
            foreach (var sample in clipSampleData)
            {
                clipLoudness += Mathf.Abs(sample);
            }
            clipLoudness /= sampleDataLength; //clipLoudness is what you are looking for
        }
        float newTarget = clipLoudness / maxLoudness;
        lastValue = Mathf.Lerp(lastValue, newTarget, smoothLoudnessDelta);
        updateEmissionValues(lastValue);
    }

    public void updateEmissionValues(float newEmission)
    {
        foreach (ControlEmission emissionController in emissionControllers){
            emissionController.adjustEmission(newEmission);
        }
    }
}
