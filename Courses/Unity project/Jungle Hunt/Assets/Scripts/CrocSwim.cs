using UnityEngine;

public class CrocSwim : MonoBehaviour
{
    float speedX = 3;
    bool isCrocFacingRight = false;
    Rigidbody2D rigidBody;

    void Start()
    {
        rigidBody = gameObject.GetComponent<Rigidbody2D>();
        InvokeRepeating("ChangeDirection", 0f, 1f);
    }

    void Update()
    {
        rigidBody.velocity = new Vector2(speedX, 0f);
    }

    void ChangeDirection()
    {
        isCrocFacingRight = !isCrocFacingRight;
        speedX *= -1;

        Vector2 scale = gameObject.transform.localScale;
        scale.x *= -1;
        transform.localScale = scale;
    }
}