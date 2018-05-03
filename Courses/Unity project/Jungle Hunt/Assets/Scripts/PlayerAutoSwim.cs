using UnityEngine;
using UnityEngine.UI;

public class PlayerAutoSwim : MonoBehaviour
{
    double POSITION_X_ENDING = -8;
    double POSITION_SEA_BOTTOM = -4.4;
    double POSITION_SEA_LEVEL = 2.3;

    Rigidbody2D rigidBody;

    bool isMovementLocked = false;
    float currentOxygen = 10;
    float speedX = 2;
    float speedY = 5;

    public Slider breathingBar;

    void Awake()
    {
        rigidBody = gameObject.GetComponent<Rigidbody2D>();
    }

    void Start()
    {
        breathingBar.value = currentOxygen;
    }

    void Update()
    {
        var parent = gameObject.transform.parent;
        Rigidbody2D parentBody = null;

        var directionX = Input.GetAxis("Horizontal");
        var directionY = Input.GetAxis("Vertical");

        // If the player is trapped in bubble it should not be able to move till it goes over sea level.
        if (isMovementLocked)
        {
            parentBody = parent.GetComponent<Rigidbody2D>();

            float newVelocityX = parentBody.position.x - rigidBody.position.x;
            float newVelocityY = parentBody.position.y - rigidBody.position.y;

            rigidBody.velocity = new Vector2(newVelocityX, newVelocityY) * 7;
        }
        else
        {
            // Let the player control the x-axis speed (accelerate/deaccelerate)
            if (rigidBody.position.x > POSITION_X_ENDING)
            {
                var velocityX = -4 + (directionX * speedX);
                rigidBody.velocity = new Vector2(velocityX, rigidBody.velocity.y);
            }

            // Block the player from going deeper than the bottom of the sea
            if (rigidBody.position.y > POSITION_SEA_BOTTOM)
            {
                var velocityY = Mathf.Min(0, directionY * speedY);
                rigidBody.velocity = new Vector2(rigidBody.velocity.x, velocityY);
            }
        }

        // If the player is over the sea level
        if (rigidBody.position.y > POSITION_SEA_LEVEL)
        {
            // The player gets the oxygen slowly when it is over sea level
            currentOxygen = Mathf.Clamp(currentOxygen + 10 * Time.deltaTime, currentOxygen, 10);
            isMovementLocked = false;

            // Release the player from the bubble
            if (parent)
            {
                gameObject.transform.parent = null;
                Destroy(parent.gameObject);
            }
        }
        else
        {
            // Currently max time without breathing is 10 secs
            currentOxygen -= Time.deltaTime;

            if (currentOxygen < 0)
                GameManager.Instance.TakeDamage();
        }

        breathingBar.value = currentOxygen;
    }

    void OnCollisionEnter2D(Collision2D coll)
    {
        if (coll.gameObject.CompareTag("Croc"))
            GameManager.Instance.TakeDamage();

        if (coll.gameObject.CompareTag("LifeRing"))
            GameManager.Instance.LoadLevel("Level3");
    }

    void OnTriggerEnter2D(Collider2D coll)
    {
        if (coll.gameObject.CompareTag("Bubble"))
        {
            isMovementLocked = true;
            gameObject.transform.parent = coll.transform;
        }
        else if (coll.gameObject.CompareTag("Coin"))
        {
            GameManager.Instance.AddPoints(10);
            Destroy(coll.gameObject);
        }
    }
}
