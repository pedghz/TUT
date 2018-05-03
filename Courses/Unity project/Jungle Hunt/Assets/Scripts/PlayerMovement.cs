using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    double POSITION_X_ENDING = -8;
    double POSITION_X_STARTING = 68;

    int JUMP_POWER = 1200;

    Rigidbody2D rigidBody;
    Transform lastParent;

    bool isFacingRight = false;
    int speedX = 10;
    int jumpCounter = 0;

    private Animator animator;

    void Awake()
    {
        rigidBody = gameObject.GetComponent<Rigidbody2D>();
    }

    void Start()
    {
        animator = GetComponent<Animator>();
        FlipPlayer();
    }

    void Update()
    {
        var directionX = Input.GetAxis("Horizontal");
        var newSpeedX = directionX * speedX;

        if (Input.GetButtonDown("Jump") && jumpCounter < 2)
        {
            Jump();
            animator.SetTrigger("PlayerJump");
            animator.ResetTrigger("PlayerIdle");
            animator.ResetTrigger("PlayerRun");
        }

        // Flipping the player when needed
        if ( (directionX < 0 && !isFacingRight) || (directionX > 0 && isFacingRight) )
            FlipPlayer();

        // Limiting the player from going further than a specific amount from the right or left of the screen
        if (((rigidBody.position.x < POSITION_X_STARTING) && directionX > 0) ||
            (rigidBody.position.x > POSITION_X_ENDING) && directionX < 0)
        {
            rigidBody.velocity = new Vector2(newSpeedX, rigidBody.velocity.y);
            animator.SetTrigger("PlayerRun");
            animator.ResetTrigger("PlayerIdle");
        }
        // When left/right arrow keys are not pressed, so player is in idle state
        else
        {
            rigidBody.velocity = new Vector2(0, rigidBody.velocity.y);
            animator.SetTrigger("PlayerIdle");
            animator.ResetTrigger("PlayerRun");
        }

    }

    void Jump()
    {
        // Jump away from a vine
        if (transform.parent && transform.parent.CompareTag("Vine"))
        {
            transform.SetParent(null);

            transform.rotation = Quaternion.identity;
            rigidBody.isKinematic = false;
        }

        jumpCounter += 1;
        rigidBody.AddForce(Vector2.up * JUMP_POWER);
    }

    void FlipPlayer()
    {
        isFacingRight = !isFacingRight;

        Vector2 scale = transform.localScale;
        scale.x *= -1;
        transform.localScale = scale;
    }

    void OnCollisionEnter2D(Collision2D coll)
    {
        jumpCounter = 0;

        if (coll.gameObject.CompareTag("Floor"))
            GameManager.Instance.TakeDamage();

        if (coll.gameObject.CompareTag("Rock"))
            GameManager.Instance.LoadLevel("Level2");

        if (coll.gameObject.CompareTag("Cannibal"))
            GameManager.Instance.TakeDamage();

        if (coll.gameObject.CompareTag("Spouse"))
            GameManager.Instance.LoadLevel("Finish");
    }

    void OnTriggerEnter2D(Collider2D coll)
    {
        jumpCounter = 0;

        if (coll.gameObject.CompareTag("Vine"))
        {
            // Do nothing if it's already a child of a vine
            if (lastParent && coll.transform.IsChildOf(lastParent))
                return;

            lastParent = coll.transform.parent;

            transform.SetParent(coll.transform);

            transform.localPosition = new Vector3(0, 0, 0);
            rigidBody.isKinematic = true;

            GameManager.Instance.AddPoints(10);

            return;
        }

        if (coll.gameObject.CompareTag("Coin"))
        {
            GameManager.Instance.AddPoints(10);
            Destroy(coll.gameObject);
        }

    }
}
