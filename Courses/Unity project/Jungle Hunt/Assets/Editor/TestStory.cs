using UnityEngine;
using UnityEngine.TestTools;
using NUnit.Framework;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;

public class TestStory {

    [Test]
    public void TestStorySimplePasses()
    {
        // Test initiating a storyteller
        Assert.DoesNotThrow(delegate
        {
            GameObject test1 = new GameObject();
            test1.AddComponent<StoryTeller>();
            var x1 = test1.GetComponent<StoryTeller>();
            x1.ChapterText = null;
        });

        // Verify that an invalid operation throws an error
        Assert.Throws<System.NullReferenceException>(delegate
        {
            GameObject test = new GameObject();
            test.AddComponent<StoryTeller>();
            var x = test.GetComponent<StoryTeller>();

            Assert.Equals(x.story.Count, 0);
        });
    }

    [Test]
    public void MakingNewStory()
    {
        GameObject test1 = new GameObject();
        test1.AddComponent<StoryTeller>();
        var x1 = test1.GetComponent<StoryTeller>();
        x1.story = new List<string>();
        x1.story.Add("Hej");
        x1.story.Add("Hei");
        x1.story.Add("Hello");

        Assert.True(x1.story.Count == 3);
    }

    [Test]
    public void EditingStory()
    {
        GameObject test1 = new GameObject();
        test1.AddComponent<StoryTeller>();
        var x1 = test1.GetComponent<StoryTeller>();
        x1.story = new List<string>();
        x1.story.Add("Hej");
        x1.story[0] = "Moi";

        Assert.True(x1.story[0] == "Moi");
    }

    [UnityTest]
    public IEnumerator TestStoryWithEnumeratorPasses() {

        yield return null;
    }
}