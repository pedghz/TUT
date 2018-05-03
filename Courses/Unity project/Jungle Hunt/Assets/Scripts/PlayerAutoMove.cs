using UnityEngine;

public class PlayerAutoMove : MonoBehaviour
{
    int THRESHOLD_X = -12;

    Rigidbody2D rigidBody;

    bool isJumping = false;

    int speedX = 5;
    int jumpPower = 1200;
    int jumpCounter = 0;

    private Animator animator;

    void Awake()
    {
        rigidBody = gameObject.GetComponent<Rigidbody2D>();
    }

    void Start()
    {
        animator = GetComponent<Animator>();
        animator.ResetTrigger("PlayerIdle");
        animator.SetTrigger("PlayerWalk");
    }

    void Update()
    {
        var directionX = Input.GetAxis("Horizontal");

        // Handle ducking
        if (!isJumping && Input.GetKey("down"))
            rigidBody.rotation = 90;
        else
            rigidBody.rotation = 0;

        // Handle jumping
        if (Input.GetButtonDown("Jump") && jumpCounter < 2)
            Jump();

        // Set the velocity of the player automatically
        if (rigidBody.position.x > THRESHOLD_X)
        {
            rigidBody.velocity = new Vector2(-7 + (directionX * speedX),  rigidBody.velocity.y);
            if (directionX == 1)
            {
                animator.SetTrigger("PlayerSlow");
                animator.ResetTrigger("PlayerWalk");
                animator.ResetTrigger("PlayerRun");
            }
            else if (directionX == -1)
            {
                animator.SetTrigger("PlayerRun");
                animator.ResetTrigger("PlayerWalk");
                animator.ResetTrigger("PlayerSlow");
            }
            else
            {
                animator.SetTrigger("PlayerWalk");
                animator.ResetTrigger("PlayerRun");
                animator.ResetTrigger("PlayerSlow");
            }
        }
    }

    void Jump()
    {
        if (Mathf.Abs(rigidBody.rotation) < Mathf.Epsilon)
        {
            animator.SetTrigger("PlayerJump");
            animator.ResetTrigger("PlayerIdle");
            animator.ResetTrigger("PlayerRun");
            jumpCounter += 1;
            isJumping = true;
            rigidBody.AddForce(Vector2.up * jumpPower);
        }
    }

    void OnCollisionEnter2D(Collision2D coll)
    {
        jumpCounter = 0;
        isJumping = false;

        if (coll.gameObject.CompareTag("Boulder"))
            GameManager.Instance.TakeDamage();

        if (coll.gameObject.CompareTag("Portal"))
            GameManager.Instance.LoadLevel("Level4");
    }

    void OnTriggerEnter2D(Collider2D coll)
    {
        if (coll.gameObject.CompareTag("Coin"))
        {
            GameManager.Instance.AddPoints(10);
            Destroy(coll.gameObject);
        }
    }
}
