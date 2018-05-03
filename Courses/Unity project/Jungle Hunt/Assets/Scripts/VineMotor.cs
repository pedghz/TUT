using UnityEngine;

public class VineMotor : MonoBehaviour
{
    float MAX_ANGULAR_VELOCITY = 5.0f;

    Rigidbody2D rigidBody;
    float speed;

    public float MaxSpeed;

    void Start()
    {
        rigidBody = gameObject.GetComponent<Rigidbody2D>();

        // TODO: Isn't max speed the max speed?? Why is speed 100x the max speed?
        speed = MaxSpeed * 100;
    }

    void Update()
    {
        if (Mathf.Abs(rigidBody.angularVelocity) < MAX_ANGULAR_VELOCITY)
        {
            rigidBody.AddTorque(speed);
            speed = -speed;
        }
    }
}
