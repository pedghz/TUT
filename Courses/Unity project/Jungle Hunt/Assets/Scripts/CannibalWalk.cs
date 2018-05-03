using UnityEngine;

public class CannibalWalk : MonoBehaviour
{
    float speedX = 3;
    bool isCannibalFacingRight = false;
    Rigidbody2D rigidBody;

    void Start()
    {
        rigidBody = gameObject.GetComponent<Rigidbody2D>();
        InvokeRepeating("ChangeDirection", 0f, Random.Range(1f, 3f));
    }

    void Update()
    {
        rigidBody.velocity = new Vector2(speedX, 0f);
    }

    void ChangeDirection()
    {
        isCannibalFacingRight = !isCannibalFacingRight;
        speedX *= -1;

        Vector2 scale = gameObject.transform.localScale;
        scale.x *= -1;
        transform.localScale = scale;
    }
}