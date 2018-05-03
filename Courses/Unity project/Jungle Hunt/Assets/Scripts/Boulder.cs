using UnityEngine;

public class Boulder : MonoBehaviour
{
    Rigidbody2D rigidBody;

    void Start()
    {
        rigidBody = gameObject.GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        transform.Rotate(0, 0, -200 * Time.deltaTime);
        rigidBody.velocity = new Vector2(2, rigidBody.velocity.y);
    }
}