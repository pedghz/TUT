using UnityEngine;
using UnityEngine.TestTools;
using NUnit.Framework;
using System.Collections;
using UnityEngine.UI;

public class TestSaveManager {

    [Test]
    public void TestSaveManagerSimplePasses() {
        PlayerPrefs.SetString("PlayerName", "player name");
        Assert.IsTrue(PlayerPrefs.GetString("PlayerName") == "player name");
    }

    // A UnityTest behaves like a coroutine in PlayMode
    // and allows you to yield null to skip a frame in EditMode
    [UnityTest]
    public IEnumerator TestSaveManagerWithEnumeratorPasses() {
        // Use the Assert class to test conditions.
        // yield to skip a frame
        yield return null;
    }
}
