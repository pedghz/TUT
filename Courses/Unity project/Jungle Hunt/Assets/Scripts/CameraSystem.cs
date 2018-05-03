using UnityEngine;

public class CameraSystem : MonoBehaviour
{
    float MIN = 0;
    float MAX = 60;
    float OFFSET = 5;

    public GameObject Player;

    void Start()
    {
        Player = Player ? Player : GameObject.FindGameObjectWithTag("Player");
    }

    void LateUpdate()
    {
        Vector3 oldPosition = gameObject.transform.position;

        gameObject.transform.position = new Vector3(
            Player ?
                Mathf.Clamp(Player.transform.position.x - OFFSET, MIN, MAX) :
                0,
            oldPosition.y,
            oldPosition.z
        );
    }
}
