using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ControlEmission : MonoBehaviour
{
    public GameObject target;
    protected Material mat;
    protected Color baseColor;
    protected Color minColor;
    protected Color maxColor;
    public float maxEmissionMultiplier = 1.2f;
    public float minEmissionMultiplier = .85f;
    public float emissionValue = 0.5f;
    public float pulseSpeed = 20f;
    public bool pulse = false;
    // Start is called before the first frame update
    void Start()
    {
        mat = target.GetComponent<Renderer>().material;
        baseColor = mat.GetColor("_EmissionColor");
        minColor = baseColor * minEmissionMultiplier;
        maxColor = baseColor * maxEmissionMultiplier; 
    }

    // Update is called once per frame
    void Update()
    {
        if (pulse)
        {
            minColor = baseColor * minEmissionMultiplier;
            maxColor = baseColor * maxEmissionMultiplier;

            float e = (Mathf.Sin(Time.time * pulseSpeed) + 1) / 2.0f;
            adjustEmission(e);

        }
    }
    public void adjustEmission(float newEmission)
    {
        Color newColor = Color.Lerp(minColor, maxColor, newEmission);
        mat.SetColor("_EmissionColor", newColor);

    }
}
