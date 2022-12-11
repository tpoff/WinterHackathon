using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class AvatarAnimatorScript : MonoBehaviour
{
    public bool isTalking = true;
    public bool isLookup = false;
    public Animator animator;//animator.SetBool("", false);
    public RuntimeAnimatorController newController;
    public AudioSource audioSource;
    // Start is called before the first frame update
    void Start()
    {
        audioSource = GetComponent<AudioSource>();

    }
    public void SetAnimator()
    {
        animator.runtimeAnimatorController = newController;
    }
    // Update is called once per frame
    void Update()
    {
        
    }

    public void updateState(string newState)
    {
        // TODO: once avatar model is built and animated. 
        if (newState == "DATA_LOOKUP")
        {
            animator.SetBool("isTalking", false);
            animator.SetBool("isLookup", true);
        }
        else if (audioSource.isPlaying)
        {
            animator.SetBool("isTalking", true);
            animator.SetBool("isLookup", false);

        }
        else
        {
            animator.SetBool("isTalking", false);
            animator.SetBool("isLookup", false);

        }
    }
}
