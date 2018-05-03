using UnityEngine;
using UnityEngine.UI;

public class Health : MonoBehaviour
{
    public Text HealthText;

    void Start()
    {
        UpdateHealth();
    }

    public void UpdateHealth()
    {
        HealthText.text = GameManager.Instance.GetHealth().ToString();
    }
}
