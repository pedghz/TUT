using UnityEngine;

public class Bubble : MonoBehaviour
{
    float POSITION_Y_MAX = 2.3f;

    Rigidbody2D rigidBody;
    int speedY = 3;

    void Awake()
    {
        rigidBody = gameObject.GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        rigidBody.velocity = new Vector2(0, speedY);

        var positionY = rigidBody.position.y;
        var childCount = gameObject.transform.childCount;

        if (positionY > POSITION_Y_MAX && childCount < 1)
            Destroy(gameObject);
    }
}