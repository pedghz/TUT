using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BubbleSpawner : MonoBehaviour
{
    public GameObject Bubble;
    public GameObject Player;
    public GameObject SeaFloor;

    void Start()
    {
        SpawnBubbles();
    }

    void SpawnBubbles()
    {
        var positionX = Player.transform.position.x - Random.Range(4, 10);
        var positionY = SeaFloor.transform.position.y - 1;
        var position = new Vector3(positionX, positionY, 0);

        Instantiate(Bubble, position, Quaternion.identity);

        Invoke("SpawnBubbles", Random.Range(0.3f, 3f));
    }
}
