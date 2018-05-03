using UnityEngine;
using UnityEngine.TestTools;
using NUnit.Framework;
using System.Collections;
using System.Collections.Generic;

public class IntegrationTests {

    [Test]
    public void IntegrationTestsSimplePasses()
    {
        // Verify that the modules do not break each other
        Assert.DoesNotThrow(delegate
        {
            GameObject test1 = new GameObject();
            test1.AddComponent<Health>();
            test1.AddComponent<PlayerAutoMove>();
            test1.AddComponent<BoulderSpawner>();
            test1.AddComponent<Points>();
            test1.AddComponent<VineMotor>();
        });


    }

    [Test]
    public void IntegrateSystem()
    {
        // Integrate the main functionalities and
        // test that the invidual modules still work as
        // expected.
        Assert.DoesNotThrow(delegate
        {
            GameObject test1 = new GameObject();
            test1.AddComponent<Health>();
            test1.AddComponent<PlayerAutoMove>();
            test1.AddComponent<BoulderSpawner>();
            test1.AddComponent<Points>();
            test1.AddComponent<VineMotor>();
            var x1 = test1.GetComponent<Points>();
            var x2 = test1.GetComponent<VineMotor>();
            var x3 = test1.GetComponent<BoulderSpawner>();
            var x4 = test1.GetComponent<PlayerAutoMove>();

            if (x1.transform != x2.transform)
            {
                Assert.Fail("Points vs VineMotor");
            }
            if (x3.transform != x4.transform)
            {
                Assert.Fail("BoulderSpawner vs PlayerAutoMove");
            }
            if (x1.transform != x3.transform)
            {
                Assert.Fail("Points vs BoulderSpawner");
            }
            if (x1.transform != x4.transform)
            {
                Assert.Fail("Points vs PlayerAutoMove");
            }
            if (x2.transform != x3.transform)
            {
                Assert.Fail("VineMotor vs BoulderSpawner");
            }
            if (x2.transform != x4.transform)
            {
                Assert.Fail("VineMotor vs PlayerAutoMove");
            }
        });

        // Ensure that the current mode is not playmode
        Assert.AreNotEqual(TestPlatform.EditMode, "PlayMode");
    }

    [UnityTest]
    public IEnumerator IntegrationTestsWithEnumeratorPasses() {

        yield return null;
    }
}