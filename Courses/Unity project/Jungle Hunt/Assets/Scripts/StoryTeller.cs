using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class StoryTeller : MonoBehaviour
{
    public Image BackGround;
    public Text ChapterText;

    public AudioSource MusicSource;
    public AudioClip StoryMusic;

    public Canvas menuCanvas;
    public Canvas storyCanvas;
    public List<string> story;

    public string LevelToLoad;
    public bool autoLoadLevel;
    
    private int activeSlideIndex = 0;
    
    private int secondsBetweenFrames = 3;
    private float deltaTime;


    void Start()
    {
        if(menuCanvas)
        {
            menuCanvas.enabled = false;
        }
        storyCanvas.enabled = true;

        for (int slide = 0; slide < story.Count; slide++)
        {
            if(story[slide].Contains("$"))
            {
                string format = story[slide].Substring(story[slide].IndexOf("$")+1, 3);
                story[slide] = story[slide].Replace("$" + format, GameManager.Instance.GetVar(format));
            }
        }

        ChapterText.text = story[activeSlideIndex];
    }

    void Update()
    {
        deltaTime += Time.deltaTime;

        if (Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.Mouse0))
        {
            incrementSlide();
        }
        else if (deltaTime > secondsBetweenFrames)
        {
            deltaTime = 0;
            incrementSlide();
        }

        if (activeSlideIndex == story.Count)
        {
            EndStory();
        }
        if (activeSlideIndex < story.Count)
        {
            ChapterText.text = story[activeSlideIndex];
        }
    }

    void EndStory()
    {
        if(autoLoadLevel || Input.anyKey)
        {
            GameManager.Instance.LoadLevel(LevelToLoad);
        }
    }

    void incrementSlide()
    {
        if (activeSlideIndex < story.Count)
        {
            activeSlideIndex += 1;
        }
    }
}
