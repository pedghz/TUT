using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoulderSpawner : MonoBehaviour
{
    public GameObject BigBoulder;
    public GameObject SmallBoulder;
    public GameObject Player;

    void Start()
    {
        SpawnBoulders();
    }

    void SpawnBoulders()
    {
        var boulderX = Player.transform.position.x - 20;

        var positionBig = new Vector3(boulderX, Random.Range(1f, 2.5f), 0);
        var positionSmall = new Vector3(boulderX, -3, 0);

        var rand = Random.Range(0, 2);

        if (rand == 1)
            Instantiate(BigBoulder, positionBig, Quaternion.identity);
        else
            Instantiate(SmallBoulder, positionSmall, Quaternion.identity);

        Invoke("SpawnBoulders", Random.Range(0.8f, 1.6f));
    }
}
